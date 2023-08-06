import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_style('whitegrid')


# Removing outliers per column
def remove_outliers_numeric(df,feature,option = "lognormal",delta=1.5):
    '''This function takes as input DataFrame and feature to remove outliers.
    Two options are available option lognormal and option normal depending on the distribution
    shape'''
    
    if option == "lognormal":
        
        df['log_feature'] = np.log(df[feature])
        feature = 'log_feature'
        
    elif option == "normal":
        
        feature = feature
        
    else:
        
        print("This option is not available")
    
    Q1_value = df[feature].quantile(0.25)
    Q3_value = df[feature].quantile(0.75)
    IQR_value = Q3_value - Q1_value    #IQR is interquartile range.

    filter_value = (df[feature] >= Q1_value - delta * IQR_value) & (df[feature] <= Q3_value + delta *IQR_value)
    df = df.loc[filter_value,:]
    
    return df

# Plot distribution of data per mode
def plot_distribution_numeric(df, feature, option = 'lognormal',title = 'distribution', mode = 'with_outliers', **kwargs):
    ''' This function takes as input a dataFrame as a feature and plot his distribution.
    Three possible modes, plotting the distribution as it is (mode = 'normal'), plotting excluding outliers (mode = 'without_outliers') or
    plotting excluding values below min_feature and above_max_feature (mode = 'with_limits')'''

    plt.figure(figsize=(8,6))

    if mode == 'with_outliers':
        sns.distplot(df[feature])

    elif mode == 'without_outliers':
        df_clean = remove_outliers_numeric(df[[feature]],feature,option=option)
        sns.distplot(df_clean[feature])

    elif mode == 'with_limits':
        df_clean = df.loc[(df[feature]>kwargs['min_feature'])&(df[feature]<kwargs['max_feature']),feature]
        sns.distplot(df_clean)

    else:
        print("this mode is not available")

    plt.title(title)
    plt.show()
    return