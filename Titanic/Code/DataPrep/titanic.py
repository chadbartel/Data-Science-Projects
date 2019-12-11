#! usr/env/bin python

from pandas import read_csv, CategoricalDtype
from numpy import int32, float64, zeros_like, triu_indices_from
from numpy import bool as npbool
from sklearn.preprocessing import LabelEncoder
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from matplotlib.pyplot import gcf
from seaborn import heatmap
from seaborn import diverging_palette

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

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
    

    def drop_column(self, column: str):
        """
        Drops a column from data attribute.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError
        
        if column in self.data.columns.tolist():
            self.data = self.data.drop([column], axis='columns')
        
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
            raise ValueError

        # Drop 'Ticket' column 
        #   Does not add value, no valuable pattern found
        try:
            self.drop_column('Ticket')
        except KeyError:
            raise KeyError

        # Drop 'Cabin' column
        #   Too many missing values > 20%, impute inherently biased
        try:
            self.drop_column('Cabin')
        except KeyError:
            raise KeyError

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
            self.drop_column(column)
        
        return None

    
    def plot_missing_data(self):
        """
        Generate bar plot of missing data across all columns.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        else:
            # Plot missing data
            _x = self.data.isnull().sum().index.tolist()
            _y = self.data.isnull().sum().values.tolist()

            _, ax = plt.subplots()
            plt.bar(_x, _y)

            for i, j in zip(_x, _y):
                ax.annotate(str(j), xy=(i, j))

            plt.show()

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


    def impute_values(self, estimator, column: str, columns: list, 
        max_iter: int, drop: bool=False):
        """
        Impute values for a column using the given estimator.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        if column not in columns:
            # Column must be numeric
            raise ValueError

        # Create new column name
        new_column = column + '_Impute'

        # Create iterative imputer
        imp = IterativeImputer(
            estimator=estimator,
            max_iter=max_iter
        )

        # Fit imputer
        imp.fit(self.data[columns])

        # Set imputed values to new field
        self.data[new_column] = imp.transform(
            self.data[columns]
        )[:, columns.index(column)]
        
        if drop:
            # Drop non-imputed column
            self.drop_column(column)

        return None
    
    
    def get_target_correlation(self, var: str=None, target: str="Survived"):
        """
        Returns a pivot table showing correlation of a variable on the target.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        if var is not None and var not in self.data.columns.tolist():
            # Column does not exist
            raise ValueError

        if target not in self.data.columns.tolist():
            # Column does not exist
            raise ValueError
        
        if self.data[var].dtype == 'float64':
            # Variable is not discrete
            raise ValueError
        
        if var is None:
            return self.data[[target]].mean()
        
        return self.data[[var, target]].groupby(var, as_index=False).mean()
    

    def plot_value_counts(self, column: str):
        """
        Returns a barplot of frequency counts for a column.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        if column not in self.data.columns.tolist():
            # Column does not exist
            raise ValueError

        _x = self.data[column].value_counts().index.tolist()
        _y = self.data[column].value_counts().values.tolist()

        _, ax = plt.subplots()
        plt.bar(_x, _y)

        for i, j in zip(_x, _y):
            ax.annotate('{} ({:.1f}%)'.format(
                j, (j/self.data.shape[0])*100), xy=(i, j)
            )

        plt.show()

        return None


    def get_value_counts(self, column: str, normalize: bool=False):
        """
        Returns a Pandas Series object of value counts for a column.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError

        if column not in self.data.columns.tolist():
            # Column does not exist
            raise ValueError

        return self.data[column].value_counts(normalize=normalize)
    

    def get_correlation_heatmap(self, columns: list, method: str='pearson', 
        annot: bool=True, cmap: str=None):
        """
        Returns Matplotlib figure object of correlation heatmap.
        """
        
        if self.data is None:
            # No data in object
            raise ValueError
        
        for column in columns:
            if column not in self.data.columns.tolist():
                # Column does not exist
                raise ValueError
        
        if cmap is None:
            cmap = diverging_palette(220, 10, as_cmap=True)
        
        # Compute correlation matrix
        corr = self.data[columns].corr(method=method)

        # Generate mask for upper triangle
        mask = zeros_like(corr, dtype=npbool)
        mask[triu_indices_from(mask)] = True
        
        # Draw heatmap figure
        heatmap(
            corr,
            mask=mask,
            cmap=cmap,
            vmax=1.,
            vmin=-1,
            center=0,
            square=True,
            annot=annot
        )
        fig = gcf()
        
        return fig
