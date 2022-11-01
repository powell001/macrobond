from base_functions import *


def sliceMacrobondCountryName_Exogenous(seriesName, varName):
    """
        take last four characters of series name, this appears to be the country name,
        convert to human readable form.

        unfortunately, CPI uses a different identifier, so for CPI take the first three
        characters of a series name.
    """

    if varName != "CPI":
        country1 = seriesName[-4:]

        dictCountry = {

            "atmq": "Austria",
            "atam": "Austria",
            "atp1": "Austria",
            "athp": "Austria",

            "bemq": "Belgium",
            "beam": "Belgium",
            "bep1": "Belgium",
            "behp": "Belgium",

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
            "eaam": "Euro Area",
            "eap1": "Euro Area",
            "euhp": "Euro Area",
            "eahp": "Euro Area",

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

            "meam": "Montenegro",

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
        return dictCountry[country1]
    else:  # i.e., for CPI
        country1 = seriesName[:3]

        dictCountry = {

            "alp": "Albania",
            "atp": "Austria",
            "bap": "Bosnia",
            "bep": "Belgium",
            "bgp": "Bulgaria",
            "chp": "Switzerland",
            "cyp": "Cyprus",
            "czp": "Czech Republic",
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
            "mkp": "North Macedonia",
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

        return dictCountry[country1]


def sliceMacrobondExogenousName(seriesName, varName):
    """
        remove last four characters of series name, this appears to be the sector name.
        again, CPI is different, and the 'center' of the series name needs to be plucked out.
    """

    if varName != 'CPI':
        sector1 = seriesName[:-4]
        dictExog = {
            "clv10eurhabnsab1gq": "GDP_total",
            "clv15meurtotal": "Consumption",
            "thspernsapopnc": "Population",
            "totali15q": "Housing_Prices"
        }

        return dictExog[sector1]

    else:
        sector1 = seriesName[-8:-4]
        dictExog = {
            "pric": "CPI",
            "ric0": "CPI"
        }
        return dictExog[sector1]


def collectData_general(seriesName, varName, freq):
    print(seriesName)

    values = getMacrobondSeries(seriesName, connectMacrobond())
    seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())

    if freq == "annual":  # no idea why this is necessary
        df_values = pd.DataFrame(values, index=seriesDates[0])
    else:
        df_values = pd.DataFrame(values, index=seriesDates[0])

    sectorName = sliceMacrobondExogenousName(seriesName, varName)
    countryName = sliceMacrobondCountryName_Exogenous(seriesName, varName)

    df_values.columns = [countryName + "_" + sectorName]

    return df_values


def collectData_getFreq(data1):
    all_quartData = []
    all_yearData = []
    all_monthlyData = []

    for index, row in data1.iterrows():
        seriesName = row['Macrobond_series_id']
        varName = row['Variable']
        seriesDates, freq = collectSeriesMetaData(seriesName, connectMacrobond())

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
            monthData = collectData_general(seriesName, varName, freq)
            all_monthlyData.append(monthData)
        else:
            print("freq not known")

    return all_quartData, all_yearData, all_monthlyData

def dataCheckSeriesNames(all_quartData2, all_yearData2, all_monthlyData2):
    # quarterlhy
    data10 = pd.concat(all_quartData2, axis=1)
    data10.index = pd.DatetimeIndex(data10.index)
    data10.to_csv("data/ProcessedData/Exogenous_Quarterly.csv")
    # yearly
    data11 = pd.concat(all_yearData2, axis=1)
    data11.index = pd.DatetimeIndex(data11.index)
    data11.to_csv("data/ProcessedData/Exogenous_Yearly.csv")
    # monthly
    data12 = pd.concat(all_monthlyData2, axis=1)
    data12.index = pd.DatetimeIndex(data12.index)
    data12.to_csv("data/ProcessedData/Exogenous_Monthly.csv")

    count_exog = allData[['Country', 'Variable']].groupby("Country").count().sort_values(by=["Country"])

    countries_quarterly = [x.split("_")[0] for x in data10.columns]
    countries_yearly = [x.split("_")[0] for x in data11.columns]
    countries_monthly = [x.split("_")[0] for x in data12.columns]

    allExogCountry = countries_quarterly + countries_yearly + countries_monthly

    exog_dict = {i: allExogCountry.count(i) for i in allExogCountry}
    exog_in_code = pd.DataFrame.from_dict(exog_dict, orient='index').sort_index()

    check_count = pd.merge(count_exog, exog_in_code, left_index=True, right_index=True)
    check_count.columns = ['countExcel', 'countCode']
    check_count['diff'] = check_count['countExcel'] - check_count['countCode']

    assert all(check_count['diff'].tolist())==0, "There are differences between the Excel sheet and the processed data"

    print(check_count)


deleteallFiles("exogenous")
allData = pd.read_excel("data/OriginalData/macrobond_codes_international_sectormodel.xlsx")
all_quartData1, all_yearData1, all_monthlyData1 = collectData_getFreq(allData)
dataCheckSeriesNames(all_quartData1, all_yearData1, all_monthlyData1)
