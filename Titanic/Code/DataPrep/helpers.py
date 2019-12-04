#! usr/env/bin python

from pandas import read_csv, CategoricalDtype
from numpy import int32, float64
from sklearn.preprocessing import LabelEncoder

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


    def __init__(self, name: str=None):
        
        # Set datatypes
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
        
        if not name:
            # Invalid name passed
            self.name = None

        elif name.lower().strip() in ['train', 'test']:
            # Valid name passed
            self.name = name.lower().strip()
        
        else:
            # Invalid name passed
            self.name = None

        if self.name == 'train':
            # Get Titanic train data
            self.data = read_csv(
                r'Titanic\Data\Raw\train.csv',
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )

        elif self.name == 'test':
            # Get Titanic test data
            self.data = read_csv(
                r'Titanic\Data\Raw\test.csv',
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )
        
        else:
            # No data
            self.data = None

        return None
    

    def get_data(self, name: str=None):
        """
        Gets train/test Titanic data from csv.
        """
        
        if self.name is None and name.lower().strip() in ['train', 'test']:
            # Valid name passed
            self.name = name.lower().strip()

            # Get data
            self.data = read_csv(
                r'Titanic\Data\Raw\{}.csv'.format(self.name),
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )
        
        elif self.name is not None and self.name in ['train', 'test']:
            # Get data
            self.data = read_csv(
                r'Titanic\Data\Raw\{}.csv'.format(self.name),
                index_col='PassengerId',
                usecols=list(self.dtypes_.keys()),
                dtype=self.dtypes_
            )

        else:
            # Invalid name passed
            raise ValueError

        return None


    def clean_data(self):
        """
        Cleans Titanic data for issues identified in EDA.
        """
        
        if self.data is None:
            # No data in object
            return -1

        else:
            # Drop 'Ticket' column
            self.data = self.data.drop(['Ticket'], axis=1)

            # Drop 'Cabin' column
            self.data = self.data.drop(['Cabin'], axis=1)

            return None


    def encode_labels(self, column: str, drop: bool=False):
        """
        Encodes the labels in a column to integers.
        """

        new_column = ''
        if column is None:
            # No column name passed
            raise ValueError

        elif not column in self.data.columns.tolist():
            # Column name does not exist
            raise ValueError

        else:
            new_column += column + '_Code'
        
        if self.data is None:
            # No data in object
            raise ValueError

        else:
            # Encode labels in column
            encoder = LabelEncoder()
            self.data[new_column] = encoder.fit_transform(
                self.data[column].astype(str)
            )
        
        if drop:
            # Drop encoded column
            self.data = self.data.drop(column, axis='columns')
        
        return None
