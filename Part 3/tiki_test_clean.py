import pandas as pd
import numpy as np
from scipy import stats
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns

# Read data
df = pd.read_csv('tiki_test_uncleaned.csv')
# print(df.head(5))

# Check statistics
print(df.describe())

# Check dtype, usage
print(df.info())

# Handling missing value
print(df.isnull().sum())  # No missing data

# Column name standardization
df['Main Category'] = df['Seller\'s Vertical']
df = df.drop(columns=['Seller\'s Vertical'])

# Data type check
df['Sign-up Time'] = pd.to_datetime(df['Sign-up Time'])
df['Activation Time'] = pd.to_datetime(df['Activation Time'])
df['1st Listing'] = pd.to_datetime(df['1st Listing'])
df['1st Salable'] = pd.to_datetime(df['1st Salable'])
df['1st Transaction'] = pd.to_datetime(df['1st Transaction'])
new_order = ['Seller ID', 'Main Category', 'Sign-up Time',
             'Activation Time', '1st Listing', '1st Salable', '1st Transaction']
df = df[new_order]

# Check duplicate
print(df.duplicated().sum())                   # No duplicate
print(df['Seller ID'].duplicated().sum())      # Primary key constraint

# Check membership constraints for categorical data
print(df['Main Category'].unique())

# Cross-field validation for date column
conditions = ((df['Sign-up Time'] > df['Activation Time']) |
              (df['Activation Time'] > df['1st Transaction']))
invalid_rows = df[conditions]
if not invalid_rows.empty:
    print("Invalid rows found:")
    print(invalid_rows.count())
    # print(invalid_rows)
else:
    print("All rows are valid.")

# Adding columns for analysis
df['Sign-up to Activation'] = df['Activation Time'] - df['Sign-up Time']
df['Sign-up to Activation'] = df['Sign-up to Activation'].dt.days

df['Sign-up to Transaction'] = df['1st Transaction'] - df['Sign-up Time']
df['Sign-up to Transaction'] = df['Sign-up to Transaction'].dt.days

df['Sign-up to Listing'] = df['1st Listing'] - df['Sign-up Time']
df['Sign-up to Listing'] = df['Sign-up to Listing'].dt.days

df['Sign-up to Salable'] = df['1st Salable'] - df['Sign-up Time']
df['Sign-up to Salable'] = df['Sign-up to Salable'].dt.days

df['Activation to Listing'] = df['1st Listing'] - df['Activation Time']
df['Activation to Listing'] = df['Activation to Listing'].dt.days

df['Listing to Salable'] = df['1st Salable'] - df['1st Listing']
df['Listing to Salable'] = df['Listing to Salable'].dt.days

df['Salable to Transaction'] = df['1st Transaction'] - df['1st Salable']
df['Salable to Transaction'] = df['Salable to Transaction'].dt.days


class OutliersDetector:
    def __init__(self, data):
        self.data = data

    def zscore(self, column, threshold=3):
        z_score = np.abs(stats.zscore(self.data[column]))
        outliers = self.data[z_score > threshold]
        return outliers

    def remove_outliers(self, column, threshold=3):
        z_score = np.abs(stats.zscore(self.data[column]))
        filtered_data = self.data[z_score <= threshold]
        return filtered_data


if __name__ == "__main__":

    detector = OutliersDetector(df)
    outliers_z_score = detector.zscore('Sign-up to Activation')
    df2 = detector.remove_outliers('Sign-up to Activation')
    print("Outliers detected by Z-Score method:")
    print(outliers_z_score.info())
    # print(df2.info())

# Save data clean
    df2.to_csv('tiki_test.csv', index=False)
