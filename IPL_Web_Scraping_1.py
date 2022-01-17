from selenium import webdriver
import pandas as pd


# Chrome Browser class
class ChromeBrowser:
    def __init__(self):
        self.cd = r'chromedriver.exe'

    def Chrome(self):
        return webdriver.Chrome(self.cd)


# IPL data extraction
class IPL_Data:
    def __init__(self, url_id, years, columns):
        self.url_id = url_id
        self.years = years
        self.columns = columns

    def ExtractDetails(self, n):
        Chrome1 = ChromeBrowser().Chrome()
        Chrome2 = ChromeBrowser().Chrome()
        year = self.years[n]
        id = self.url_id[n]
        url = 'https://www.cricbuzz.com/cricket-series/' + str(id) + '/indian-premier-league-' + str(year) + '/matches'
        Chrome1.get(url)
        table = Chrome1.find_element_by_xpath('//*[@id="page-wrapper"]/div[4]')
        date_list = table.find_elements_by_class_name('ng-binding')
        date = []

        # Date and year columns
        for j in date_list:
            date.append(j.text)
            for i in range(3, len(date) - 1):
                if date[i] == '' and date[i + 1] == '':
                    date[i] = date[i - 1]
        while "" in date:
            date.remove("")
        year_list = []
        for i in range(len(date)):
            year_list.append(year)
        team_list = table.find_elements_by_class_name('text-hvr-underline')
        team = []
        team1 = []
        team2 = []
        for j in team_list:
            team.append(j.text)
            team1.append(j.text.split('vs')[0])
            team2.append(j.text.split('vs')[1].split(',')[0])

        # result and time columns
        place_card = table.find_elements_by_class_name('text-gray')
        place = []
        time = []
        for i in range(len(place_card)):
            if (i % 2 == 0):
                place.append(place_card[i].text)
            elif (i % 2 == 1):
                time.append(place_card[i].text)
        result_list = table.find_elements_by_class_name('cb-text-complete')
        result = []
        for i in result_list:
            result.append(i.text)
        score_card = []
        toss = []
        bat_bowl = []
        for j in result_list:
            load = j.get_attribute('href')
            ref = load.split("/")
            ref[3] = "cricket-match-facts"
            ref = '/'.join(ref)
            score_card.append(ref)
            Chrome2.get(ref)
            tab = Chrome2.find_element_by_xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div[2]')
            won = tab.find_element_by_xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div[2]/div[6]')
            won = won.text.replace(" won the toss and opt to ", " ")
            bat_bowl.append(won.split()[-1])
            if won.split()[-1] == "bowl":
                won = won.replace("bowl", " ")
            elif won.split()[-1] == "bat":
                won = won.replace("bat", " ")
            toss.append(won)
        Chrome1.close()
        Chrome2.close()
        init_dict = {'Team1': team1, 'Team2': team2, 'Date': date, 'Year': year_list, 'Time': time, 'Place': place,
                     'Toss': toss,
                     'TossDecision': bat_bowl, 'Result': result}
        return init_dict

    def StoreData(self, df_dict):
        df = pd.DataFrame(df_dict, dtype='object')
        df.to_csv('IPL_Results(2008-2020).csv')
        print(df.shape)


url_id = [2058, 2059, 2060, 2037, 2115, 2170, 2261, 2330, 2430, 2568, 2676, 2810, 3130]
years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
columns = ['Team1', 'Team2', 'Date', 'Year', 'Time', 'Place', 'Toss', 'TossDecision', 'Result']

Code = IPL_Data(url_id, years, columns)

df_team1 = []
df_team2 = []
df_date = []
df_year = []
df_time = []
df_place = []
df_toss = []
df_toss_decision = []
df_result = []

for i in range(0, len(url_id)):
    print(i)
    init_dict = Code.ExtractDetails(i)
    df_team1.extend(init_dict['Team1'])
    df_team2.extend(init_dict['Team2'])
    df_date.extend(init_dict['Date'])
    df_year.extend(init_dict['Year'])
    df_time.extend(init_dict['Time'])
    df_place.extend(init_dict['Place'])
    df_toss.extend(init_dict['Toss'])
    df_toss_decision.extend(init_dict['TossDecision'])
    df_result.extend(init_dict['Result'])
df_dict = {'Team1': df_team1, 'Team2': df_team2, 'Date': df_date, 'Year': df_year, 'Time': df_time, 'Place': df_place,
           'Toss': df_toss,
           'TossDecision': df_toss_decision, 'Result': df_result}
Code.StoreData(df_dict)
