import numpy as np

def fetch_medal_tally(dataFrame, year, country):
    medal_dataFrame = dataFrame.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_dataFrame = medal_dataFrame
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_dataFrame = medal_dataFrame[medal_dataFrame['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_dataFrame = medal_dataFrame[medal_dataFrame['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_dataFrame = medal_dataFrame[(medal_dataFrame['Year'] == year) & (medal_dataFrame['region'] == country)]

    if flag == 1:
        x = temp_dataFrame.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_dataFrame.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(dataFrame):
    years = dataFrame['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(dataFrame['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country