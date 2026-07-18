import torch
import torch.nn as nn

class FlexibleCNN(nn.Module):
    def __init__(self, n_layers, n_filters, kernel_sizes, batch_size, dropout_rate, fc_size, num_classes):
        super(FlexibleCNN, self).__init__()
        
        blocks = []
        in_channels = 3
        self.num_classes = num_classes
        
        for i in range(n_layers):
            out_channels = n_filters[i]
            kernel_size = kernel_sizes[i]
            padding = (kernel_size - 1) // 2
            block = nn.Sequential(
                nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, padding=padding),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2)
            )
            
            blocks.append(block)
            in_channels = out_channels
        
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.features = nn.Sequential(*blocks)
        self.dropout_rate = dropout_rate
        self.fc_size = fc_size
        self.classifier = None
        
    def create_classifier(self, flatten_size, device):
        self.classifier = nn.Sequential(
            nn.Dropout(p=self.dropout_rate),
            nn.Linear(flatten_size, self.fc_size),
            nn.ReLU(),
            nn.Dropout(p=self.dropout_rate),
            nn.Linear(self.fc_size, self.num_classes)
        ).to(device)
    
    def forward(self, x):
        device = x.device
        x = self.features(x)
        x = self.adaptive_pool(x)
        
        flatten = torch.flatten(x, 1)
        flatten_size = flatten.size(1)
        if self.classifier is None:
            self.create_classifier(flatten_size, device)
        
        return self.classifier(flatten)


def fine_tuning_stage1(model, model_name, num_classes):
    if model_name == "ResNet18":
        for param in model.parameters():
            param.requires_grad = False
        
        original_fc = model.fc
        in_features = original_fc.in_features
        new_fc = nn.Linear(in_features, num_classes)
        model.fc = new_fc
        print(f"Original FC: {original_fc}")
        print(f"New FC: {new_fc}")
    
    elif model_name == "MobileNet":
        for param in model.features.parameters():
            param.requires_grad = False
        
        original_fc = model.classifier[-1]
        in_features = original_fc.in_features
        new_fc = nn.Linear(in_features, num_classes)
        model.classifier[-1] = new_fc
        
        print(f"Original FC: {original_fc}")
        print(f"New FC: {new_fc}")
    
    else:
        print("Error: This model is not available.")
    
    return model


def fine_tuning_stage2(fine_tuned_model, model_name):
    if model_name == "ResNet18":
        for param in fine_tuned_model.layer4.parameters():
            param.requires_grad = True
            
    elif model_name == "MobileNet":
        for param in fine_tuned_model.features[-1].parameters():
            param.requires_grad = True
            
    else:
        print("Error: This model is not available.")
    
    return fine_tuned_model