# Data Science Framework - A Tutorial

## Preface
Supervised learning problem predicting one of two classes.

## Framework Overview
 1. Define the problem
 2. Gather the data
    - Wrangle data
        - Data architecture
        - Data governance
        - Data extraction
 3. Prepare data for consumption
    - Surface-level analysis
        - Columns/features
            - Name
            - Data type
            - Qualitative vs quantitative
            - Independent vs dependent
    - Clean data
        - Correct
            - Correcting aberrant values and outliers
                - E.g.: age = 800; name = Fake Name; etc.
        - Complete
            - Completing missing information
                - Quantitative: impute mean, median, or mean + random std dev
                - Qualitative: impute mode
            - We can also try a model where we don't impute anything
            - Drop records that are mostly missing or if they represent a small percentage
            - Drop columns that have an overwhelming number of missing values
                - Any impute strategy will introduce bias
        - Create
            - Creating new features for analysis
        - Convert
            - Converting fields to the correct format for calculations and presentation
                - Label encoding
                - OneHot encoding
                - Convert variable data types
    - Split ttraining and testing data
 4. Perform exploratory data analysis
    - Examine correlation of qualitative feature variables to the response variable
        - E.g.: "What is the percentage of survival for each value of 'Sex', 'Pclass', and 'Embarked'?"
        - Crosstabs, barplots, pointplots
    - Examine distribution of quantitative feature variables
        - Histograms, boxplots
    - Analyze relationship between each quantitative feature and qualitative feature encoded with the response variable
        - Boxplots, violinplots
 5. Model data
    - Iterate through each applicable ML algorithm using cross-validation to determine best initial test results
    - Understand which model improvement results in greater ROI
 6. Validate and implement data model
 7. Optimize and strategize

### 1. Define the problem

### 2. Gather the data

### 3. Prepare data for consumption
