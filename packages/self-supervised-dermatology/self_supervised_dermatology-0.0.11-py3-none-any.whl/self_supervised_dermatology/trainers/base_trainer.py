import torch
import sys
import math
import os
import shutil
import copy
import wandb
import torchmetrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch.nn.functional as F
from collections import OrderedDict
from typing import Union, Tuple
from pathlib import Path
from abc import ABC
from abc import abstractmethod
from torchvision import transforms
from torch.utils.data import DataLoader
from scipy import stats
from sklearn.decomposition import PCA

from src.datasets.encrypted_image_folder import EncryptedImageFolder
from src.datasets.utils import get_train_validation_data_loaders
from src.datasets.downstream.pad_ufes_20_dataset import PADUFES20Dataset
from src.datasets.downstream.ham10000_dataset import HAM10000Dataset
from src.datasets.downstream.fitzpatrick17_dataset import Fitzpatrick17kDataset
from src.datasets.downstream.isic_task1_dataset import ISICTask1Dataset
from src.models.classifiers import LinearClassifier
from src.models.segmentation import DecoderLinear, FCN16s, FCN8s, DecoderConv
from src.utils.metrics import mIoU, pixel_accuracy
from src.models.utils import ModelType
from src.optimizers.lars import LARS
from src.utils.utils import is_main_process, is_dist_avail_and_initialized
from src.models.utils import cosine_scheduler


class Trainer(ABC, object):

    def __init__(self,
                 train_dataset,
                 val_dataset,
                 config: dict,
                 config_path: Union[str, Path],
                 arch_name: str,
                 debug=False,
                 evaluation: bool = False,
                 project_name='vm02-SSL'):
        self.config = config
        self.config_path = config_path
        self.device = self._get_device()
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.start_epoch = 1
        self.debug = debug

        # logging to W&B
        wandb.init(config=self.config,
                   project=project_name,
                   group=arch_name if not evaluation else "downstream")

        # distributed training configuration
        self.multi_gpu = False
        self.dist_training = is_dist_avail_and_initialized()
        if self.dist_training:
            self.local_rank = int(os.environ['LOCAL_RANK'])
            run_name = f'{arch_name}-{wandb.run.name}-rank-{self.local_rank}'
        else:
            run_name = f'{arch_name}-{wandb.run.name}'

        # update the name of the run
        wandb.run.name = run_name
        wandb.run.save()
        self.run_dir = Path(wandb.run.dir)

        # check if the trainer is in eval mode or not
        if not evaluation:
            # set all the required attributes of the model
            self.set_model_attributes()
            # load the downstream tasks and classifiers
            self.load_downstream_tasks()
            # logging
            print(f"Data loaded: there are "
                  f"{len(self.train_dataset)*self.config['batch_size']} train images.")
            print(f"Data loaded: there are "
                  f"{len(self.val_dataset)*self.config['batch_size']} val images.")
        # debug pytorch code
        torch.autograd.set_detect_anomaly(True)
        # optimize various tensor operations automatically
        torch.backends.cudnn.benchmark = True

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def _get_embedding(self, model, img) -> torch.Tensor:
        pass

    @property
    def get_ckp_path(self) -> Path:
        return self.run_dir / self.config['fine_tune_from'] / 'checkpoints'

    def set_model_attributes(self):
        # get model type
        self.model_type = ModelType[self.config['model']['model_type']]
        if self.model_type is None:
            raise ValueError('Wrong model type')
        if self.model_type is ModelType.VIT:
            self.embed_dim = self.config['model']['emb_dim'] * self.config[
                'model']['eval']['n_last_blocks']
        else:
            self.embed_dim = self.config['model']['emb_dim']
            if 'base_model' in self.config['model']:
                embed_dict = {
                    "resnet18": 512,
                    "resnet50": 2048,
                }
                self.embed_dim = embed_dict.get(
                    self.config['model']['base_model'], self.embed_dim)

    def distribute_model(self, model: torch.nn.Module) -> torch.nn.Module:
        if torch.cuda.device_count() > 1:
            print(f'Multiple GPUs detected, model will run on '
                  f'{torch.cuda.device_count()} GPUs!')
            if self.dist_training:
                print('Distributed training, distributing the model.')
                model = torch.nn.parallel.DistributedDataParallel(
                    model,
                    device_ids=[self.local_rank],
                    output_device=self.local_rank)
            else:
                model = torch.nn.DataParallel(model)
            self.multi_gpu = True
        else:
            print('Single GPU detected, model will run on single instance.')
        return model

    def get_optimizer(self, optimizer_name: str):
        optimizer_dict = {
            'adam': torch.optim.Adam,
            'adamw': torch.optim.AdamW,
            'sgd': torch.optim.SGD,
            'lars': LARS,
        }
        optimizer_cls = optimizer_dict.get(optimizer_name, np.nan)
        if optimizer_cls is np.nan:
            raise ValueError('Invalid optimizer name.')
        return optimizer_cls

    def load_downstream_tasks(self):
        # configs
        train_transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])
        val_transform = transforms.Compose([
            transforms.Resize(256, interpolation=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])
        mask_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        d_config = self.config['downstream']

        # PADUFES20Dataset (diagnosis, classification)
        self.load_pad_ufes_20(d_config, train_transform, val_transform)
        # HAM10000Dataset (diagnosis, classification)
        self.load_ham10000(d_config, train_transform, val_transform)
        # Fitzpatrick17kDataset (diagnosis, classification)
        self.load_fitzpatrick17k(d_config, train_transform, val_transform)
        # ISIC Task 1 (segmentation)
        self.load_isic_task1(d_config, train_transform, mask_transform)
        # Body Localization (classification)
        self.load_body_loc(d_config, train_transform)

    def load_pad_ufes_20(self, d_config: dict,
                         train_transform: transforms.Compose,
                         val_transform: transforms.Compose):
        if d_config['pu_path'] is not None:
            pu_path = Path(d_config['pu_path'])
            self.pu_dataset = PADUFES20Dataset(csv_file=pu_path / 'metadata.csv',
                                               root_dir=pu_path / 'images',
                                               transform=train_transform,
                                               val_transform=val_transform)
            self.pu_train, self.pu_val = get_train_validation_data_loaders(
                self.pu_dataset, self.config['batch_size'],
                **d_config['splitter'])
            # classifier
            self.pu_clf = LinearClassifier(
                self.embed_dim,
                self.pu_dataset.n_classes)
            self.pu_clf = self.pu_clf.to(self.device)

    def load_ham10000(self, d_config: dict,
                      transform: transforms.Compose,
                      val_transform: transforms.Compose):
        if d_config['ham_path'] is not None:
            ham_path = Path(d_config['ham_path'])
            self.ham_dataset = HAM10000Dataset(csv_file=ham_path / 'HAM10000_metadata.csv',
                                               dataset_dir=ham_path,
                                               transform=transform,
                                               val_transform=val_transform)
            self.ham_train, self.ham_val = get_train_validation_data_loaders(
                self.ham_dataset, self.config['batch_size'],
                **d_config['splitter'])
            # classifier
            self.ham_clf = LinearClassifier(
                self.embed_dim,
                self.ham_dataset.n_classes)
            self.ham_clf = self.ham_clf.to(self.device)

    def load_fitzpatrick17k(self, d_config: dict,
                            transform: transforms.Compose,
                            val_transform: transforms.Compose):
        if d_config['fitz_path'] is not None:
            fitz_path = Path(d_config['fitz_path'])
            self.fitz_dataset = Fitzpatrick17kDataset(
                csv_file=fitz_path / 'fitzpatrick17k.csv',
                dataset_dir=fitz_path,
                transform=transform,
                val_transform=val_transform)
            self.fitz_train, self.fitz_val = get_train_validation_data_loaders(
                self.fitz_dataset, self.config['batch_size'],
                **d_config['splitter'])
            # classifier
            self.fitz_clf = LinearClassifier(
                self.embed_dim,
                self.fitz_dataset.n_classes)
            self.fitz_clf = self.fitz_clf.to(self.device)

    def load_body_loc(self, d_config: dict, transform: transforms.Compose):
        if d_config['body_loc_path'] is not None:
            base_path = Path(d_config['body_loc_path'])
            train_path = base_path / 'strong_labels_train'
            test_path = base_path / 'strong_labels_test'
            test2_path = base_path / 'strong_labels_test_balanced510'
            # Train / Val set
            self.body_loc_dataset = EncryptedImageFolder(
                train_path,
                enc_keys=[str(base_path / 'key.key')],
                transform=transform)
            self.body_loc_train, self.body_loc_val = get_train_validation_data_loaders(
                self.body_loc_dataset, self.config['batch_size'],
                **d_config['splitter'])
            # Test set
            self.body_loc_test = EncryptedImageFolder(
                test_path,
                enc_keys=[str(base_path / 'key.key')],
                transform=transform)
            self.body_loc_test = DataLoader(
                self.body_loc_test,
                batch_size=self.config['batch_size'],
                drop_last=False,
                shuffle=False)
            self.body_loc_test2 = EncryptedImageFolder(
                test2_path,
                enc_keys=[str(base_path / 'key.key')],
                transform=transform)
            self.body_loc_test2 = DataLoader(
                self.body_loc_test2,
                batch_size=self.config['batch_size'],
                drop_last=False,
                shuffle=False)
            # classifier
            self.body_loc_clf = LinearClassifier(
                self.embed_dim,
                len(self.body_loc_dataset.classes))
            self.body_loc_clf = self.body_loc_clf.to(self.device)

    def load_isic_task1(self, d_config: dict, transform: transforms.Compose,
                        mask_transform: transforms.Compose):
        if d_config['isic_path'] is not None:
            # dataset
            isic_path = Path(d_config['isic_path'])
            self.isic_train = ISICTask1Dataset(
                dataset_dir=isic_path,
                dataset_type='train',
                transform=transform,
                mask_transform=mask_transform)
            self.isic_val = ISICTask1Dataset(
                dataset_dir=isic_path,
                dataset_type='val',
                transform=transform,
                mask_transform=mask_transform)
            self.isic_train = DataLoader(
                self.isic_train,
                batch_size=self.config['batch_size'],
                num_workers=d_config['splitter']['num_workers'],
                drop_last=True,
                shuffle=True)
            self.isic_val = DataLoader(
                self.isic_val,
                batch_size=self.config['batch_size'],
                num_workers=d_config['splitter']['num_workers'],
                drop_last=True,
                shuffle=True)

            # decoder
            if self.model_type is ModelType.VIT:
                self.isic_dec = DecoderLinear(
                    n_cls=1,
                    patch_size=self.config['model']['student']['patch_size'],
                    d_encoder=self.embed_dim)
            elif self.model_type is ModelType.CNN:
                self.isic_dec = FCN8s(
                    num_classes=1,
                    backbone_name=self.config['model']['base_model'],
                    backbone=None)
            elif self.model_type is ModelType.UNET:
                self.isic_dec = DecoderConv(dim_in=2, num_labels=1)
            self.isic_dec = self.isic_dec.to(self.device)

    def eval_classification_task(self,
                                 loader,
                                 val_loader,
                                 classifier,
                                 model,
                                 task_name: str,
                                 n_iter: int,
                                 fine_tune: bool = False):
        # loss function, optimizer, scores
        ce_loss = torch.nn.CrossEntropyLoss(
            label_smoothing=self.config['downstream']['label_smoothing'])
        ce_loss = ce_loss.to(self.device)

        if self.config['optim'] == "sgd":
            optimizer = torch.optim.SGD(
                params=classifier.parameters(),
                lr=self.config['downstream']['lr'] * self.config['batch_size'] / 256,
                momentum=0.9,
                weight_decay=0,
            )
        elif self.config['optim'] == "adam":
            optimizer = torch.optim.Adam(
                params=classifier.parameters(),
                lr=self.config['downstream']['lr'] * self.config['batch_size'] / 256,
                weight_decay=0,
            )
        elif self.config['optim'] == "adamw":
            optimizer = torch.optim.AdamW(
                params=classifier.parameters(),
                lr=self.config['downstream']['lr'] * self.config['batch_size'] / 256,
            )
        else:
            raise ValueError(
                f'Unrecognized optimizer name: {self.config["optim"]}')

        # define the learning rate scheduler
        lr_schedule = cosine_scheduler(
            # linear scaling rule
            self.config['lr'] * self.config['batch_size'] / 256.,
            eval(self.config['min_lr']),
            self.config['downstream_train_epochs'],
            len(loader),
            warmup_epochs=self.config['warmup_epochs'],
        )
        wd_schedule = cosine_scheduler(
            self.config['weight_decay'],
            self.config['weight_decay_end'],
            self.config['downstream_train_epochs'],
            len(loader),
        )

        # define metrics
        loss_metric_train = torchmetrics.MeanMetric()
        loss_metric_train = loss_metric_train.to(self.device)
        accuracy_top_1_train = torchmetrics.Accuracy(
            num_classes=classifier.num_labels, top_k=1, average='macro')
        accuracy_top_1_train = accuracy_top_1_train.to(self.device)
        f1_score_train = torchmetrics.F1Score(
            num_classes=classifier.num_labels, average='macro')
        f1_score_train = f1_score_train.to(self.device)

        loss_metric_val = torchmetrics.MeanMetric()
        loss_metric_val = loss_metric_val.to(self.device)
        accuracy_top_1_val = torchmetrics.Accuracy(
            num_classes=classifier.num_labels, top_k=1, average='macro')
        accuracy_top_1_val = accuracy_top_1_val.to(self.device)
        f1_score_val = torchmetrics.F1Score(num_classes=classifier.num_labels,
                                            average='macro')
        f1_score_val = f1_score_val.to(self.device)

        # metrics
        l_loss_train = []
        l_f1_train = []
        l_acc_train = []
        l_loss_val = []
        l_f1_val = []
        l_acc_val = []
        step = 0
        # start training
        for epoch in range(self.config['downstream_train_epochs']):
            # training
            model.train()
            classifier.train()
            loader.dataset.training = True
            for img, target in loader:
                # update weight decay and LR according to their schedule
                # but only if wanted
                self.update_optim_from_schedulers(optimizer, lr_schedule,
                                                  wd_schedule, step)
                # move batch to device
                img = img.to(self.device)
                target = target.to(self.device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # retreive the embedding
                if fine_tune:
                    if self.model_type is ModelType.UNET:
                        img = img[:, 1, :, :][:, None, :, :]
                    emb = self._get_embedding(model, img)
                else:
                    with torch.no_grad():
                        if self.model_type is ModelType.UNET:
                            img = img[:, 1, :, :][:, None, :, :]
                        emb = self._get_embedding(model, img)
                # forward pass through the classifier
                pred = classifier(emb)

                # calculate loss and scores
                loss = ce_loss(pred, target)

                # backpropagation
                loss.backward()
                optimizer.step()

                # log to W&B
                log_dict = {
                    f'Downstream/{task_name}/train_loss': loss.item(),
                    f'Downstream/{task_name}/train_f1': f1_score_train(pred, target),
                    f'Downstream/{task_name}/epoch': epoch,
                    f'Downstream/{task_name}/step': step,
                }
                wandb.log(log_dict)
                step += 1

                # add to overall metrics
                loss_metric_train.update(loss.detach())
                accuracy_top_1_train.update(pred, target)
                f1_score_train.update(pred, target)
            l_loss_train.append(loss_metric_train.compute())
            l_f1_train.append(f1_score_train.compute())
            l_acc_train.append(accuracy_top_1_train.compute())

            # Validation
            model.eval()
            classifier.eval()
            val_loader.dataset.training = False
            l_pred_val = []
            l_target_val = []
            for img, target in val_loader:
                # move batch to device
                img = img.to(self.device)
                target = target.to(self.device)

                # retreive the embedding
                with torch.no_grad():
                    if self.model_type is ModelType.UNET:
                        img = img[:, 1, :, :][:, None, :, :]
                    emb = self._get_embedding(model, img)
                    # forward pass through the classifier
                    pred = classifier(emb)

                # calculate loss and scores
                loss = ce_loss(pred, target)
                # add to overall metrics
                l_pred_val.append(pred)
                l_target_val.append(target)
                loss_metric_val.update(loss.detach())
                accuracy_top_1_val.update(pred, target)
                f1_score_val.update(pred, target)
            l_loss_val.append(loss_metric_val.compute())
            l_f1_val.append(f1_score_val.compute())
            l_acc_val.append(accuracy_top_1_val.compute())
            print(f'Epoch: {epoch}, '
                  f'Train Loss: {l_loss_train[-1]}, '
                  f'Train Acc: {l_acc_train[-1]}, '
                  f'Train F1: {l_f1_train[-1]}, '
                  f'Valid Loss: {l_loss_val[-1]}, '
                  f'Valid Acc: {l_acc_val[-1]}, '
                  f'Valid F1: {l_f1_val[-1]}')
            # log to W&B
            log_dict = {
                f'Downstream/{task_name}/valid_loss': l_loss_val[-1],
                f'Downstream/{task_name}/valid_f1': l_f1_val[-1],
                f'Downstream/{task_name}/epoch': epoch,
                f'Downstream/{task_name}/step': step,
            }
            wandb.log(log_dict)

            # log confusion matrix to track progress
            wandb.log(
                {
                    f'downstream/cm_{task_name}_valid':
                    wandb.plot.confusion_matrix(
                        probs=torch.cat(l_pred_val).cpu().detach().numpy(),
                        preds=None,
                        y_true=torch.cat(l_target_val).cpu().detach().numpy(),
                        class_names=loader.dataset.classes)
                },
                step=n_iter)

        # get the best epoch in terms of F1 score
        best_epoch = torch.Tensor(l_f1_val).argmax()
        # log to W&B
        log_dict = {
            f'Downstream/{task_name}/best_val_epoch': best_epoch,
            f'Downstream/{task_name}/best_train_loss': l_loss_train[best_epoch],
            f'Downstream/{task_name}/best_train_acc_top_1': l_acc_train[best_epoch],
            f'Downstream/{task_name}/best_train_f1_score': l_f1_train[best_epoch],
            f'Downstream/{task_name}/best_val_loss': l_loss_val[best_epoch],
            f'Downstream/{task_name}/best_val_acc_top_1': l_acc_val[best_epoch],
            f'Downstream/{task_name}/best_val_f1_score': l_f1_val[best_epoch],
            f'Downstream/{task_name}/epoch': epoch,
            f'Downstream/{task_name}/step': step,
        }
        wandb.log(log_dict)

    def eval_segmentation_task(self, loader, decoder, model, backbone,
                               task_name: str, validation: bool, n_iter: int):
        if self.model_type is ModelType.CNN:
            # set the backbone
            decoder.set_backbone(backbone)

        # loss function, optimizer, scores
        bce_loss = torch.nn.BCEWithLogitsLoss()
        bce_loss = bce_loss.to(self.device)

        optimizer = torch.optim.Adam(decoder.parameters(),
                                     lr=self.config['downstream']['lr'])
        # configs
        if validation:
            prefix = 'val'
            decoder.eval()
        else:
            prefix = 'train'
            decoder.train()

        # define metrics
        loss_metric = torchmetrics.MeanMetric()
        loss_metric = loss_metric.to(self.device)

        iou_metric = torchmetrics.MeanMetric()
        iou_metric = iou_metric.to(self.device)

        acc_metric = torchmetrics.MeanMetric()
        acc_metric = acc_metric.to(self.device)

        # how many epochs to train
        if not validation:
            n_epochs = self.config['downstream_train_epochs']
        else:
            n_epochs = 1
        l_loss = []
        l_iou = []
        l_acc = []
        # start training
        for epoch in range(n_epochs):
            for img, target in loader:
                # move batch to device
                img = img.to(self.device)
                target = target.to(self.device)

                # zero the parameter gradients
                optimizer.zero_grad()

                if self.model_type is ModelType.VIT:
                    with torch.no_grad():
                        # retreive the embedding
                        emb = model.backbone.get_intermediate_layers(
                            img,
                            n=self.config['model']['eval']['n_last_blocks'])
                        emb = torch.cat(emb, dim=-1)
                        # remove the class token for reconstruction
                        emb = emb[:, 1:, :]
                    # forward pass through the classifier
                    mask = decoder(emb,
                                   im_size=(img.shape[-2], img.shape[-1]))
                elif self.model_type is ModelType.CNN:
                    mask = decoder(img)
                elif self.model_type is ModelType.UNET:
                    im_size = (img.shape[-2], img.shape[-1])
                    imgs_g = img[:, 1, :, :][:, None, :, :]
                    out, _ = model(imgs_g)
                    mask = decoder(out, im_size=im_size)

                # calculate loss and scores
                loss = bce_loss(mask, target)
                iou = mIoU(mask, target)
                acc = pixel_accuracy(mask, target)

                if self.debug:
                    print(f'Loss: {loss.item()}, IOU: {iou}, PixAcc: {acc}')

                if not validation:
                    # backpropagation
                    loss.backward()
                    optimizer.step()

                # add to overall metrics
                loss_metric.update(loss.detach())
                iou_metric.update(iou)
                acc_metric.update(acc)
            l_loss.append(loss_metric.compute())
            l_iou.append(iou_metric.compute())
            l_acc.append(acc_metric.compute())
            print(
                f'Epoch: {epoch}, Loss: {l_loss[-1]}, Acc: {l_acc[-1]}, IOU: {l_iou[-1]}'
            )

        # get the best epoch in terms of IOU score
        best_epoch = torch.Tensor(l_iou).argmax()
        # log to W&B
        log_dict = {
            f'Downstream/{task_name}/{prefix}_best_epoch': best_epoch,
            f'Downstream/{task_name}/{prefix}_loss': l_loss[best_epoch],
            f'Downstream/{task_name}/{prefix}_iou': l_iou[best_epoch],
            f'Downstream/{task_name}/{prefix}_pix_acc': l_acc[best_epoch],
        }
        wandb.log(log_dict, step=n_iter)

    def eval_downstream_tasks(self,
                              model,
                              backbone,
                              n_iter: int,
                              fine_tune: bool = False):
        if is_main_process():
            print('*' * 20 + ' Eval Downstream Tasks ' + '*' * 20)

            # check if multi gpu or not
            if self.multi_gpu:
                model = model.module

            # define our classification tasks
            clf_tasks = []
            # define our segmentation tasks
            seg_tasks = []
            # load downstream config
            d_config = self.config['downstream']

            # fitzpatrick17k
            if d_config['fitz_path'] is not None:
                clf_tasks.append({
                    'train': self.fitz_train,
                    'val': self.fitz_val,
                    'clf': self.fitz_clf,
                    'name': 'fitzpatrick17k',
                })

            # pad_ufes_20
            if d_config['pu_path'] is not None:
                clf_tasks.append({
                    'train': self.pu_train,
                    'val': self.pu_val,
                    'clf': self.pu_clf,
                    'name': 'pad_ufes_20',
                })

            # ham10000
            if d_config['ham_path'] is not None:
                clf_tasks.append({
                    'train': self.ham_train,
                    'val': self.ham_val,
                    'clf': self.ham_clf,
                    'name': 'ham10000',
                })

            # isic
            if d_config['isic_path'] is not None:
                seg_tasks.append({
                    'train': self.isic_train,
                    'val': self.isic_val,
                    'dec': self.isic_dec,
                    'name': 'isic_task1',
                })

            # save the original model weights
            orig_model = copy.deepcopy(model.state_dict())

            # loop over all classification tasks and train+eval
            for task in clf_tasks:
                ds_train = task['train']
                ds_val = task['val']
                clf = task['clf']
                name = task['name']
                if ds_train is not None and ds_val is not None and clf is not None:
                    print('~' * 20 + f' {name} ' + '~' * 20)
                    # load the original weights
                    model.load_state_dict(orig_model)
                    self.eval_classification_task(ds_train,
                                                  val_loader=ds_val,
                                                  classifier=clf,
                                                  model=model,
                                                  task_name=name,
                                                  n_iter=n_iter,
                                                  fine_tune=fine_tune)

            # loop over all segmentation tasks and train+eval
            for task in seg_tasks:
                ds_train = task['train']
                ds_val = task['val']
                dec = task['dec']
                name = task['name']
                if ds_train is not None and ds_val is not None and dec is not None:
                    print('~' * 20 + f' {name} ' + '~' * 20)
                    # load the original weights
                    model.load_state_dict(orig_model)
                    self.eval_segmentation_task(ds_train,
                                                decoder=dec,
                                                model=model,
                                                backbone=backbone,
                                                task_name=name,
                                                validation=False,
                                                n_iter=n_iter)
                    self.eval_segmentation_task(ds_val,
                                                decoder=dec,
                                                model=model,
                                                backbone=backbone,
                                                task_name=name,
                                                validation=True,
                                                n_iter=n_iter)

    def _get_device(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Running on:", device)
        return device

    def _save_config_file(self, model_checkpoints_folder: Path):
        if not os.path.exists(model_checkpoints_folder):
            os.makedirs(model_checkpoints_folder)
            shutil.copy(self.config_path,
                        model_checkpoints_folder / 'config.yaml')

    def restart_from_checkpoint(self, ckp_path, run_variables=None, **kwargs):
        if not os.path.isfile(ckp_path):
            print("Pre-trained weights not found. Training from scratch.")
            return
        print("Found checkpoint at {}".format(ckp_path))

        # open checkpoint file
        checkpoint = torch.load(ckp_path, map_location="cpu")

        # key is what to look for in the checkpoint file
        # value is the object to load
        # example: {'state_dict': model}
        for key, value in kwargs.items():
            if key in checkpoint and value is not None:
                try:
                    msg = value.load_state_dict(checkpoint[key], strict=False)
                    if len(msg.missing_keys) > 0:
                        k = next(iter(checkpoint[key]))
                        if 'module.' in k:
                            print(f'=> Found `module` in {key}, trying to transform.')
                            transf_state_dict = OrderedDict()
                            for k, v in checkpoint[key].items():
                                # remove the module from the key
                                # this is caused by the distributed training
                                k = k.replace('module.', '')
                                transf_state_dict[k] = v
                            msg = value.load_state_dict(transf_state_dict,
                                                        strict=False)
                    print("=> loaded '{}' from checkpoint '{}' with msg {}".
                          format(key, ckp_path, msg))
                except TypeError:
                    try:
                        msg = value.load_state_dict(checkpoint[key])
                        print("=> loaded '{}' from checkpoint: '{}'".format(key, ckp_path))
                    except ValueError:
                        print("=> failed to load '{}' from checkpoint: '{}'".format(key, ckp_path))
            else:
                print("=> key '{}' not found in checkpoint: '{}'".format(key, ckp_path))

        # reload variable important for the run
        if run_variables is not None:
            for var_name in run_variables:
                if var_name in checkpoint:
                    run_variables[var_name] = checkpoint[var_name]

    def _save_checkpoint(self, save_dict, epoch, save_best=False):
        if is_main_process():
            filename = str(self.run_dir / 'checkpoints' /
                           'checkpoint-epoch{}.pth'.format(epoch))
            torch.save(save_dict, filename)
            print("Saving checkpoint: {} ...".format(filename))
            if save_best:
                best_path = str(self.run_dir / 'checkpoints' / 'model_best.pth')
                torch.save(save_dict, best_path)
                print("Saving current best: model_best.pth ...")

    def _log_embeddings(
        self,
        model,
        n_iter: int,
        n_items: Union[int, None] = 3_000,
        log_self_attention: bool = False,
        return_embedding: bool = False,
        **kwargs
    ) -> Union[Tuple[torch.Tensor, torch.Tensor, torch.Tensor], None]:
        # evaluate model on val set
        if is_main_process():
            model.eval()
            with torch.no_grad():
                imgs = []
                lbls = []
                embeddings = []
                entropy = []
                for i, (img, lbl) in enumerate(self.val_dataset):
                    img = img.to(self.device)
                    # get the embeddings
                    emb = self._get_embedding(model, img)
                    ent_emb = self.calculate_embedding_entropy(emb)
                    # visualize self attention if requested
                    if i == 0 and log_self_attention:
                        self._visualize_self_attention(model,
                                                       img,
                                                       n_iter,
                                                       wandb_cat='self-attention')
                    # add info to lists
                    embeddings.append(emb.cpu().numpy())
                    imgs.append(img.cpu().numpy())
                    lbls.append(lbl.cpu())
                    entropy.append(ent_emb)

            # create (concat) our embedding space
            embeddings = np.concatenate(embeddings, axis=0)
            embeddings = torch.Tensor(embeddings)
            imgs = np.concatenate(imgs, axis=0)
            imgs = torch.Tensor(imgs)

            # entropy embedding space
            ent_avg = torch.mean(torch.Tensor(entropy)[:, 0])
            ent_min = torch.mean(torch.Tensor(entropy)[:, 1])
            ent_max = torch.mean(torch.Tensor(entropy)[:, 2])
            ent_std = torch.mean(torch.Tensor(entropy)[:, 3])
            ent_med = torch.mean(torch.Tensor(entropy)[:, 4])

            # nearest neighbors
            self._visualize_nearest_neighbors(embeddings, imgs, n_iter=n_iter)

            # select only N items (otherwise the embedding logging is to slow)
            lbls = torch.cat(lbls, dim=0)
            if n_items is not None:
                embeddings = embeddings[:n_items]
                imgs = imgs[:n_items]
                lbls = lbls[:n_items]

            if return_embedding:
                return embeddings, imgs, lbls

            # log the embeddings to wandb
            imgs = [wandb.Image(x) for x in imgs]
            df_emb = pd.DataFrame(embeddings.tolist())
            emb_cols = [f"dim_{x+1}" for x in range(embeddings[0].size()[0])]
            df_emb.columns = emb_cols
            df_emb['lbls'] = lbls.tolist()
            df_emb['image'] = imgs
            cols = df_emb.columns.tolist()
            df_emb = df_emb[cols[-1:] + cols[:-1]]
            wandb.log({
                "embeddings": df_emb,
                'entropy/val_ent_avg': ent_avg,
                'entropy/val_ent_min': ent_min,
                'entropy/val_ent_max': ent_max,
                'entropy/val_ent_std': ent_std,
                'entropy/val_ent_med': ent_med,
            }, step=n_iter)

    def _visualize_self_attention(self,
                                  model: torch.nn.Module,
                                  images: torch.Tensor,
                                  n_iter: int = 0,
                                  wandb_cat: str = 'Attention'):
        if self.multi_gpu:
            model = model.module
        patch_size = self.config['model']['student']['patch_size']
        w_featmap = images.shape[-2] // patch_size
        h_featmap = images.shape[-1] // patch_size
        attentions = model.backbone.get_last_selfattention(images)
        # number of head
        nh = attentions.shape[1]
        # loop over the number of images to visualize
        for idx_img in range(self.config['imgs_to_visualize']):
            # we keep only the output patch attention
            att = attentions[idx_img, :, 0, 1:].reshape(nh, -1)
            att = att.reshape(nh, w_featmap, h_featmap)
            att = F.interpolate(att.unsqueeze(0),
                                scale_factor=patch_size,
                                mode="nearest")
            att = att[0].cpu()
            att_img = sum(att[i] * 1 / att.shape[0]
                          for i in range(att.shape[0]))
            plt.clf()
            plt.imshow(att_img, cmap='inferno')
            plt.xticks([])
            plt.yticks([])
            mean_attention = wandb.Image(att_img, caption='mean_attention')
            in_img = wandb.Image(images[idx_img], caption='input')
            # make a grid of all attention heads
            l_att = [
                wandb.Image(att[i], caption=f'head_{i}')
                for i in range(att.shape[0])
            ]
            l_att = [in_img, mean_attention] + l_att
            wandb.log({
                f'{wandb_cat}/attentions_{idx_img}': l_att,
                f'{wandb_cat}/attention_mean_{idx_img}': wandb.Image(plt),
            }, step=n_iter)

    def _visualize_nearest_neighbors(self,
                                     embeddings: torch.Tensor,
                                     imgs: torch.Tensor,
                                     n_iter: int = 0):
        cos = torch.nn.CosineSimilarity(dim=0)
        # loop over the number of images to visualize
        for idx_img in range(self.config['imgs_to_visualize']):
            cos_sim = torch.Tensor(
                [cos(x, embeddings[idx_img]) for x in embeddings])
            cos_top = torch.topk(cos_sim, 5)
            nn_imgs = [
                wandb.Image(imgs[idx], caption=f'Sim: {val}')
                for idx, val in zip(cos_top.indices, cos_top.values)
            ]
            wandb.log({
                f"NearestNeighbors/imgs_{idx_img}": nn_imgs,
            }, step=n_iter)

    def update_optim_from_schedulers(self, optimizer, lr_schedule, wd_schedule,
                                     n_iter: int):
        # update weight decay and LR according to their schedule
        # but only if wanted
        for i, param_group in enumerate(optimizer.param_groups):
            if lr_schedule is not None and self.config['use_lr_scheduler']:
                param_group["lr"] = lr_schedule[n_iter]
            if i == 0:  # only the first group is regularized
                if wd_schedule is not None and self.config['use_wd_scheduler']:
                    param_group["weight_decay"] = wd_schedule[n_iter]

    def calculate_embedding_entropy(self, embeddings: torch.Tensor):
        embeddings = (embeddings - torch.min(embeddings, dim=0).values) + 1e-7
        embedding_dist = embeddings / torch.sum(embeddings, dim=0)
        entropy_mat = torch.sum((embedding_dist * torch.log(embedding_dist)),
                                dim=0)
        ent_avg = -torch.mean(entropy_mat)
        ent_min = -torch.min(entropy_mat)
        ent_max = -torch.max(entropy_mat)
        ent_med = -torch.median(entropy_mat)
        ent_std = torch.std(entropy_mat)
        return ent_avg, ent_min, ent_max, ent_std, ent_med

    def calculate_student_teacher_acc(self, teacher_output, student_output,
                                      n_g_crops):
        # check if the outputs are tuples or not
        # if yes, use the first element (iBOT)
        if type(teacher_output) == tuple and type(student_output) == tuple:
            probs1 = teacher_output[0].chunk(n_g_crops)
            probs2 = student_output[0].chunk(n_g_crops)
        # DINO
        else:
            probs1 = teacher_output.chunk(n_g_crops)
            probs2 = student_output.chunk(n_g_crops)
        pred1 = probs1[0].max(dim=1)[1]
        pred2 = probs2[1].max(dim=1)[1]
        acc = (pred1 == pred2).sum() / pred1.size(0)
        return acc

    def ema_update_teacher(self, student, teacher, momentum_schedule, n_iter):
        # EMA update for the teacher
        with torch.no_grad():
            # momentum parameter
            m = momentum_schedule[n_iter]
            names_q, params_s, names_k, params_t = [], [], [], []
            # get student parameters
            for name_s, param_s in student.named_parameters():
                names_q.append(name_s)
                params_s.append(param_s)
            # get teacher parameters
            for name_t, param_t in teacher.named_parameters():
                names_k.append(name_t)
                params_t.append(param_t)
            # get the names (parameters) which both have in common
            names_common = list(set(names_q) & set(names_k))
            params_s = [
                param_s for name_s, param_s in zip(names_q, params_s)
                if name_s in names_common
            ]
            params_t = [
                param_t for name_t, param_t in zip(names_k, params_t)
                if name_t in names_common
            ]
            for param_s, param_t in zip(params_s, params_t):
                param_t.data.mul_(m).add_((1 - m) * param_s.detach().data)

    def check_loss_nan(self, loss):
        # check if loss is not infinite
        if not math.isfinite(loss):
            print(f"Loss is {loss}, stopping training")
            wandb.alert(title='Loss NaN',
                        text=f'Loss is {loss}, stopping training.')
            sys.exit(1)

    def check_dataset_shift_assumption(self, model, train_set, val_set, test_set, test_set2):
        self.val_dataset = train_set
        train_emb = self._log_embeddings(model=model,
                                         n_iter=0,
                                         log_self_attention=False,
                                         return_embedding=True,
                                         n_items=None)
        self.val_dataset = val_set
        val_emb = self._log_embeddings(model=model,
                                       n_iter=0,
                                       log_self_attention=False,
                                       return_embedding=True,
                                       n_items=None)
        self.val_dataset = test_set
        test_emb = self._log_embeddings(model=model,
                                        n_iter=0,
                                        log_self_attention=False,
                                        return_embedding=True,
                                        n_items=None)
        self.val_dataset = test_set2
        test2_emb = self._log_embeddings(model=model,
                                         n_iter=0,
                                         log_self_attention=False,
                                         return_embedding=True,
                                         n_items=None)
        if all(v is not None for v in [train_emb, val_emb, test_emb, test2_emb]):
            train_emb, _, _, = train_emb
            val_emb, _, _, = val_emb
            test_emb, _, _, = test_emb
            test2_emb, _, _, = test2_emb

            # define PCA for transforming the embedding space
            # into independent random variables
            pca = PCA(n_components=None)
            # compute PCA for the spaces
            train_emb = torch.Tensor(pca.fit_transform(train_emb))
            plt.plot(np.cumsum(pca.explained_variance_ratio_))
            plt.xlabel('Number of components')
            plt.ylabel('Explained Variance')
            plt.title('Explained variance TRAIN')
            plt.show()
            plt.savefig('explained_var_train.png')

            val_emb = torch.Tensor(pca.fit_transform(val_emb))
            test_emb = torch.Tensor(pca.fit_transform(test_emb))
            test2_emb = torch.Tensor(pca.fit_transform(test2_emb))

            # get min / max of each feature
            mins = torch.cat([train_emb, val_emb, test_emb, test2_emb]).min(dim=0).values
            maxs = torch.cat([train_emb, val_emb, test_emb, test2_emb]).max(dim=0).values

            div_train_val = []
            div_val_test = []
            div_train_test = []
            div_test_test = []
            for d in range(train_emb.shape[1]):
                # convert each feature dimension into normalized histogram
                # that can be used as a distrbution
                train_feat_hist = torch.histogram(
                    train_emb[:, d],
                    bins=100,
                    range=(float(mins[d].numpy()), float(maxs[d].numpy())))
                train_feat_hist = train_feat_hist.hist / train_emb.shape[0]
                train_feat_hist = torch.clip(train_feat_hist, min=1e-7, max=1)

                val_feat_hist = torch.histogram(
                    val_emb[:, d],
                    bins=100,
                    range=(float(mins[d].numpy()), float(maxs[d].numpy())))
                val_feat_hist = val_feat_hist.hist / val_emb.shape[0]
                val_feat_hist = torch.clip(val_feat_hist, min=1e-7, max=1)

                test_feat_hist = torch.histogram(
                    test_emb[:, d],
                    bins=100,
                    range=(float(mins[d].numpy()), float(maxs[d].numpy())))
                test_feat_hist = test_feat_hist.hist / test_emb.shape[0]
                test_feat_hist = torch.clip(test_feat_hist, min=1e-7, max=1)

                test2_feat_hist = torch.histogram(
                    test2_emb[:, d],
                    bins=100,
                    range=(float(mins[d].numpy()), float(maxs[d].numpy())))
                test2_feat_hist = test2_feat_hist.hist / test_emb.shape[0]
                test2_feat_hist = torch.clip(test2_feat_hist, min=1e-7, max=1)

                # KL divergence between train / val / test
                kl_train_val = (
                    train_feat_hist *
                    torch.log(train_feat_hist / val_feat_hist)).sum(dim=-1)
                kl_val_test = (
                    val_feat_hist *
                    torch.log(val_feat_hist / test_feat_hist)).sum(dim=-1)
                kl_train_test = (
                    train_feat_hist *
                    torch.log(train_feat_hist / test_feat_hist)).sum(dim=-1)
                kl_test_test = (
                    test_feat_hist *
                    torch.log(test_feat_hist / test2_feat_hist)).sum(dim=-1)

                div_train_val.append(kl_train_val)
                div_val_test.append(kl_val_test)
                div_train_test.append(kl_train_test)
                div_test_test.append(kl_test_test)

            div_train_val = torch.tensor(div_train_val)
            div_val_test = torch.tensor(div_val_test)
            div_train_test = torch.tensor(div_train_test)
            div_test_test = torch.tensor(div_test_test)
            print('*' * 20 + ' Inspect Datasets ' + '*' * 20)
            print(f'Featurewise KL divergence between TRAIN and VAL, '
                  f'mean: {div_train_val.mean()}, std: {div_train_val.std()}')
            print(f'Featurewise KL divergence between VAL and TEST, '
                  f'mean: {div_val_test.mean()}, std: {div_val_test.std()}')
            print(f'Featurewise KL divergence between TRAIN and TEST, '
                  f'mean: {div_train_test.mean()}, std: {div_train_test.std()}')
            print(f'Featurewise KL divergence between TEST and TEST2, '
                  f'mean: {div_test_test.mean()}, std: {div_test_test.std()}')

            # compare val train and test set
            t_value, p_value = stats.ttest_1samp(div_val_test,
                                                 div_train_val.mean(),
                                                 alternative='two-sided')
            print('Test statistic is %f' % float("{:.6f}".format(t_value)))
            print('p-value for two-sided test is %f' % p_value)
            alpha = 0.05

            if p_value <= alpha:
                print(f'Since p-value ({p_value}) < alpha ({alpha}),'
                      ' reject null hypothesis (train/val and test not same).')
            else:
                print(f'Since p-value ({p_value}) > alpha ({alpha}), '
                      'not rejecting null hypothesis.')

            # compare the two test sets
            t_value, p_value = stats.ttest_1samp(div_test_test,
                                                 div_train_val.mean(),
                                                 alternative='two-sided')
            print('Test statistic is %f' % float("{:.6f}".format(t_value)))
            print('p-value for two-sided test is %f' % p_value)
            alpha = 0.05

            if p_value <= alpha:
                print(f'Since p-value ({p_value}) < alpha ({alpha}),'
                      ' reject null hypothesis (the test sets are not the same).')
            else:
                print(f'Since p-value ({p_value}) > alpha ({alpha}), '
                      'not rejecting null hypothesis.')
            print('*'*40)
