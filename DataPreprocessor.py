import pandas as pd

def preprocess(dataFrame,region_dataFrame):
    # filtering to get only summer olympic data
    dataFrame = dataFrame[dataFrame['Season'] == 'Summer']

    # merge with both the datasets
    dataFrame = dataFrame.merge(region_dataFrame, on='NOC', how='left')

    # dropping duplicates
    dataFrame.drop_duplicates(inplace=True)
    
    # one hot encoding medals
    dataFrame = pd.concat([dataFrame, pd.get_dummies(dataFrame['Medal'])], axis=1)
    return dataFrame