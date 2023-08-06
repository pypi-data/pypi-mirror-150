import pandas as pd
import shap
import time

class Explainer:

    def __init__(self, data, model, preprocess = False, cols = None):
        #Creating a Shap TreeExplainer instance for explaining the dataset
        self.data = data
        self.model = model
        self.cols = cols
        start = time.time()
        print('Initializing Shap TreeExplainer')
        self.explainer = shap.TreeExplainer(self.model)
        print('Command took {} seconds'.format(time.time() - start))
        
        if preprocess  == True:
            assert cols != None and len(cols) > 0, "Please provide the features to be explained as a list for preprocess = True"
            self.preprocess_data(cols)

    def preprocess_data(self, cols):
        #trim data in dataset not in model (for sklearn based models)
        print('Preprocessing data')
        start = time.time()
        self.data = self.data[cols]

        # Re-order data
        self.data = self.data.reindex(columns = cols)
        print('Command took {} seconds'.format(time.time() - start))

    def impute_data(self, imputed_features, impute_val):
        #Imputing missing features with imputed value
        print('Imputing data')
        start = time.time()
        for col in imputed_features:
            self.data.loc[self.data[col] == 0.0 , col] = impute_val

        print('Command took {} seconds'.format(time.time() - start))
        return self.data

    def get_shap_values(self, interpretable_features, impute = False, imputed_features = None, impute_val = -1.0):
        #Computing Shap values using marginal contributions of features
        if impute == True:
            assert imputed_features != None and len(imputed_features) > 0, "Please provide the features to be imputed as a list for impute = True"
            self.data = self.impute_data(imputed_features, impute_val)


        print('Get Shap values of dataset')
        start = time.time()
        shap_values = self.explainer(self.data, check_additivity = False)
        print('Command took {} seconds'.format(time.time() - start))

        shap_df = pd.DataFrame(shap_values.values, columns = self.cols)
        shap_df = shap_df[interpretable_features]
        return shap_df
