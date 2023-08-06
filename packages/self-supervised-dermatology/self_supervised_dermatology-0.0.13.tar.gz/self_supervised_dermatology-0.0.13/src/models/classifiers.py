from torch import nn


class LinearClassifier(nn.Module):
    """Linear layer to train on top of frozen features"""
    def __init__(self, dim, num_labels=1000):
        super(LinearClassifier, self).__init__()
        self.num_labels = num_labels

        self.dropout = nn.Dropout(0.3)

        self.linear = nn.Linear(dim, 128)
        self.linear.weight.data.normal_(mean=0.0, std=0.01)
        self.linear.bias.data.zero_()
        self.relu = nn.ReLU()

        self.dropout2 = nn.Dropout(0.3)

        self.linear2 = nn.Linear(128, num_labels)
        self.linear2.weight.data.normal_(mean=0.0, std=0.01)
        self.linear2.bias.data.zero_()

    def forward(self, x):
        # flatten
        x = x.view(x.size(0), -1)
        # Dropout
        x = self.dropout(x)
        # 1. linear layer
        x = self.linear(x)
        x = self.relu(x)
        x = self.dropout2(x)
        # 2. linear layer
        x = self.linear2(x)
        return nn.LogSoftmax(dim=1)(x)
