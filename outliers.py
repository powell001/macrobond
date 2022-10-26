import pandas as pd
import statsmodels.tsa.seasonal

from base_functions import *
from os import path

def readMacrobondDatatoDF(dataNamesLocation, overwrite=True):

    ''' 1. if the sectorDataAll file doesn't exist, create it
        2. if sectorDataAll does exist, but you want to overwrite it, create it
        3. if sectorDataAll does exist, and you dont want to overwrite it, dont do anything
    '''

    if (path.exists("data/sectorDataAll.csv") == False):
        allData = pd.read_excel(dataNamesLocation)
        individualSeries = collectData(allData)
        pd.concat(individualSeries, axis=1).to_csv("data/sectorDataAll.csv")
        print("Created file data/sectorDataAll.csv")
    elif (path.exists("data/sectorDataAll.csv") == False) and (overwrite == True):
        allData = pd.read_excel(dataNamesLocation)
        individualSeries = collectData(allData)
        pd.concat(individualSeries, axis=1).to_csv("data/sectorDataAll.csv")
        print("Created file data/sectorDataAll.csv")
    else:
        print("File /data/sectorDataAll.csv exists")

dataNamesLocation ="data/macrobond_series_eu_industries.xlsx"

readMacrobondDatatoDF(dataNamesLocation, overwrite=False)


# Create descriptive statistics per country, per series, save as a csv

data1 = pd.read_csv("data/sectorDataAll.csv")
print(data1.head())

def getCountrySectorData(data, countryName):
    getCols = [col for col in data.columns if countryName in col]
    return(data[getCols])


country1 = getCountrySectorData(data1, "Austria")
country1.to_csv("tmp1.csv")

import scipy
#plt.plot(country1.iloc[:,0].dropna())
#plt.show()

countries1 = allCountries()

allcountries = []
for j in countries1:
    country1 = getCountrySectorData(data1, j)/100000
    rows = []
    for i in range(1, country1.shape[1]):
        colData = scipy.signal.detrend(country1.iloc[:,i].dropna())
        sectorName = country1.columns[i]

        mean_detrend = colData.mean()

        std_detrend = colData.std()

        # number of obs less than two deviations away from detrended mean
        outlier_low = len(colData[colData < colData.mean() - 2 * colData.std()])

        # number of obs greater than two deviations away from detrended mean
        outlier_high = len(colData[colData > colData.mean() + 2 * colData.std()])

        # trend
        data = country1.iloc[:,i].dropna()
        x = np.arange(0,len(data))
        y = np.array(data)
        z = np.polyfit(x,y,1)
        trend = z[0]

        avg_LastFiveYears = country1.iloc[-5:, i].dropna().mean()

        rows.append([j, sectorName, avg_LastFiveYears, trend,  mean_detrend, std_detrend, outlier_low, outlier_high])
    df = pd.DataFrame(rows, columns=["Country", "Sector", "5yr_Avg", "trend", "mean_detrend", "std_detrend", "outlier_low","outlier_high"])
    allcountries.append(df)

pd.concat(allcountries).to_csv("tmp6.csv")
