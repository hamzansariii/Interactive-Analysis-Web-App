
def yearwise_medal_tally(dataFrame,country):
    temp_dataFrame = dataFrame.dropna(subset=['Medal'])
    temp_dataFrame.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_dataFrame = temp_dataFrame[temp_dataFrame['region'] == country]
    final_dataFrame = new_dataFrame.groupby('Year').count()['Medal'].reset_index()

    return final_dataFrame

def country_event_heatmap(dataFrame,country):
    temp_dataFrame = dataFrame.dropna(subset=['Medal'])
    temp_dataFrame.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_dataFrame = temp_dataFrame[temp_dataFrame['region'] == country]

    pt = new_dataFrame.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(dataFrame, country):
    temp_dataFrame = dataFrame.dropna(subset=['Medal'])

    temp_dataFrame = temp_dataFrame[temp_dataFrame['region'] == country]

    x = temp_dataFrame['Name'].value_counts().reset_index().head(10).merge(dataFrame, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x