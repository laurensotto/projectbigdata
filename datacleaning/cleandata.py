import pandas as pd

df = pd.read_csv("covid.csv", sep=";")

df_ggd = df.groupby(['Date_of_publication', 'Province', 'Municipal_health_service'])['Total_reported'].sum()
df_provincie = df.groupby(['Date_of_publication', 'Province'])['Total_reported'].sum()
df_land = df.groupby(['Date_of_publication'])['Total_reported'].sum()
df_ggd.to_csv("covid_ggd.csv", sep=";")
df_provincie.to_csv("covid_provincie.csv", sep=";")


df_bedden = pd.read_csv("bedden.csv", sep=",")


def reformatDate(string):
    split = string.split("-")

    if split[0][0] != "0" and len(split[0]) == 1:
        split[0] = "0" + split[0]

    if split[1][0] != "0" and len(split[1]) == 1:
        split[1] = "0" + split[1]

    formattedDate = split[2] + "-" + split[1] + "-" + split[0]
    return formattedDate


df_bedden['Date_of_publication'] = df_bedden['Datum'].apply(reformatDate)
df_bedden = df_bedden[['Date_of_publication', 'IC_Bedden_COVID_Nederland', 'Kliniek_Bedden_Nederland']]
df_land = pd.merge(df_land, df_bedden, on='Date_of_publication')
df_land.to_csv("covid_land.csv", sep=";")
