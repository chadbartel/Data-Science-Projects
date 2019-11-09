# [Interactive Data Exploration, Analysis, and Reporting](https://github.com/Azure/Azure-TDSP-Utilities/blob/master/DataScienceUtilities/DataReport-Utils/Python/IDEAR-Python-Instructions-JupyterNotebook.md)

1. Read and summarize the data
    1. Read and infer column types
    2. Print the first n rows of the data
    3. Print the dimensions, column names, and types of the data
2. Extract descriptive statistics of each column
    1. Print the descriptive statistics of numerical columns
    2. Print the descriptive statistics of categorical columns
3. Explore individual variables
    1. Explore the target variable
    2. Explore individual numeric variables and test for normality (on sampled data)
        * Histogram
        * KDE
        * QQ-plot
        * Boxplot
    3. Explore individual categorical variables (sorted by frequencies)
4. Explore interactions between variables
    1. Rank variables
        * The associations between CATEGORICAL and NUMERICAL variables are computed using the [eta-squared metric](https://en.wikiversity.org/wiki/Eta-squared).
        * The associations between CATEGORICAL variables are computed using the [Cramer V metric](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V).
    2. Explore interactions between categorical variables
    3. Explore interactions between numerical variables (on sampled data)
        * Scatter plot
        * Fit linear model and show
        * Fit loss line and show
    4. Explore correlation matrix between numerical variables
    5. Explore interactions between numerical and categorical variables
        * Boxplot for each categorical value
    6. Explore interactions between two numerical variables and a categorical variable (on sampled data)
        * Scatter plot with categorical color
5. Visualize numerical data by projecting to principal component spaces
6. Generate report
