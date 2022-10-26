import win32com.client
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pytest

# load per country
# table per country
# pdf and text data descriptions
# auto arimas
# statistics
#from macrobond_api_constants import SeriesFrequency as f
#https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test


def connectMacrobond():
    connection = win32com.client.Dispatch("Macrobond.Connection")
    print("API version: ", connection.Version)
    return(connection.Database)

def getMacrobondSeries(myseries, connect):
    data1 = connect.FetchOneSeries(myseries)
    return(data1.Values)

def collectSeriesMetaData(myseries, d):

    data1 = d.FetchOneSeries(myseries)

    metaData=data1.Metadata
    print("Meta Values: ", metaData.GetFirstValue("Frequency"))
    #print("First date: ",  data1.DatesAtStartOfPeriod[0])
    print("First date: ", pd.to_datetime(data1.DatesAtStartOfPeriod[0].strftime('%Y-%m-%d')))
    seriesStartDate = pd.to_datetime(data1.DatesAtStartOfPeriod[0].strftime('%Y-%m-%d'))
    seriesEndDate = pd.to_datetime(data1.DatesAtStartOfPeriod[-1].strftime('%Y-%m-%d'))

    country=metaData.GetFirstValue("Region")

    if metaData.GetFirstValue("Frequency")=='quarterly':
        dates1=pd.date_range(seriesStartDate, seriesEndDate, freq="QS")
    else:
        print(metaData.GetFirstValue("Frequency"))

    return(dates1)



#seriesName = 'clv10meurscaab1gdea1'
#print(collectSeriesMetaData("clv10meurscacb1gata1", connectMacrobond()))
#plotOneSeries(seriesName)

def sliceMacrobondCountryName(seriesName):

    '''take last four characters of series name, this appears to be the country name'''

    # Todo if not in dictionary ...

    country1=seriesName[-4:]

    dictCountry={
        "ata1": "Austria",
        "bea1": "Belguim",
        "bga1": "Bulgaria",
        "hra1": "Croatia",
        "cya1": "Cyprus",
        "cza1": "Czech Republic",
        "dka1": "Denmark",
        "eea1": "Estonia",
        "eaa1": "Euro Area",
        "fia1": "Finland",
        "fra1": "France",
        "dea1": "Germany",
        "ela1": "Greece",
        "hua1": "Hungary",
        "iea1": "Ireland",
        "ita1": "Italy",
        "lva1": "Latvia",
        "lta1": "Lithuania",
        "lua1": "Luxembourg",
        "mta1": "Malta",
        "nla1": "Netherlands",
        "mka1": "North Macedonia",
        "noa1": "Norway",
        "pla1": "Poland",
        "pta1": "Portugal",
        "roa1": "Romania",
        "rsa1": "Serbia",
        "ska1": "Slovakia",
        "sia1": "Slovenia",
        "esa1": "Spain",
        "sea1": "Sweden",
        "cha1": "Switzerland",
        "tra1": "Turkey",
        "uka1": "United Kingdom"
        }

    return(dictCountry[country1])

def sliceMacrobondSectorName(seriesName):

    '''remove last four characters of series name, this appears to be the sector name'''

    #Todo if not in dictionary ...

    sector1 = seriesName[:-4]

    dictSector={
        "clv10meurscacb1g": "Manufacturing",
        "clv10meurscaab1g": "Agriculture, Forestry & Fishing",
        "clv10meurscar_ub1g": "Arts, Entertainment & Recreation",
        "clv10meurscafb1g": "Construction",
        "clv10meurscakb1g": "Financial & Insurance Activities",
        "clv10meurscab_eb1g": "Industry",
        "clv10meurscajb1g": "Information & Communication",
        "clv10meurscamnb1g": "Professional, Scientific & Technical Activities",
        "clv10meurscao_qb1g": "Public Administration",
        "clv10meurscalb1g": "Real Estate",
        "clv10meurscag_ib1g": "Wholesale Retail",
    }

    return(dictSector[sector1])


def plotOneSeries(seriesName):

    values=getMacrobondSeries(seriesName, connectMacrobond())
    values=np.log(values)

    seriesDates=collectSeriesMetaData(seriesName, connectMacrobond())

    sectorName=sliceMacrobondSectorName(seriesName)

    countryName=sliceMacrobondCountryName(seriesName)

    df1=pd.DataFrame(values, index=seriesDates)
    plt.plot(df1)
    plt.title(sectorName + ": " + countryName)

    plt.savefig("figures/" + sectorName + "_" + countryName + '.png')
    # Needed to
    plt.close()

    return(None)


# changing the rc parameters and plotting a line plot
plt.rcParams['figure.figsize'] = [18, 12]

keepTrack = []
def plotAllSectorSeries(seriesName):

    values=getMacrobondSeries(seriesName, connectMacrobond())
    values=np.log(values)

    seriesDates=collectSeriesMetaData(seriesName, connectMacrobond())

    countryName = sliceMacrobondCountryName(seriesName)

    sectorName=sliceMacrobondSectorName(seriesName)

    if sectorName not in keepTrack:
        plt.close()

    keepTrack.append(sectorName)
    df1 = pd.DataFrame(values, index=seriesDates)
    plt.plot(df1)

    plt.text(y=values[-1], x= dt.date(2023, 1, 1), s=countryName)
    plt.title(sectorName + ": All Countries")
    plt.savefig("figures/1_" + sectorName + "_AllCounties" + '.png')

    return(None)

def deleteallFiles():
    import os, shutil
    folder = 'figures/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

allSeries = []
def collectData(data1):
    allData = list()
    for index, row in data1.iterrows():
        seriesName = row['Macrobond_series_id']

        values = getMacrobondSeries(seriesName, connectMacrobond())

        # dataframe
        seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())
        df_values = pd.DataFrame(values, index=seriesDates)

        sectorName = sliceMacrobondSectorName(seriesName)
        countryName = sliceMacrobondCountryName(seriesName)

        df_values.columns = [countryName + "_" + sectorName]

        allSeries.append(df_values)
    return(allSeries)


    # for i in data1.shape[0]:
    #     seriesName = data1.iloc[i, 0]
    #
    #     values = getMacrobondSeries(seriesName, connectMacrobond())
    #     print(values)
    #     values = np.log(values)
    #
    #     seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())
    #
    #     countryName = sliceMacrobondCountryName(seriesName)
    #
    #     sectorName = sliceMacrobondSectorName(seriesName)


countriesKeepTrack = []
def sortDataCountries(data1):
    pass
    #data1.groupby(["Country"])


deleteallFiles()
import datetime as dt
allData = pd.read_excel("data/macrobond_series_eu_industries.xlsx")
# gp1count=allData.groupby('Country').count()
# print(gp1count)

data2 = collectData(allData)

pd.concat(data2,  axis=1).to_csv("tmp2.csv")

# gp1sum=allData.groupby('Country').sum()
# print(gp1sum)


allData = pd.read_excel("data/macrobond_series_eu_industries.xlsx")
for i in range(0,allData.shape[0]):
    seriesName = allData.iloc[i, 0]
    print(seriesName)
    plotOneSeries(seriesName)

from matplotlib.pyplot import figure
for i in range(0,allData.shape[0]):
    seriesName = allData.iloc[i, 0]
    print(seriesName)
    plotAllSectorSeries(seriesName)

#seriesName='clv10meurscag_ib1gsia1'
#print(sliceMacrobondCountryName(seriesName))




####################################################
# import pmdarima as pm
# from pmdarima.preprocessing import BoxCoxEndogTransformer
# from pmdarima.pipeline import Pipeline
#
# # Plot an auto-correlation:
# #pm.plot_acf(pm.c(values))
#
# model1 = pm.auto_arima(values, start_p=1, start_q=1,
#                              max_p=4, max_q=4, m=4,
#                              start_P=0, seasonal=True,
#                              d=1, D=1, trace=False,
#                              error_action='ignore',  # don't want to know if an order does not work
#                              suppress_warnings=True,  # don't want convergence warnings
#                              stepwise=True)  # set to stepwise
#
# print(model1.summary())
#
# train, test = values[:120], values[120:]
#
# pipeline = Pipeline([
#     ("boxcox", BoxCoxEndogTransformer()),
#     ("model", model1)
# ])
#
# pipeline.fit(train)
# print(pipeline.predict(5))

# wineind = pm.datasets.load_wineind()
# print(len(wineind))

#
# raw1 = pd.read_excel("macrobond_codes_international_sectormodel.xlsx")
#
# countries=raw1["Country"]
# print(countries)
#
# #print(raw1[raw1.Country=="Sweden"])
# ls1 = []
# countryList = []
# countryDFList = []
# for i in countries:
#     print(i)
#     #country = raw1.iloc[i, 1]
#     # if country in countryList:
#     #     break
#     # countryList.append(country)
#
#     countryData = raw1[raw1.Country == i]
#
#     print(countryData)
#
#     data1 = []
#     for j in range(0,countryData.shape[0]):
#         macbondCode = countryData.Macrobond_series_id.iloc[j]
#         print(macbondCode)
#         Variable = countryData.Variable.iloc[j]
#         print(Variable)
#
#
#         s = d.FetchOneSeries(macbondCode)
#         print(len(s.Values))
#         data1.append(pd.DataFrame(s.Values))
#
#     countryDf = pd.concat(data1, axis=1, ignore_index=True)
#     countryDf.columns=countryData['Variable']
#     countryDf['Country']=countryData['Country']
#     countryDFList.append(countryDf)
#
#
# zz=pd.concat(countryDFList)
# zz.to_csv("tmp.csv")

    #print(raw1.iloc[i,0:3])
    #s = d.FetchOneSeries(one)
    #print(s)
    #values = s.Values
    #print(values)
    #ls1.append(pd.DataFrame({values))

# print(countryDf.head(20))
#
# print(isinstance(countryDf, pd.DataFrame))
#
# countryDf['tmp']='aaa'
# print(countryDf)

#dd = countryDf['Country']='Austria'
#print(dd)

# int(pd.concat(ls1))

# values = s.Values
# print(values)
#
# plt.plot(values)
#
# #plt.imshow(img.reshape((28, 28)))
#
# plt.show()
# import pmdarima as pm
#
# data = pm.datasets.load_wineind()
# train, test = data[:150], data[150:]
#
# # Fit two different ARIMAs
# m1 = pm.auto_arima(train, error_action='ignore', seasonal=True, m=1)
# m12 = pm.auto_arima(train, error_action='ignore', seasonal=True, m=12)
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# fig, axes = plt.subplots(1, 2, figsize=(12, 8))
# x = np.arange(test.shape[0])
#
# # Plot m=1
# axes[0].scatter(x, test, marker='x')
# axes[0].plot(x, m1.predict(n_periods=test.shape[0]))
# axes[0].set_title('Test samples vs. forecasts (m=1)')
#
# # Plot m=12
# axes[1].scatter(x, test, marker='x')
# axes[1].plot(x, m12.predict(n_periods=test.shape[0]))
# axes[1].set_title('Test samples vs. forecasts (m=12)')
#
# plt.show()