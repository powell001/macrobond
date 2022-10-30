import pandas as pd
import statsmodels.tsa.seasonal

from base_functions import *
from os import path

#@dataclasses

def readMacrobondDatatoDF(dataNamesLocation, overwrite=True):

    ''' 1. if the sectorDataAll.csv file doesn't exist, create it
        2. if sectorDataAll.csv does exist, but you want to overwrite it, create it with overwrite = True
        3. if sectorDataAll.csv does exist, and you dont want to overwrite it, set overwrite = False
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
data1 = pd.read_csv("data/sectorDataAll.csv", parse_dates=True, index_col=[0])


def getCountrySectorData(data, countryName):
    getCols = [col for col in data.columns if countryName in col]
    return(data.loc[:, getCols])

country1 = getCountrySectorData(data1, "Austria")
country1.to_csv("tmp1.csv")

import scipy
countries1 = allCountries()

allcountries = []
for j in countries1:
    # select one country at a time
    country1 = getCountrySectorData(data1, j)/1000000

    rows = []

    for i in range(0, country1.shape[1]):
        # for each variable of each country


        colData = scipy.signal.detrend(country1.iloc[:,i].dropna())
        sectorName = country1.columns[i]

        mean_detrend = colData.mean()

        std_detrend = colData.std()

        # number of obs less than two deviations away from detrended mean
        outlier_low = len(colData[colData < colData.mean() - 2.5 * colData.std()])

        # number of obs greater than two deviations away from detrended mean
        outlier_high = len(colData[colData > colData.mean() + 2.5 * colData.std()])

        # trend
        data = country1.iloc[:,i].dropna()
        x = np.arange(0,len(data))
        y = np.array(data)
        z = np.polyfit(x,y,1)
        trend = z[0]
        constant = z[1]
        formula1 = f"{constant:.1f} + {trend:.1f}x."

        lastQuarter = country1.iloc[:, i].dropna()[-1]

        avg_LastFourQuarters = country1.dropna().iloc[-4:, i].mean()

        avg_LastFiveYears = country1.dropna().iloc[-(4*5):, i].mean()

        volatility = (std_detrend/avg_LastFiveYears) * 100

        warnings = "Missing values"

        date_created = pd.to_datetime("today").strftime("%m/%d/%Y")

        numberObservations = country1.iloc[:,i].dropna().shape[0]

        missingValues = country1.iloc[:,i].isna().sum()

        rangeofValues = (country1.iloc[:,i].dropna().index[0].strftime('%m-%d-%Y'), country1.iloc[:,i].dropna().index[-1].strftime('%m-%d-%Y'))


        rows.append([j,
                     sectorName,
                     rangeofValues,
                     missingValues,
                     lastQuarter,
                     avg_LastFourQuarters,
                     avg_LastFiveYears,
                     formula1,
                     std_detrend,
                     outlier_low,
                     outlier_high,
                     volatility,
                     warnings,
                     date_created])
    df = pd.DataFrame(rows, columns=["Country",
                                     "Sector",
                                     "rangeofValues",
                                     "missingValues",
                                     "lastQuarter",
                                     "avg_LastFourQuarters",
                                     "avg_LastFiveYears",
                                     "formula1 (1M) per quarter",
                                     "std_detrend",
                                     "outlier_low (2.5 std)",
                                     "outlier_high (2.5 std)",
                                     "volatility",
                                     "warnings",
                                     "date_created"])
    allcountries.append(df)

pd.concat(allcountries).to_csv("basicStats.csv", index=False, float_format='%.2f')
