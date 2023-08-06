from torch.utils.data.dataset import Dataset

class CustomImageDataset(Dataset):

    def __init__(self, data, annotations, transform):
        pass

    def __len__(self):
        
        return len(self.annotations)
    
    def __getitem__(self):
        pass