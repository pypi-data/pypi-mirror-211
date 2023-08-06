# import deepbench
# import deepgotdata
# ^ Add these git links to poetry.
import torch
from stand_in_pkg.deepbench import Catalogue
from stand_in_pkg.deepgotdata import GotDataPull
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader, random_split
from settings import GCP_KEY
from typing import Union, List
from custom_dataset import CustomImageDataset
from math import floor
import os
from glob import iglob
from preprocess.preprocessor import Preprocessor

class Ingestor():

    def __init__(self, config_dict: dict, gcp_key:str=GCP_KEY):

        self.gcp_key = gcp_key
        self.config_dict = config_dict

    # Ingests some user data based on the configuration variable. Make the data configuration an enum type somewhere.
    def ingest_user_data(self, file_path: Union[dict, str], data_configuration: str, bench_dict: dict=None, gotdata_dict: dict=None):
        """ Ingests user data based on the configuration variable. Make the data configuration an enum type somewhere."""
        transform = transforms.ToTensor()

        if data_configuration == 'LABELLED_IMAGE_FOLDERS':

            labels = self.onehot_labels_from_folder_names(file_path)

            img_dataset = CustomImageDataset(annotations_file=labels, img_dir=file_path, transform=transform, shuffle=True)
        elif data_configuration == 'LABELLED_IMAGE_CSV':
        
            if type(file_path) == 'dict':
                self.__check_path_exists___(file_path['labels'])
                self.__check_path_exists___(file_path['images'])
            else:
                pass
            
            img_dataset = CustomImageDataset(annotations_file=file_path['labels'], img_dir=file_path['images'], transform=transform, shuffle=True)
        elif data_configuration == 'LABELLED_NUMPY':

            if type(file_path) == 'dict':
                self.__check_path_exists___(file_path['labels'])
                self.__check_path_exists___(file_path['images'])
            else:
                raise ValueError(f"Please provide a dictionary with the keys 'labels' and 'images' for the file paths to the labels and images respectively.")
            
            img_dataset = CustomImageDataset(annotations_file=file_path['labels'], img_dir=file_path['images'], transform=transform, shuffle=True)

        elif data_configuration == 'UNLABELLED':
            self.__check_path_exists___(file_path)
            img_dataset = CustomImageDataset(annotations_file=None, img_dir=file_path, transform=transform, shuffle=True)

        elif data_configuration == 'DEEPBENCH':
            img_dataset = self.initialize_bench_data(n_obj=bench_dict['n_obj'], pix_dim=bench_dict['pix_dim'], data_type=bench_dict['data_type'], image_type=bench_dict['image_type'], data_path=bench_dict['data_path'])

        elif data_configuration == 'DEEPGOTDATA':
            img_dataset = self.load_deepgot_data(gotdata_dict['data_name'], gotdata_dict['data_type'], gotdata_dict['data_path'])
        else:
            raise ValueError(f"Data configuration {data_configuration} is not supported. Please choose from 0, 1, 2, 3 for the data configuration.")
        
        preprocess = Preprocessor(dataset=img_dataset, config_dict=self.config_dict)
        train_set, test_set = random_split(img_dataset, [floor(len(labels)*.7), floor(1-len(labels)*7)])
        train_loader, test_loader = self.get_general_dataloader(train_set, test_set)

        return train_loader, test_loader


    def load_example_data(self, data_name: str):
        transform = transforms.ToTensor()

        if data_name == "MNIST":
            train_set, test_set = self.get_mnist_dataset(transform=transform)
        elif data_name == "CIFAR":
            train_set, test_set = self.get_cifar_dataset(transform=transform)
        elif data_name == "FMNIST":
            train_set, test_set = self.get_fashion_mnist_dataset(transform=transform)
        else:
            raise ValueError(f"Data name {data_name} is not supported. Please choose from mnist, cifar, fashion-mnist for the example data, or use DeepBench, DeepGotData, or your own data")

        train_loader, test_loader = self.get_general_dataloader(train_set, test_set)

        return train_loader, test_loader
    
    def get_general_dataloader(self, train_set, test_set):

        train_loader = DataLoader(train_set, batch_size=self.config_dict["MODEL_PARAMS"]["TRAIN_BATCH_SIZE"], shuffle=self.config_dict["MODEL_PARAMS"]["SHUFFLE"])
        test_loader = DataLoader(test_set, batch_size=self.config_dict["MODEL_PARAMS"]["TEST_BATCH_SIZE"], shuffle=self.config_dict["MODEL_PARAMS"]["SHUFFLE"])

        return train_loader, test_loader


    def get_mnist_dataset(self, transform, data_path: Union[None, str]="./data"):

        train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        test_set = datasets.MNIST(root='./data', train=False, transform=transform)

        return train_set, test_set

    def get_cifar_dataset(self, transform, data_path: Union[None, str]="./data"):

        train_set = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
        test_set = datasets.CIFAR10(root='./data', train=False, transform=transform)

        return train_set, test_set

    def get_fashion_mnist_dataset(self, transform, data_path: Union[None, str]="./data"):

        train_set = datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
        test_set = datasets.FashionMNIST(root='./data', train=False, transform=transform)

        return train_set, test_set
    
    # Creates some data using DeepBench.
    def initialize_bench_data(self, n_obj: int, pix_dim: int, data_type: str, image_type: str, data_path: Union[None, str]="./data"):

        catalogue = Catalogue(n_obj, pix_dim, data_type, image_type, data_path=data_path)
        labels, _ = catalogue.get_catalogue()

        bench_dataset = CustomImageDataset(annotations_file=labels, image_dir=data_path + "/images", transform=transforms.ToTensor())

        return bench_dataset

    # Loads data from the DeepGotData Google database.
    def load_deepgot_data(self, data_path: Union[None, str]="./data"):
        
        catalogue = GotDataPull(self.gcp_key, data_path=data_path)
        labels, data = catalogue.pull_data_by_id()

        if catalogue.__check_data_type__(data):
            got_dataset = CustomImageDataset(annotations_file=labels, image_dir=data_path + "/images", transform=transforms.ToTensor())
        else:
            raise ValueError("Data type is not supported. Please use a supported data type apart of the following set: jpeg, png, or numpy.")
        
        return got_dataset

    def onehot_labels_from_folder_names(self, data_path: str):
        
        labels_by_image_name = []
        rootdir_glob = f'{data_path}./**' 
        label_list = [f for f in iglob(rootdir_glob, recursive=True) if os.path.isdir(f)]

        for label in label_list:
            for file in os.listdir(label):
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    labels_by_image_name.append([file, label])

        return labels_by_image_name

    def __check_path_exists___(self, path: str):
        
        if os.path.exists(path):
            return True
        else:
            raise FileNotFoundError(f"Path {path} does not exist. Please check the path and try again.")