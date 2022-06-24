




def weight_v_height(dataFrame,sport):
    athlete_dataFrame = dataFrame.drop_duplicates(subset=['Name', 'region'])
    athlete_dataFrame['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_dataFrame = athlete_dataFrame[athlete_dataFrame['Sport'] == sport]
        return temp_dataFrame
    else:
        return athlete_dataFrame

def men_vs_women(dataFrame):
    athlete_dataFrame = dataFrame.drop_duplicates(subset=['Name', 'region'])

    men = athlete_dataFrame[athlete_dataFrame['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_dataFrame[athlete_dataFrame['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final