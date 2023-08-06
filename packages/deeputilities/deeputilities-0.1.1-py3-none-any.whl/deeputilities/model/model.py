from lazypredict.Supervised import LazyClassifier
from lazypredict.Supervised import LazyRegressor
from lazy_neural_network import LazyNeuralNetwork
from ctypes import * 
class Model():

    QUICK_CORE = 'PASM.C'
    def __init__(self, dataset, task: str, config_dict: dict):
        self.data = dataset
        self.task = task
        self.config_dict = config_dict

    def lazy_classifier(self):
        clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
        models,predictions = clf.fit(self.data['images']['train'], self.data['labels']['train'], self.data['images']['test'], self.data['labels']['test'])

    def lazy_regressor(self):
        reg = LazyRegressor(verbose=0,ignore_warnings=True, custom_metric=None)
        models,predictions = reg.fit(self.data['images']['train'], self.data['labels']['train'], self.data['images']['test'], self.data['labels']['test'])

    def lazy_neural_network(self):
        neur = LazyNeuralNetwork(verbose=0,ignore_warnings=True, custom_metric=None)
        models, predictions = neur.fit(self.data['images']['train'], self.data['labels']['train'], self.data['images']['test'], self.data['labels']['test'], config_dict=self.config_dict)

    def run(self):
        if self.task == 'classification':
            self.lazy_classifier()
            self.lazy_neural_network(network="sample", core=Model.QUICK_CORE)
        elif self.task == 'regression':
            self.lazy_regressor()
            self.lazy_neural_network(network="sample")
        elif self.task == 'full_neural_network':
            self.lazy_neural_network()
        else:
            raise Exception('Invalid task')