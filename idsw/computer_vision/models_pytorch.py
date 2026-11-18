"""
idsw.computer_vision.models_pytorch
===================================
Deep Learning computer vision models using PyTorch and Torchvision:
- Custom PyTorch CNN architectures
- Transfer learning with Torchvision backbones (ResNet, MobileNet)
- Siamese neural networks for one-shot learning and image similarity
"""

import numpy as np

from idsw import InvalidInputsError, ControlVars


def build_cnn_classifier_pytorch(num_classes = 2, in_channels = 3):
    """
    build_cnn_classifier_pytorch:
    Constructs a PyTorch Convolutional Neural Network module.

    : param: num_classes: integer, number of target classes.
    : param: in_channels: integer (default 3 for RGB, 1 for grayscale).
    : return: torch.nn.Module instance.
    """
    try:
        import torch
        import torch.nn as nn

        class IDSWPyTorchCNN(nn.Module):
            def __init__(self, n_classes, channels):
                super().__init__()
                self.features = nn.Sequential(
                    nn.Conv2d(channels, 32, kernel_size = 3, padding = 1),
                    nn.BatchNorm2d(32),
                    nn.ReLU(inplace = True),
                    nn.MaxPool2d(kernel_size = 2, stride = 2),

                    nn.Conv2d(32, 64, kernel_size = 3, padding = 1),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace = True),
                    nn.MaxPool2d(kernel_size = 2, stride = 2),

                    nn.AdaptiveAvgPool2d((4, 4))
                )
                self.classifier = nn.Sequential(
                    nn.Flatten(),
                    nn.Dropout(0.3),
                    nn.Linear(64 * 4 * 4, 128),
                    nn.ReLU(inplace = True),
                    nn.Dropout(0.3),
                    nn.Linear(128, n_classes)
                )

            def forward(self, x):
                x = self.features(x)
                x = self.classifier(x)
                return x

        model = IDSWPyTorchCNN(num_classes, in_channels)

        if ControlVars.show_results:
            print("=" * 80)
            print("PYTORCH CNN CLASSIFIER BUILT SUCCESSFULLY")
            print("=" * 80)

        return model

    except ImportError:
        raise InvalidInputsError("PyTorch is not installed. Run: pip install torch torchvision")


def apply_transfer_learning_pytorch(base_model_name = 'resnet18', num_classes = 2, freeze_base = True):
    """
    apply_transfer_learning_pytorch:
    Constructs a PyTorch transfer learning model using a pre-trained Torchvision backbone.

    : param: base_model_name: 'resnet18', 'resnet50', or 'mobilenet_v2'.
    : param: num_classes: number of output classes.
    : param: freeze_base: whether to freeze the backbone layers.
    : return: torch.nn.Module.
    """
    try:
        import torch
        import torch.nn as nn
        import torchvision.models as models

        name = str(base_model_name).strip().lower()

        if name == 'resnet18':
            model = models.resnet18(weights = models.ResNet18_Weights.DEFAULT)
            in_features = model.fc.in_features
            if freeze_base:
                for param in model.parameters():
                    param.requires_grad = False
            model.fc = nn.Linear(in_features, num_classes)

        elif name == 'resnet50':
            model = models.resnet50(weights = models.ResNet50_Weights.DEFAULT)
            in_features = model.fc.in_features
            if freeze_base:
                for param in model.parameters():
                    param.requires_grad = False
            model.fc = nn.Linear(in_features, num_classes)

        elif name == 'mobilenet_v2':
            model = models.mobilenet_v2(weights = models.MobileNet_V2_Weights.DEFAULT)
            in_features = model.classifier[1].in_features
            if freeze_base:
                for param in model.parameters():
                    param.requires_grad = False
            model.classifier[1] = nn.Linear(in_features, num_classes)

        else:
            raise InvalidInputsError(f"Unsupported backbone '{base_model_name}'. Choose from: 'resnet18', 'resnet50', 'mobilenet_v2'.")

        if ControlVars.show_results:
            print(f"PyTorch transfer learning model instantiated with {base_model_name} (freeze = {freeze_base}).")

        return model

    except ImportError:
        raise InvalidInputsError("Torchvision is not installed. Run: pip install torchvision")


def build_siamese_network_pytorch(embedding_dim = 128, in_channels = 3):
    """
    build_siamese_network_pytorch:
    Builds a Siamese Neural Network in PyTorch with twin subnetworks sharing identical weights.
    Outputs Euclidean or Cosine distance embeddings for one-shot learning and image verification.

    : param: embedding_dim: dimension of the latent feature representation.
    : param: in_channels: number of input image channels.
    : return: torch.nn.Module instance.
    """
    try:
        import torch
        import torch.nn as nn

        class SiameseTwinNetwork(nn.Module):
            def __init__(self, emb_dim, channels):
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Conv2d(channels, 32, kernel_size = 3, padding = 1),
                    nn.ReLU(inplace = True),
                    nn.MaxPool2d(2, 2),
                    nn.Conv2d(32, 64, kernel_size = 3, padding = 1),
                    nn.ReLU(inplace = True),
                    nn.AdaptiveAvgPool2d((4, 4)),
                    nn.Flatten(),
                    nn.Linear(64 * 4 * 4, emb_dim)
                )

            def forward_one(self, x):
                return self.encoder(x)

            def forward(self, input1, input2):
                output1 = self.forward_one(input1)
                output2 = self.forward_one(input2)
                # Compute Euclidean distance
                distance = torch.norm(output1 - output2, p = 2, dim = 1)
                return output1, output2, distance

        model = SiameseTwinNetwork(embedding_dim, in_channels)

        if ControlVars.show_results:
            print(f"PyTorch Siamese Twin Network constructed with embedding dimension {embedding_dim}.")

        return model

    except ImportError:
        raise InvalidInputsError("PyTorch is not installed. Run: pip install torch torchvision")
