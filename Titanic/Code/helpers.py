#! usr/env/bin python

import pandas as pd

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


def score_impute_strategies(data, imp_target:str, columns: list, 
    estimators: list, scorer: str, n_splits: int=5, max_iter: int=10, 
    simple_strats: list=['mean', 'median'], groups=None):
    """
    Given a Pandas DataFrame where the target variable is in the first column,
    calculate the score of each type of imputation strategy passed.
    """

    # Separate X and y arrays
    X_full = data.loc[data[imp_target].notnull()][columns].iloc[:, 1:]
    y_full = data.loc[data[imp_target].notnull()][columns].iloc[:, 0]

    # Estimate the score on the entire dataset, with no missing values
    base_est = estimators[0]
    score_full_data = pd.DataFrame(
        cross_val_score(
            base_est, X_full, y_full, scoring=scorer,
            cv=KFold(n_splits, shuffle=True), groups=groups
        ),
        columns=['Full Data']
    )

    # Create copy of entire dataset with missing values
    X_missing = data[columns].iloc[:, 1:]
    y_missing = data[columns].iloc[:, 0]

    # Estimate the score after imputation (mean and median strategies)
    score_simple_imputer = pd.DataFrame()
    for strategy in list(simple_strats):
        estimator = make_pipeline(
            SimpleImputer(strategy=strategy),
            base_est
        )
        score_simple_imputer[strategy] = cross_val_score(
            estimator, X_missing, y_missing, scoring=scorer,
            cv=KFold(n_splits, shuffle=True), groups=groups
        )

    # Estimate the score after iterative imputation
    score_iterative_imputer = pd.DataFrame()
    for impute_estimator in estimators:
        estimator = make_pipeline(
            IterativeImputer(estimator=impute_estimator, max_iter=max_iter),
            base_est
        )
        score_iterative_imputer[impute_estimator.__class__.__name__] = \
            cross_val_score(
                estimator, X_missing, y_missing, scoring=scorer,
                cv=KFold(n_splits, shuffle=True), groups=groups
            )

    # Aggregate scores together from each method
    scores = pd.concat(
        [score_full_data, score_simple_imputer, score_iterative_imputer],
        keys=['Original', 'SimpleImputer', 'IterativeImputer'], axis=1
    )

    # Return results
    return scores
