# system level
import sys
import json
import os
import codecs

# arrays
import numpy as np
from numpy import random
from scipy import interp

# keras
import tensorflow as tf
from keras.models import model_from_json
from keras.utils import np_utils
from keras import backend as K
from keras import models

# sklearn (for machine learning)
from sklearn import metrics
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import confusion_matrix
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import brier_score_loss
from sklearn.decomposition import PCA

from scipy.stats import sem

#model plotting
import pydotplus
import keras.utils

# plotting
from matplotlib import pyplot as plt
import pylab as pl
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
import matplotlib.patches as mpatches
# from vis.visualization import visualize_cam
# from vis.utils import utils
from sklearn.metrics import precision_recall_curve


class Diagnosis():

    def __init__(self, dataset):
        self.data = dataset

    def examples_plot(images, nrows, ncols, name=False):#WORKS
    # ------------------------------------------------------------------------------
    # Funciton plots images given in examples
    # ------------------------------------------------------------------------------
        from matplotlib.colors import LogNorm
        folder = "images/"
        fig1=plt.figure(figsize=(5,5))
        for i, image in enumerate(images):
            plt.subplot(nrows, ncols, i + 1)
            plt.axis("off")
            plt.imshow(image, aspect='auto', cmap='viridis', norm=LogNorm())
        plt.subplots_adjust(hspace=0, wspace=0)
        plt.show()
        if name==False:
            fig1.savefig('images/example.pdf')
        else:
            fig1.savefig(folder+name)   
        return



    def load_plot_model(json_file):#WORKS
    # ------------------------------------------------------------------------------
    # Funciton loads model architecture and plots it
    # ------------------------------------------------------------------------------
        json_file = open(json_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        keras.utils.vis_utils.pydot = pydotplus
        keras.utils.plot_model(loaded_model, to_file='images/model.pdf', show_shapes=True)
        return loaded_model



    def true_pred (y_test, y_prob):#WORKS!
    # ------------------------------------------------------------------------------
    # Function plots true labels vs predictions for train, validaiton and test set
    # ------------------------------------------------------------------------------
        fig, axis1 = plt.subplots(figsize=(8,8))
        plt.scatter(y_test, y_prob, label='test')
        plt.plot([0,1], [0,1], 'k--', label="1-1")
        plt.xlabel("Truth")
        plt.ylabel("Prediction")
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig('images/true_pred.pdf') 


    def loss_acc_plot_novalidation(loss, acc):#WORKS!
    # ------------------------------------------------------------------------------
    # Funciton plots a combined loss and accuracy plot for training and validation set
    # ------------------------------------------------------------------------------
        epochs_list = list(range(len(loss)))

        figsize=(6,4)
        fig, axis = plt.subplots(figsize=figsize)
        plot_acc = axis.plot(epochs_list, acc, 'navy', label='accuracy')

        plot_loss = axis.plot(epochs_list, loss, 'red', label='loss')

        axis.set_xlabel('Epoch')
        axis.set_ylabel('Loss/Accuracy')
        plt.tight_layout()
        axis.legend(loc='center right')
        plt.savefig('images/loss_acc.pdf')
        


    def loss_acc_plot(loss, val_loss, acc, val_acc):#WORKS!
    # ------------------------------------------------------------------------------
    # Funciton plots a combined loss and accuracy plot for training and validation set
    # ------------------------------------------------------------------------------
        epochs_list = list(range(len(loss)))

        figsize=(6,4)
        fig, axis = plt.subplots(figsize=figsize)
        plot_lacc = axis.plot(epochs_list, acc, 'navy', label='accuracy')
        plot_val_lacc = axis.plot(epochs_list, val_acc, 'deepskyblue', label="validation accuracy")

        plot_loss = axis.plot(epochs_list, loss, 'red', label='loss')
        plot_val_loss = axis.plot(epochs_list, val_loss, 'lightsalmon', label="validation loss")

        axis.set_xlabel('Epoch')
        axis.set_ylabel('Loss/Accuracy')
        plt.tight_layout()
        axis.legend(loc='center right')
        plt.savefig('images/loss_acc.pdf')
        



    def prec_recall_plot(y_test, probability):#WORKS!
    # ------------------------------------------------------------------------------
    # Funciton plots a combined precision and recall plot for training and validation set
    # ------------------------------------------------------------------------------
        precision, recall, thresholds = precision_recall_curve(y_test, probability)
        AUC = auc(recall, precision)

        figsize=(6,4)
        plt.plot(precision, recall, 'r')

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.tight_layout()
        plt.savefig('images/prec_recall.pdf')
        return AUC


    def conf_matrix(y_true, y_pred, normalize=False, cmap=plt.cm.Blues):#WORKS!
    # ------------------------------------------------------------------------------
    # Outputs the confusion matrix for arbitrary number of classes
    # ------------------------------------------------------------------------------
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        #if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        # Only use the labels that appear in the data
        classes = unique_labels(y_true, y_pred)


        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.figure.colorbar(im, ax=ax)
        # We want to show all ticks...
        ax.set(xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            # ... and label them with the respective list entries
            xticklabels=classes, yticklabels=classes,
            title=title,
            ylabel='True label',
            xlabel='Predicted label')
        ax.set_ylim(len(classes)-0.5, -0.5)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        fig.tight_layout()
        plt.savefig('images/conf.pdf')

    def isomap_analysis(samples_array, n_neighbors=5, n_components=.95):
        iso_50 = PCA(n_components=.95)
        iso_result = iso_50.fit_transform(samples_array)

        return iso_result

    def plot_tsne(xy, colors=None, alpha=0.25, figsize=(6,6), s=0.5, cmap='hsv'):
        plt.figure(figsize=figsize, facecolor='white')
        plt.margins(0)
        plt.axis('off')
        fig = plt.scatter(xy[:,0], xy[:,1],
                    color=colors, # set colors of markers
                    cmap=cmap, # set color map of markers
                    alpha=alpha, # set alpha of markers
                    # marker=',', # use smallest available marker (square)
                    s=s, # set marker size. single pixel is 0.5 on retina, 1.0 otherwise
                    lw=0, # don't use edges
                    edgecolor='') # don't use edges
        # remove all axes and whitespace / borders
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.show()
        plt.savefig("figure.png")

