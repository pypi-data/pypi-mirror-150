import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from boruta import BorutaPy
from paml.searches.wrapper_catboost import CatBoostClassifierScikit, CatBoostRegressorScikit
import warnings


class FeatureSelector(TransformerMixin):
    '''Custom feature selection class using BorutaPy'''
    def __init__(self, params, task):
        self.params = params
        self.task = task

    def fit(self, X, y):
        self.accept = []
        
        if self.task == 'regression':
            self.selector = BorutaPy(estimator=RandomForestRegressor(max_depth=self.params['max_depth'], n_jobs=-1),
                                    n_estimators='auto')
        elif self.task == 'classification':
            self.selector = BorutaPy(estimator=RandomForestClassifier(max_depth=self.params['max_depth'], n_jobs=-1),
                                    n_estimators='auto')

        numeric_features = [col for col in X.columns if is_numeric_dtype(X[col]) or np.all(X[col].str.isnumeric())]
        if numeric_features:
            X_boruta = X[numeric_features]

            self.selector.fit(X_boruta.values, y)
            self.accept = X_boruta.columns[self.selector.support_].to_list()
        return self

    def transform(self, X, y=None):
        cat_features = [col for col in X.columns if X[col].dtypes  == 'object']      
        final_df = None
        # cat_features_index = [X.columns.get_loc(x) for x in X.columns if X[x].dtypes == 'object']
        if self.accept:
            if cat_features:
                final_df = X.loc[:, self.accept]
                final_df[cat_features] = X[cat_features].copy()
            else:
                final_df = X.loc[:, self.accept] 
            return final_df
        else:
            return X


class Estimator(BaseEstimator):
    warnings.filterwarnings("ignore")

    '''Custom Estimator Class for fitting and predicting models on Pipelines'''
    def __init__(self, model):
        self.model = model

    def fit(self, X, y=None):
        if type(X) == np.ndarray:
            X = pd.DataFrame(X)
        # if not (isinstance(self.model, CatBoostClassifierScikit) or isinstance(self.model, CatBoostRegressorScikit)):
        #     X = pd.get_dummies(data = X, drop_first = True)
        return self.model.fit(X, y)

    def predict(self, X):
    
        if type(X) == np.ndarray:
                X = pd.DataFrame(X)
                
        numeric_features = [col for col in X.columns if is_numeric_dtype(X[col]) or np.all(X[col].str.isnumeric())]

        if numeric_features:
            for col in X[numeric_features].columns.copy():
            #    X.loc[:][col] = X.loc[:,col].astype('float')
                X.loc[:, col] = X[col].copy().astype('float64')


        if not (isinstance(self.model, CatBoostClassifierScikit) or isinstance(self.model, CatBoostRegressorScikit)):
            X = pd.get_dummies(X, drop_first=True)
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    
    def get_estimator(self):
        return self.model


class CustomImputer:

    '''Custom Imputation class for imputing missing data, imputes mean for real data and most frequent 
    categorical data'''
    def __init__(self):
        pass
    def fit( self, X, y = None):
        if type(X) == np.ndarray:
            X = pd.DataFrame(X)
            X = X.convert_dtypes(convert_integer=True, convert_string = False)
            numeric_features_index = [X.columns.get_loc(col) for col in X.columns if is_numeric_dtype(X[col]) or np.all(X[col].str.isnumeric())]
            if numeric_features_index:
                for feat in X.columns:
                    if feat in X.columns[numeric_features_index]:
                        # X.loc[:][feat] = X[feat].astype('float64')
                        X.loc[:, feat] = X[feat].copy().astype('float64')





        self.fill_values = pd.Series([X[column].value_counts().index[0] 
                                if X[column].dtype == np.dtype('O') and  X[column].isnull().sum() == len(X[column])
                                else  0 if X[column].isnull().sum() == len(X[column]) 
                                        else X[column].mean() if X[column].dtype != np.dtype('O') else X[column].value_counts().index[0] 
                                            for column in X.columns], index = X.columns)

        return self

    def transform(self, X, y=None):
        if type(X) == np.ndarray:
            X = pd.DataFrame(X)
            X = X.convert_dtypes(convert_integer=True, convert_string = False)
        numeric_features_index = [X.columns.get_loc(x) for x in X.columns if is_numeric_dtype(X[x]) or np.all(X[x].str.isnumeric())]
        if numeric_features_index:
            for feat in X.columns.copy().values:
                if feat in X.columns[numeric_features_index].copy():
                    X.loc[:, feat] = X[feat].copy().astype('float64')
                    # X.loc[:][feat] = X[feat].astype('float64')

        return X.fillna(self.fill_values)

    def fit_transform(self, X, y = None):
        self.fit(X)
        return self.transform(X)


class GetDummiesTransformer(TransformerMixin):  
    def __init__(self) -> None:
        self.training_columns = None
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X, y = None):
       
        cats = [col for col in X.columns if X[col].dtypes == 'object']
        X = pd.get_dummies(X, drop_first=True, columns = cats)
        if not np.any(self.training_columns):
            self.training_columns = X.columns
        else:
            missing_cols = set(self.training_columns) - set(X.columns )

            for col in missing_cols:
                X[col] = 0
            X = X[self.training_columns]
        
        return X