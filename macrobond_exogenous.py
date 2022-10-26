import pandas as pd
import statsmodels.tsa.seasonal

from base_functions import *
from os import path


def collectSeriesMetaData(myseries, d):

    data1 = d.FetchOneSeries(myseries)

    metaData=data1.Metadata
    print("Meta Values: ", metaData.GetFirstValue("Frequency"))

    seriesStartDate = pd.to_datetime(data1.DatesAtStartOfPeriod[0].strftime('%Y-%m-%d'))
    seriesEndDate = pd.to_datetime(data1.DatesAtStartOfPeriod[-1].strftime('%Y-%m-%d'))

    if metaData.GetFirstValue("Frequency")=='quarterly':
        dates1=pd.date_range(seriesStartDate, seriesEndDate, freq="QS")
        freq = 'quarterly'

    elif metaData.GetFirstValue("Frequency")=='annual':
        print("in annual data")
        dates1=pd.date_range(seriesStartDate, seriesEndDate, freq="AS")
        freq = 'annual'

    elif metaData.GetFirstValue("Frequency")=='monthly':
        print("in monthly data")
        dates1=pd.date_range(seriesStartDate, seriesEndDate, freq="MS")
        freq = 'monthly'

    else:
        print(metaData.GetFirstValue("Frequency"))

    return(dates1, freq)


def sliceMacrobondCountryName_Exogenous(seriesName, varName):

    '''take last four characters of series name, this appears to be the country name,
       convert to human readable form.

       unfortunately, CPI uses a different identifier, so for CPI take the first three
       characters of a series name.
    '''

    # Todo if not in dictionary ...

    if varName != "CPI":
        country1=seriesName[-4:]

        dictCountry={

            "atmq": "Austria",
            "atam": "Austria",
            "atp1": "Austria",
            "athp": "Austria",

            "bemq": "Belguim",
            "beam": "Belguim",
            "bep1": "Belguim",
            "behp": "Belguim",

            "baam": "Bosnia",

            "bgmq": "Bulgaria",
            "bgam": "Bulgaria",
            "bgp1": "Bulgaria",
            "bghp": "Bulgaria",

            "hrmq": "Croatia",
            "hram": "Croatia",
            "hrp1": "Croatia",
            "hrhp": "Croatia",

            "cymq": "Cyprus",
            "cyam": "Cyprus",
            "cyp1": "Cyprus",
            "cyhp": "Cyprus",

            "czmq": "Czech Republic",
            "czam": "Czech Republic",
            "czp1": "Czech Republic",
            "czhp": "Czech Republic",

            "dkmq": "Denmark",
            "dkam": "Denmark",
            "dkp1": "Denmark",
            "dkhp": "Denmark",

            "eemq": "Estonia",
            "eeam": "Estonia",
            "eep1": "Estonia",
            "eehp": "Estonia",

            "eamq": "Euro Area",
            "eahp": "Euro Area",
            "eaam": "Euro Area",
            "eap1": "Euro Area",
            "ehap": "Euro Area",
            "euhp": "Euro Area",

            "fimq": "Finland",
            "fiam": "Finland",
            "fip1": "Finland",
            "fihp": "Finland",

            "frmq": "France",
            "fram": "France",
            "frp1": "France",
            "frhp": "France",

            "demq": "Germany",
            "deam": "Germany",
            "dep1": "Germany",
            "dehp": "Germany",

            "elmq": "Greece",
            "elam": "Greece",
            "elp1": "Greece",

            "humq": "Hungary",
            "huam": "Hungary",
            "hup1": "Hungary",
            "huhp": "Hungary",

            "ismq": "Iceland",
            "isam": "Iceland",
            "isp1": "Iceland",
            "ishp": "Iceland",

            "iemq": "Ireland",
            "ieam": "Ireland",
            "iep1": "Ireland",
            "iehp": "Ireland",

            "itmq": "Italy",
            "itam": "Italy",
            "itp1": "Italy",
            "ithp": "Italy",

            "lvmq": "Latvia",
            "lvam": "Latvia",
            "lvp1": "Latvia",
            "lvhp": "Latvia",

            "ltmq": "Lithuania",
            "ltam": "Lithuania",
            "ltpq": "Lithuania",
            "lthp": "Lithuania",
            "ltp1": "Lithuania",

            "lumq": "Luxembourg",
            "luam": "Luxembourg",
            "lup1": "Luxembourg",
            "luhp": "Luxembourg",

            "mtmq": "Malta",
            "mtam": "Malta",
            "mtp1": "Malta",
            "mthp": "Malta",

            "meam": "Montenego",

            "nlmq": "Netherlands",
            "nlam": "Netherlands",
            "nlp1": "Netherlands",
            "nlhp": "Netherlands",

            "mkam": "North Macedonia",

            "nomq": "Norway",
            "noam": "Norway",
            "nop1": "Norway",
            "nohp": "Norway",

            "plmq": "Poland",
            "plam": "Poland",
            "plp1": "Poland",
            "plhp": "Poland",

            "ptmq": "Portugal",
            "ptam": "Portugal",
            "ptp1": "Portugal",
            "pthp": "Portugal",

            "romq": "Romania",
            "roam": "Romania",
            "rop1": "Romania",
            "rohp": "Romania",

            "rsmq": "Serbia",
            "rsam": "Serbia",
            "rsp1": "Serbia",

            "skmq": "Slovakia",
            "skam": "Slovakia",
            "skp1": "Slovakia",
            "skhp": "Slovakia",

            "simq": "Slovenia",
            "siam": "Slovenia",
            "sip1": "Slovenia",
            "sihp": "Slovenia",

            "esmq": "Spain",
            "esam": "Spain",
            "esp1": "Spain",
            "eshp": "Spain",

            "semq": "Sweden",
            "seam": "Sweden",
            "sep1": "Sweden",
            "sehp": "Sweden",

            "chmq": "Switzerland",
            "cham": "Switzerland",
            "chp1": "Switzerland",

            "trhp": "Turkey",

            "ukmq": "United Kingdom",
            "ukam": "United Kingdom",
            "ukp1": "United Kingdom",
            "ukhp": "United Kingdom"

            }

        return(dictCountry[country1])

    else: # i.e., for CPI
        country1 = seriesName[:3]

        dictCountry = {

            "alp": "Albania",
            "atp": "Austria",
            "bap": "Bosnia",
            "bep": "Belguim",
            "bgp": "Bulgaria",
            "chp": "Switzerland",
            "cyp": "Cyprus",
            "czp": "Czech",
            "dep": "Germany",
            "dkp": "Denmark",
            "eep": "Estonia",
            "esp": "Spain",
            "eup": "Euro Area",
            "fip": "Finland",
            "frp": "France",
            "gbp": "United Kingdom",
            "grp": "Greece",
            "hrp": "Croatia",
            "hup": "Hungary",
            "iep": "Ireland",
            "isp": "Iceland",
            "itp": "Italy",
            "ltp": "Lithuania",
            "lup": "Luxembourg",
            "lvp": "Latvia",
            "mep": "Montenegro",
            "mkp": "North_Macedonia",
            "nlp": "Netherlands",
            "nop": "Norway",
            "plp": "Poland",
            "ptp": "Portugal",
            "rop": "Romania",
            "rsp": "Serbia",
            "sdp": "Sudan",
            "sep": "Sweden",
            "sip": "Slovenia",
            "skp": "Slovakia",
            "trp": "Turkey"
        }

        return (dictCountry[country1])


def sliceMacrobondExogenousName(seriesName, varName):

    '''remove last four characters of series name, this appears to be the sector name.
       again, CPI is different, and the 'center' of the series name needs to be plucked out.

    '''

    #Todo if not in dictionary ...

    if varName != 'CPI':
        sector1 = seriesName[:-4]
        dictExog={
            "clv10eurhabnsab1gq": "GDP_total",
            "clv15meurtotal": "Consumption",
            "thspernsapopnc": "Population",
            "totali15q": "Housing_Prices"
        }

        return (dictExog[sector1])

    else:
        sector1 = seriesName[-8:-4]
        dictExog={
            "pric": "CPI"
        }
        return (dictExog[sector1])

def plotOneSeries(seriesName, varName):

    values=getMacrobondSeries(seriesName, connectMacrobond())
    values=np.log(values)

    seriesDates, freq =collectSeriesMetaData(seriesName, connectMacrobond())

    countryName = sliceMacrobondCountryName_Exogenous(seriesName, varName)
    sectorName=sliceMacrobondExogenousName(seriesName, varName)

    df1=pd.DataFrame(values, index=seriesDates)
    plt.plot(df1)
    plt.title(sectorName + ": " + countryName)

    plt.savefig("figures/exogenous_" + sectorName + "_" + countryName + '.png')
    # Needed to
    plt.close()

    return(None)


keepTrack = []
# changing the rc parameters and plotting a line plot
plt.rcParams['figure.figsize'] = [18, 12]


def plotAllSectorSeries(seriesName):

    values=getMacrobondSeries(seriesName, connectMacrobond())
    values=np.log(values)

    seriesDates, freq =collectSeriesMetaData(seriesName, connectMacrobond())

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





#
# def deleteallFiles():
#     import os, shutil
#     folder = 'figures/'
#     for filename in os.listdir(folder):
#         file_path = os.path.join(folder, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))

# def collectData_monthly(seriesName, varName):
#
#     print(seriesName)
#
#     values = getMacrobondSeries(seriesName, connectMacrobond())
#
#     # create dataframe
#     seriesDates, freq = collectSeriesMetaData(seriesName, connectMacrobond())
#
#     df_values = pd.DataFrame(values, index=seriesDates)
#
#     sectorName = sliceMacrobondExogenousName(seriesName,varName)
#     countryName = sliceMacrobondCountryName_Exogenous(seriesName,varName)
#
#     df_values.columns = [countryName + "_" + sectorName]
#
#     return (df_values)
#
#
# def collectData_quarterly(seriesName, varName):
#
#     print(seriesName)
#
#     values = getMacrobondSeries(seriesName, connectMacrobond())
#
#     # create dataframe
#     seriesDates, freq = collectSeriesMetaData(seriesName, connectMacrobond())
#
#     df_values = pd.DataFrame(values, index=seriesDates)
#
#     sectorName = sliceMacrobondExogenousName(seriesName,varName)
#     countryName = sliceMacrobondCountryName_Exogenous(seriesName,varName)
#
#     df_values.columns = [countryName + "_" + sectorName]
#
#     return (df_values)
#
#
# def collectData_annual(seriesName, varName):
#
#     print(seriesName)
#
#     values = getMacrobondSeries(seriesName, connectMacrobond())
#
#     # dataframe
#     seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())
#
#     df_values = pd.DataFrame(values, index=seriesDates[0])
#
#     sectorName = sliceMacrobondExogenousName(seriesName, varName)
#     countryName = sliceMacrobondCountryName_Exogenous(seriesName, varName)
#
#     df_values.columns = [countryName + "_" + sectorName]
#
#     return (df_values)
#


def collectData_general(seriesName, varName, freq):
    print(seriesName)

    values = getMacrobondSeries(seriesName, connectMacrobond())

    # dataframe
    seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())

    if freq == "annual":  # no idea why this is necessary
        df_values = pd.DataFrame(values, index=seriesDates[0])
    else:
        df_values = pd.DataFrame(values, index=seriesDates[0])

    sectorName = sliceMacrobondExogenousName(seriesName, varName)
    countryName = sliceMacrobondCountryName_Exogenous(seriesName, varName)

    df_values.columns = [countryName + "_" + sectorName]

    return (df_values)

# deleteallFiles()
import datetime as dt

allData = pd.read_excel("data/macrobond_codes_international_sectormodel.xlsx")

all_quartData = []
all_yearData = []
all_monthlyData = []
def collectData_getFreq(data1):
    for index, row in data1.iterrows():
        seriesName = row['Macrobond_series_id']
        varName = row['Variable']
        seriesDates, freq = collectSeriesMetaData(seriesName, connectMacrobond())

        #plot data
        plotOneSeries(seriesName, varName)

        if freq == "quarterly":
            print("In quarterly")
            quartData = collectData_general(seriesName, varName, freq)
            all_quartData.append(quartData)
        elif freq == "annual":
            print("In annual")
            annualData = collectData_general(seriesName, varName, freq)
            all_yearData.append(annualData)
        elif freq == "monthly":
            print("In monthly")
            monthData= collectData_general(seriesName, varName, freq)
            all_monthlyData.append(monthData)
        else:
            print("freq not known")


data2 = collectData_getFreq(allData)

pd.concat(all_quartData, axis=1).to_csv("Exogenous_Quarterly.csv")
pd.concat(all_yearData, axis=1).to_csv("Exogenous_Yearly.csv")
pd.concat(all_monthlyData, axis=1).to_csv("Exogenous_Monthly.csv")






def readMacrobondDatatoDF_exogenous(dataNamesLocation, overwrite=True):

    ''' 1. if the sectorDataAll_exogenous file doesn't exist, create it
        2. if sectorDataAll_exogenous does exist, but you want to overwrite it, create it
        3. if sectorDataAll_exogenous does exist, and you dont want to overwrite it, dont do anything
    '''

    if (path.exists("data/sectorDataAll.csv") == False):
        allData = pd.read_excel(dataNamesLocation)
        individualSeries = collectData(allData)
        pd.concat(individualSeries, axis=1).to_csv("data/sectorDataAll_exogenous.csv")
        print("Created file data/sectorDataAll.csv")
    elif (path.exists("data/sectorDataAll.csv") == False) and (overwrite == True):
        allData = pd.read_excel(dataNamesLocation)
        individualSeries = collectData(allData)
        pd.concat(individualSeries, axis=1).to_csv("data/sectorDataAll_exogenous.csv")
        print("Created file data/sectorDataAll.csv")
    else:
        print("File /data/sectorDataAll_exogenous.csv exists")

dataNamesLocation ="data/macrobond_codes_international_sectormodel.xlsx"

readMacrobondDatatoDF_exogenous(dataNamesLocation, overwrite=True)


# # Create descriptive statistics per country, per series, save as a csv
#
# data1 = pd.read_csv("data/sectorDataAll.csv")
# print(data1.head())
#
# def getCountrySectorData(data, countryName):
#     getCols = [col for col in data.columns if countryName in col]
#     return(data[getCols])
#
#
# country1 = getCountrySectorData(data1, "Austria")
# country1.to_csv("tmp1.csv")
#
# import scipy
# #plt.plot(country1.iloc[:,0].dropna())
# #plt.show()
#
# countries1 = allCountries()
#
# allcountries = []
# for j in countries1:
#     country1 = getCountrySectorData(data1, j)/100000
#     rows = []
#     for i in range(1, country1.shape[1]):
#         colData = scipy.signal.detrend(country1.iloc[:,i].dropna())
#         sectorName = country1.columns[i]
#
#         mean_detrend = colData.mean()
#
#         std_detrend = colData.std()
#
#         # number of obs less than two deviations away from detrended mean
#         outlier_low = len(colData[colData < colData.mean() - 2 * colData.std()])
#
#         # number of obs greater than two deviations away from detrended mean
#         outlier_high = len(colData[colData > colData.mean() + 2 * colData.std()])
#
#         # trend
#         data = country1.iloc[:,i].dropna()
#         x = np.arange(0,len(data))
#         y = np.array(data)
#         z = np.polyfit(x,y,1)
#         trend = z[0]
#
#         avg_LastFiveYears = country1.iloc[-5:, i].dropna().mean()
#
#         rows.append([j, sectorName, avg_LastFiveYears, trend,  mean_detrend, std_detrend, outlier_low, outlier_high])
#     df = pd.DataFrame(rows, columns=["Country", "Sector", "5yr_Avg", "trend", "mean_detrend", "std_detrend", "outlier_low","outlier_high"])
#     allcountries.append(df)
#
# pd.concat(allcountries).to_csv("tmp6.csv")
