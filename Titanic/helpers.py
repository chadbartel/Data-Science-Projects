#! usr/env/bin python

from pandas import read_csv, Categorical
from numpy import int32, float64

titanic_dtypes = {
    'Survived': int32, 
    'Pclass': int32, 
    'Name': str,
    'Sex': Categorical(["male", "female"]), 
    'Age': float64, 
    'SibSp': int32, 
    'Parch': int32, 
    'Fare': float64, 
    'Embarked': Categorical(["C", "Q", "S"])
}

def get_titanic_data(train_or_test: str='train'):
    """"""
    if train_or_test == 'train':
        filepath = r'Titanic\Data\train.csv'
    elif train_or_test == 'test':
        filepath = r'Titanic\Data\test.csv'
    else:
        raise ValueError
    df = read_csv(
        filepath,
        index_col='PassengerId',
        usecols=list(titanic_dtypes.keys()),
        dtype=titanic_dtypes
    )
    return df

class TitanicData:

    def __init__(self, data=None, filepath=None):
        self.data = data
        self.filepath = filepath
    
    def read_file(self, filepath=None):
        if self.filepath is None and filepath:
            self.filepath = filepath
        
        if self.filepath.endswith('.csv'):
            self.data = read_csv(
                self.filepath,
                index_col='PassengerId',
                usecols=[
                    'Survived', 'Pclass', 'Name',
                    'Sex', 'Age', 'SibSp', 
                    'Parch', 'Fare', 'Embarked'
                ],
                dtype={
                    'Survived': int32, 
                    'Pclass': int32, 
                    'Name': str,
                    'Sex': Categorical(["male", "female"]), 
                    'Age': float64, 
                    'SibSp': int32, 
                    'Parch': int32, 
                    'Fare': float64, 
                    'Embarked': Categorical(["C", "Q", "S"])
                }
            )
        else:
            self.data = None
