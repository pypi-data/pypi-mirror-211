# Settings, mostly for environment variables.
import os 
import torchvision.models as models

# ENVIRONMENT VARIABLES
# ---------------------
GCP_KEY = os.getenv("GCP_KEY", "public-key-goes-here.json")

# NEURAL ARCHITECTURES
# --------------------
RESNET_18 = models.resnet18(pretrained=True)
ALEXNET = models.alexnet(pretrained=True)
SQUEEZENET = models.squeezenet1_0(pretrained=True)
VGG16 = models.vgg16(pretrained=True)
DENSENET = models.densenet161(pretrained=True)
INCEPTION = models.inception_v3(pretrained=True)
GOOGLENET = models.googlenet(pretrained=True)
SHUFFLENET = models.shufflenet_v2_x1_0(pretrained=True)
MOBILENET = models.mobilenet_v2(pretrained=True)
RESNEXT50_32x4d = models.resnext50_32x4d(pretrained=True)
WIDE_RESNET50_2 = models.wide_resnet50_2(pretrained=True)
MNASNET = models.mnasnet1_0(pretrained=True)

# CONFIG DEFAULTS
# ---------------
CONFIG_DICT_DEFAULT = {
    "DATA": {
        "CONFIGURATION": 1,
        "DATA_PATH": "default/path",
        "LABEL_PATH": "default/path"
    },
    "MODEL_DATA": {
        "USER_MODEL": "some-model",
        "BASE_MODEL": "some-model-of-utils",
        "TASK_TYPE": "classification"
    },
    "MODEL_PARAMS": {
        "BATCH_SIZE": 32,
        "LEARNING_RATE": 0.5,
        "OPTIMIZER": "optimizer" 
    },
    "OUTPUT": {
        "OUTPUT_PATH": "output/path"
    }
}

# Data Input Sources 
USER_DATA_CONFIGS = [
    "LABELLED_W_ANNOTATIONS", #0
    "LABELLED_W_FOLDERS", #1
    "NUMPY", #2...
    "UNLABELLED",
    "DEEPBENCH",
    "DEEPGOTDATA",
    "H5",
]

EXAMPLE_DATA_CONFIGS = [
    "MNIST",
    "CIFAR10",
    "FMNIST",
]

# Configuration Templates available
CONFIG_TEMPLATE_TYPES = [
    "ALL",
    "UTILS",
    "BENCH",
    "GOTDATA"
]

# DEFAULT PATHS
OUTPUT_PATH = f"{os.getcwd()}/deep_utilities/"
CONFIG_PATH = f"{OUTPUT_PATH}config_files/"