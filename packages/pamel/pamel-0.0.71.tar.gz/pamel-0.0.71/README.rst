## How to install?

	-The package is installed in PyPi repository. To install it use the command line: 

	-pip install -i https://test.pypi.org/simple/     pamel==0.0.50

## How to import the package?

	-import paml

	-from paml import AutoML

## How to instantiate the main class?

	-You can instantiate the class passing only the parameters task  (it is a mandatory parameter)

	-E.g.s: my_automl = AutoML(search='GridSearchCV’, task = ‘classification’)

	-Available tasks are: regression and classification

	-Available searches are: GridSearch, GridSearchCV, OptunaSearch

	-You can instantiate passing the parameters: task, search, models, compute_ks, n_folds, feature_selection, acception_rate, n_trials and n_jobs.

## Parameterization definitions:

class AutoML(task: str, search_space = None, search: str = 'GridSearch', models=['all'],
                 compute_ks: bool = False, n_folds: int = 5, feature_selection = False, fs_params={'max_depth': [5]},
                 acceptance_rate: float = 0.01, 
                 n_trials: int = 10, 
                 n_jobs: int = -1):

## Parameters

** task:** - Machine Learning task, it can be ‘regression’ or ‘classification’

**search_space:** list Default None - The parameter search_space for one or more models. The correct syntax for one model is:

     #Search space example for xgb classifier
                        [{'estimator': ['xgb'],
                        'n_estimators':[1500],
                        'use_label_encoder': [False],
                        'eta': list(np.linspace(0, 0.6, 3, dtype=float)),
                        'gamma':list(np.linspace(0, 0.3, 3,  dtype=float)),
                        'use_label_encoder': [False],
                        'objective': ['binary:logistic'],
                        'n_estimators': [300, 500],
                        'eval_metric': ["logloss"],
                        'seed': [42],
                        'learning_rate': np.linspace(1e-5, 0.01, 3),
                        'gamma': np.linspace(0, 1, 2),
                        'max_depth':np.arange(3, 10, 2),
                        'min_child_weight': [1],
                        'subsample': np.linspace(0.5, 1, 3),
                        'colsample_bytree': np.linspace(0.5, 1, 3),
                        'alpha': np.linspace(1e-8, 10, 5),
                        'lambda': np.linspace(1e-8, 10, 5)}]

If not defined by the user the  software will provide a default space. 

**models:int:** Default ['all'] - List with models to be used in the search for the AutoML tool. It is mandatory to pass the model alias within a list even if its only on model. The available models in the tool are:CatBoostClassifier, CatBoostRegressor, LGBMClassifier, LGBMRegressor, XGboostClassifier, XGBoostRegressor, AdaBoostClassifier, AdaBoostRegressor, DecisionTreeClassifier, DecisionTreeRegressor, LogisticRegression and SVR. To use these option in the autoML tool you should use the parameter models with one or more of more of the the respective aliases: ‘catboost’, ‘lgbm’, ‘xgb’, ‘adaboost’, ‘decision_tree’, ‘logistic_regression’, or ‘svr’. E.g: models = ['catboost']. To usel all models, pass the option ['all'] or do not set this parameter.

**compute_ks:** bool: Default - False:  Boolean flag for computation of Komolgorov Smirnov (KS) test. When True the 1% best AUC ranked models are tested for KS. The model with best KS is chosen. It is only used in classification tasks.

**n_folds: int:** Default- 5 - Number of folders to be used in cross-validation. It is used in GridSearchCV and OptunaSearch

**feature_selection:**- bool - Default: False: Boolean flag for indicating the tool should or not perform feature selection in the dataset. The tool used for performing Features Selection is BorutaPy with RandomForest.

**fs_params:** dict -  Default - {'max_depth': [5]} : The parameterization for the RandomForest estimator of BorutaPy. It is only used when feature_selection is True. In this version only max_depth parameter is available.

**acceptance_rate:** float - The rate of models acceptation from all the possible combinations fitted in the search. It is only used when compute_ks is set to True. E.g: If acception_rate = 0.001, from the 0.1% best AUC ranked  models fitted in the search the tool will choose the model with best KS.

**n_trials:** int- Default: 10-  Number of trials in OptunaSearch. 

**n_jobs:** int: Default: -1: Number of processors to be used. When set to -1, all processors will be used.