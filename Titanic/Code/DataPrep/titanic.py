#! usr/env/bin python

from pandas import read_csv, CategoricalDtype
from numpy import int32, float64
from sklearn.preprocessing import LabelEncoder
from scipy.stats import ttest_ind

from missingno import matrix
from matplotlib.pyplot import tight_layout, show


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

        # Initialize data
        self.data = None

        # Initialize decode dictionary
        self.decode_dict = dict()

        # Initialize missing columns
        self.missing_columns = list()

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
            #   Does not add value, no valuable pattern found
            self.data = self.data.drop(['Ticket'], axis=1)

            # Drop 'Cabin' column
            #   Too many missing values > 20%, impute inherently biased
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
            _encoder = LabelEncoder()
            self.data[new_column] = _encoder.fit_transform(
                self.data[column].astype(str)
            )
        
        # Create dictionary to decode labels
        self.decode_dict[column] = dict(
            zip(
                list(_encoder.transform(_encoder.classes_)),
                list(_encoder.classes_)
            )
        )
        
        if drop:
            # Drop encoded column
            self.data = self.data.drop(column, axis='columns')
        
        return None

    
    def plot_missing_data(self):
        """
        Generate missingno plot of missing data across all columns.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        else:
            # Plot missing data
            matrix(self.data)
            tight_layout()
            show()

        return None
    

    def get_missing_columns(self):
        """
        Update missing columns attribute.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        else:
            # Get list of missing columns in data
            self.missing_columns = self.data.columns[
                self.data.isnull().any()
            ].tolist()
        
        return self.missing_columns
    

    def test_for_mcar(self, column: str, alpha: float=0.05):
        """
        Conduct a 'simplified' Little's MCAR test on each missing column.
            1. Calculate the mean of each column with missing data.
            2. Calculate the mean of each column without missing data.
            3. If a majority of the columns have same/similar means, then it 
                is LIKELY the data is MCAR.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        if self.missing_columns == []:
            # No columns in missing columns attribute
            self.get_missing_columns()
            
        # Calculate t-test for missing column
        if column in self.missing_columns:
            _, p_value = ttest_ind(
                a=self.data['Survived'],
                b=self.data.loc[
                    ~self.data[column].isnull(), 
                    'Survived'
                ]
            )
            
            if p_value > alpha:
                return True     # Can assume MCAR
            else:
                return False    # Cannot assume MCAR
        
        else:
            raise ValueError
    

    def extract_title(self):
        """
        Parses the passenger's name for their title and creates a column.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        self.data['Title'] = self.data['Name'].str.split(
            ", ", expand=True)[1].str.split(".", expand=True)[0]
        
        return None
