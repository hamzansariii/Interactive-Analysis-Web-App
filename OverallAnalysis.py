


def data_over_time(dataFrame,col):

    nations_over_time = dataFrame.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time



def most_successful(dataFrame, sport):
    temp_dataFrame = dataFrame.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_dataFrame = temp_dataFrame[temp_dataFrame['Sport'] == sport]

    x = temp_dataFrame['Name'].value_counts().reset_index().head(15).merge(dataFrame, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x