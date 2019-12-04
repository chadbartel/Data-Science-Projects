#! usr/env/bin python

from pandas import read_csv, CategoricalDtype
from numpy import int32, float64

titanic_dtypes = {
    'PassengerId': int32,
    'Survived': int32, 
    'Pclass': int32, 
    'Name': str,
    'Sex': CategoricalDtype(["male", "female"]), 
    'Age': float64, 
    'SibSp': int32, 
    'Parch': int32, 
    'Fare': float64, 
    'Embarked': CategoricalDtype(["C", "Q", "S"])
}

def get_titanic_data(train_or_test: str='train'):
    """"""
    if train_or_test == 'train':
        filepath = r'Titanic\Data\Raw\train.csv'
    elif train_or_test == 'test':
        filepath = r'Titanic\Data\Raw\test.csv'
    else:
        raise ValueError
    df = read_csv(
        filepath,
        index_col='PassengerId',
        usecols=list(titanic_dtypes.keys()),
        dtype=titanic_dtypes
    )
    return df


class Titanic:
    """
    Reads and organizes Titanic data from csv files.
    """
    def __init__(self, name: str):

        # Read in data

        self.name = name.lower().strip()

        self.dtypes_ = {
            'PassengerId': int32,
            'Survived': int32, 
            'Pclass': int32, 
            'Name': str,
            'Sex': CategoricalDtype(["male", "female"]), 
            'Age': float64, 
            'SibSp': int32, 
            'Parch': int32, 
            'Ticket': str,
            'Fare': float64, 
            'Cabin': str,
            'Embarked': CategoricalDtype(["C", "Q", "S"])
        }

        if self.name.find('train') > -1:
            # Get Titanic train data
            self.data = read_csv(
                r'Titanic\Data\Raw\train.csv',
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )
            # Clean data
            self.clean_data()

        elif self.name.find('test') > -1:
            # Get Titanic test data
            self.data = read_csv(
                r'Titanic\Data\Raw\test.csv',
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )
            # Clean data
            self.clean_data()
        
        else:
            # Invalid name passed
            raise ValueError

    def clean_data(self):
        """
        Cleans Titanic data for issues identified in EDA.
        """
        
        # Check data
        if self.data is None:
            return -1

        # Drop 'Ticket' column
        self.data = self.data.drop(['Ticket'], axis=1)

        # Drop 'Cabin' column
        self.data = self.data.drop(['Cabin'], axis=1)
