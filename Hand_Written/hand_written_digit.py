import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn

class H_digit_Object:
    
    def __init__(self):

        self.transform = transforms.Compose([
            transforms.Resize((144, 144)),               # Resize to 144x144
            transforms.Grayscale(num_output_channels=1), # Convert image to grayscale
            transforms.ToTensor(),                       # Convert to Tensor
            transforms.Normalize([0.5], [0.5])           # Normalize for grayscale
        ])
        

        self.digits_model = models.resnet18(weights='IMAGENET1K_V1')
        self.digits_model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)  
        num_ftrs = self.digits_model.fc.in_features
        self.digits_model.fc = nn.Linear(num_ftrs, 21)  
        
        # Load the trained model weights
        self.digits_model.load_state_dict(torch.load('models/digits_model.pth', map_location=torch.device('cpu')))
        self.digits_model.eval() 
        
        # Define the class names 
        self.digits_class_names = ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', 
                                   '18', '19', '2', '20', '3', '4', '5', '6', '7', '8', '9']