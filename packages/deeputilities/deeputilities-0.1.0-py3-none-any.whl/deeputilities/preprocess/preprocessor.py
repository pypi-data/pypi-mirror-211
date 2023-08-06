from pandas_profiling import ProfileReport
import pandas as pd 
import numpy as np
from src.deeputilities.ingest.custom_dataset import CustomImageDataset

class Preprocessor():
    """ Includes EDA, data pre-processing, and cleaning."""

    def __init__(self, dataset, config_dict):
        self.dataset = dataset
        self.df = pd.DataFrame(dataset, index=None)
        self.config_dict = config_dict

    def run_preprocessing_step(self):
        profile = self.run_eda()

        if profile['WARNINGS']:
            if 'Missing values' in profile['WARNINGS'] and self.config_dict['missing_data'] == 'interpolate':
                self.run_data_interpolation() 
            elif 'Missing values' in profile['WARNINGS'] and self.config_dict['missing_data'] == 'remove':
                self.remove_missing_values()
            else:
                self.replace_missing_data()
            if 'Outliers' in profile['WARNINGS']:
                self.remove_outliers()
            if 'Duplicated' in profile['WARNINGS']:
                self.remove_duplicates()             


    def run_eda(self):
        """ Runs a pandas profiling report on the dataset."""

        profile = ProfileReport(self.df, title=f'Pandas Profiling Report for {self.dataset.name}', explorative=True)
        profile.to_file(output_file="eda_report.html")
        for idx in  len(self.df['labels']):
            if idx % 2 == 0:
                feature_weights = self.weight_feature_importance(self.df, self.df['target'])
                with open('feature_weights.txt', 'w') as f:
                    f.write(feature_weights)
        return profile

    # TODO: Implement data augmentation
    def run_data_augmentation(self):
        pass
    
    def replace_missing_data(self):
        """replace missing data values and return as pandas data frame."""

    # strip whitespace from data
        data = self.df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # replace missing values with the sentinel NaN value
        data = data.replace('?', None)

        # get missing field count
        nan_vals = dict(data.count(axis=1))
        row, cols = data.shape
        nan_vals = {key: value for (key, value) in nan_vals.items() if value < cols-2}

        # remove samples with more than one missing field
        data = data.drop(index=nan_vals.keys())

        return data

    def run_data_interpolation(self, real, discrete):
            # get mean of real-valued fields and mode for categorical fields
        mode = self.df.mode().values.flatten()
        mean = self.df.mean().values.flatten()

        # keep ONLY the categorical modes
        mode = [x for x in mode.copy() if type(x) == str]

        replacements = list(np.zeros(15))

        # get mean replacements for continuous fields
        j = 0
        for index in real:
            replacements[index] = mean[j]
            j += 1

        # get mode replacements for discrete fields
        j = 0
        for index in discrete:
            replacements[index] = mode[j]
            j += 1

        # fill NaN values with mode (discrete fields) and mean (continuous fields)
        data = self.df.fillna(pd.Series(replacements))

        return data

    def remove_missing_values(self):
        self.df.dropna(axis=0, how='any', inplace=True)

    def remove_outliers(self):
            # get field mean and std for real-valued fields
        mean = data.describe().iloc[1, :]
        std = data.describe().iloc[2, :]

        # remove outliers
        for (real, mean, std) in zip(real, mean, std):
            data = data[data[real] < 3*std + mean]

        return data


    def weight_feature_importance(x, y):
        """Calculate the Modified T-score for each feature. Bigger values mean
        more important features.
        Parameters
        ----------
        x : array-like, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The classes for the samples. There can be only 2 classes.
        Returns
        -------
        array-like, shape (n_features,) : feature scores


        """
        classes = np.unique(y)

        size_class0 = y[y == classes[0]].size
        size_class1 = y[y == classes[1]].size

        mean_class0 = np.mean(x[y == classes[0]], axis=0)
        mean_class0 = np.nan_to_num(mean_class0)
        mean_class1 = np.mean(x[y == classes[1]], axis=0)
        mean_class1 = np.nan_to_num(mean_class1)

        std_class0 = np.std(x[y == classes[0]], axis=0)
        std_class0 = np.nan_to_num(std_class0)
        std_class1 = np.std(x[y == classes[1]], axis=0)
        std_class1 = np.nan_to_num(std_class1)

        corr_with_y = np.apply_along_axis(
            lambda feature: abs(np.corrcoef(feature, y)[0][1]), 0, x)
        corr_with_y = np.nan_to_num(corr_with_y)

        corr_with_others = abs(np.corrcoef(x, rowvar=False))
        corr_with_others = np.nan_to_num(corr_with_others)

        mean_of_corr_with_others = (
                                        corr_with_others.sum(axis=1)
                                        - corr_with_others.diagonal()) / (len(corr_with_others) - 1)

        t_score_numerator = abs(mean_class0 - mean_class1)
        t_score_denominator = np.sqrt(
            (size_class0 * np.square(std_class0) + size_class1 * np.square(
                std_class1)) / (size_class0 + size_class1))
        modificator = corr_with_y / mean_of_corr_with_others

        t_score = t_score_numerator / t_score_denominator * modificator
        t_score = np.nan_to_num(t_score)

        return t_score



