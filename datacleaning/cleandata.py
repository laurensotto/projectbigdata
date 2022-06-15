import pandas as pd

df = pd.read_csv("../csvdata/covid2.csv", sep=";")
df_ggd = df.groupby(['Date_of_publication', 'Province', 'Municipal_health_service'])['Total_reported'].sum()
df_provincie = df.groupby(['Date_of_publication', 'Province'])['Total_reported'].sum()
df_land = df.groupby(['Date_of_publication'])['Total_reported'].sum()
df_dood = df.groupby(['Date_of_publication'])['Deceased'].sum()
df_land = pd.merge(df_land, df_dood, on='Date_of_publication')
df_ggd.to_csv("covid_ggd.csv", sep=";")
df_provincie.to_csv("covid_provincie.csv", sep=";")
df_bedden = pd.read_csv("../csvdata/bedden.csv", sep=",")
df_uk = pd.read_csv("../csvdata/covid_uk.csv")
df_zorg = pd.read_csv("../csvdata/zorg.csv", sep=",")

df_land.to_csv("covid_land.csv", sep=";")


def reformatDate(string):
    split = string.split("-")

    if split[0][0] != "0" and len(split[0]) == 1:
        split[0] = "0" + split[0]

    if split[1][0] != "0" and len(split[1]) == 1:
        split[1] = "0" + split[1]

    formattedDate = split[2] + "-" + split[1] + "-" + split[0]
    return formattedDate


def bilToActual(number):
    return number * 1000000000


def milToActual(number):
    return number * 1000000


df_bedden['Date_of_publication'] = df_bedden['Datum'].apply(reformatDate)
df_bedden = df_bedden[['Date_of_publication', 'IC_Bedden_COVID_Nederland', 'Kliniek_Bedden_Nederland']]
df_land = pd.merge(df_land, df_bedden, on='Date_of_publication')

df_zorg["Uitgaven VK in Pond"] = df_zorg["UK_Spending_Billion_Pound"].apply(bilToActual)
df_zorg["Uitgaven VK in Euro"] = df_zorg["UK_Spending_Billion_Euro"].apply(bilToActual)
df_zorg["Uitgaven NL in Euro"] = df_zorg["NL_Spending_Billion_Euro"].apply(bilToActual)
df_zorg["Inwoners VK"] = df_zorg["UK_Inhabitants_Million"].apply(milToActual)
df_zorg["Inwoners NL"] = df_zorg["NL_Inhabitants_Million"].apply(milToActual)
df_zorg["Uitgaven VK in Pond per inwoner"] = (df_zorg["Uitgaven VK in Pond"] / df_zorg["Inwoners VK"]).round(2)
df_zorg["Uitgaven VK in Euro per inwoner"] = (df_zorg["Uitgaven VK in Euro"] / df_zorg["Inwoners VK"]).round(2)
df_zorg["Uitgaven NL in Euro per inwoner"] = (df_zorg["Uitgaven NL in Euro"] / df_zorg["Inwoners NL"]).round(2)
df_zorg["IC-bedden VK"] = df_zorg["UK_IC_Beds"]
df_zorg["IC-bedden NL"] = df_zorg["NL_IC_Beds"]
df_zorg["Ziekenhuisbedden VK"] = df_zorg["UK_Beds"]
df_zorg["Ziekenhuisbedden NL"] = df_zorg["NL_Beds"]
df_zorg["IC-bedden VK per 100.000 inwoners"] = df_zorg["UK_IC_Beds"] / (df_zorg["Inwoners VK"] / 100000)
df_zorg["IC-bedden NL per 100.000 inwoners"] = df_zorg["NL_IC_Beds"] / (df_zorg["Inwoners NL"] / 100000)
df_zorg["Ziekenhuisbedden VK per 100.000 inwoners"] = df_zorg["UK_Beds"] / (df_zorg["Inwoners VK"] / 100000)
df_zorg["Ziekenhuisbedden NL per 100.000 inwoners"] = df_zorg["NL_Beds"] / (df_zorg["Inwoners VK"] / 100000)
df_land["IC-bedden NL bezet"] = df_land["IC_Bedden_COVID_Nederland"]
df_uk["IC-bedden VK bezet"] = df_uk["covidOccupiedMVBeds"]
df_land["Ziekenhuisbedden NL bezet"] = df_land["Kliniek_Bedden_Nederland"]
df_uk["Ziekenhuisbedden VK bezet"] = df_uk["hospitalCases"]
df_land["IC-bedden NL bezet per 100.000 inwoners"] = df_land["IC_Bedden_COVID_Nederland"] / (17590000 / 100000)
df_uk["IC-bedden VK bezet per 100.000 inwoners"] = df_uk["covidOccupiedMVBeds"] / (68210000 / 100000)
df_land["Ziekenhuisbedden NL bezet per 100.000 inwoners"] = df_land["Kliniek_Bedden_Nederland"] / (17590000 / 100000)
df_uk["Ziekenhuisbedden VK bezet per 100.000 inwoners"] = df_uk["hospitalCases"] / (68210000 / 100000)
df_uk["Date_of_publication"] = df_uk["date"]
df_uk["Aantal besmettingen VK"] = df_uk["newCasesByPublishDate"]
df_uk["Aantal doden VK"] = df_uk["newDailyNsoDeathsByDeathDate"]
df_land["Aantal besmettingen NL"] = df_land["Total_reported"]
df_land["Aantal doden NL"] = df_land["Deceased"]
df_uk["Aantal besmettingen VK per 100.000 inwoners"] = df_uk["newCasesByPublishDate"] / (68210000 / 100000)
df_uk["Aantal doden VK per 100.000 inwoners"] = df_uk["newDailyNsoDeathsByDeathDate"] / (68210000 / 100000)
df_land["Aantal besmettingen NL per 100.000 inwoners"] = df_land["Aantal besmettingen NL"] / (17590000 / 100000)
df_land["Aantal doden NL per 100.000 inwoners"] = df_land["Deceased"] / (17590000 / 100000)
df_land = pd.merge(df_land, df_uk, on='Date_of_publication')
df_land["Datum publicatie"] = df_land["Date_of_publication"]

df_combinatie = df_land[[
    "Datum publicatie",
    "Aantal besmettingen VK",
    "Aantal besmettingen NL",
    "Aantal doden VK",
    "Aantal doden NL",
    "IC-bedden VK bezet",
    "IC-bedden NL bezet",
    "Ziekenhuisbedden VK bezet",
    "Ziekenhuisbedden NL bezet",
    "Aantal besmettingen VK per 100.000 inwoners",
    "Aantal besmettingen NL per 100.000 inwoners",
    "Aantal doden VK per 100.000 inwoners",
    "Aantal doden NL per 100.000 inwoners",
    "IC-bedden VK bezet per 100.000 inwoners",
    "IC-bedden NL bezet per 100.000 inwoners",
    "Ziekenhuisbedden VK bezet per 100.000 inwoners",
    "Ziekenhuisbedden NL bezet per 100.000 inwoners",
]]

df_zorg.to_csv("zorg_fixed.csv", sep=";")
df_combinatie.to_csv("covid_land.csv", sep=";")
