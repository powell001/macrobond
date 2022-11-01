from base_functions import *

'''
Set of basic functions to load data from Macrobond, with input information derived from a Excel sheet.  
The code requires uses the headers from the Excel file (so if these change, the code breaks.
The output is currently one csv file that is saved locally.   
'''


def connectMacrobond():
    """
    Function is dependent on an API from Macrobond, if that changes this code will break.
    :return: Macrobond connection
    """

    connection = win32com.client.Dispatch("Macrobond.Connection")
    return connection.Database


def getMacrobondSeries(myseries: str, connect):
    """
    Given the name of a Macrobond series, return it values
    :param myseries: name of desired time series
    :param connect: connection string
    :return: values of time series
    """

    data1 = connect.FetchOneSeries(myseries)
    return data1.Values


def collectSeriesMetaData(myseries: str, connection):
    """
    Function which returns dates of associated time series, other meta data is available.
    :param myseries: name of desired time series
    :param connection: connectMacrobond()
    :return: dates of series
    """

    data1 = connection.FetchOneSeries(myseries)

    metaData = data1.Metadata
    seriesStartDate = pd.to_datetime(data1.DatesAtStartOfPeriod[0].strftime('%Y-%m-%d'))
    seriesEndDate = pd.to_datetime(data1.DatesAtStartOfPeriod[-1].strftime('%Y-%m-%d'))

    mydates = ""
    if metaData.GetFirstValue("Frequency") == 'quarterly':
        mydates = pd.date_range(seriesStartDate, seriesEndDate, freq="QS")
    else:
        print(metaData.GetFirstValue("Frequency"))
    return mydates


def sliceMacrobondCountryName(seriesName: str):
    """
    take last four characters of series name, this appears to be the country name
    :param: Macrobond series name
    :return: human readable version of series name
    """

    country1 = seriesName[-4:]
    dictCountry = {
        "ata1": "Austria",
        "bea1": "Belgium",
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
    return dictCountry[country1]


def sliceMacrobondSectorName(seriesName):
    """
    remove last four characters of series name, this appears to be the sector name
    :param: Macrobond series name
    :return: human readable version of sector name
    """

    # this uniquely defines the series
    sector1 = seriesName[:-4]

    dictSector = {
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
    return dictSector[sector1]


allSeries = []


def collectData(Excel_data: pd.DataFrame()):
    """
    Function loops through all rows of Excel file, collects the values, adds human readable name and the
    dates.

    :param Excel_data: Excel file location
    :return: pandas dataframe containing all of the macrobond data
    """

    for index, row in Excel_data.iterrows():
        seriesName = row['Macrobond_series_id']

        values = getMacrobondSeries(seriesName, connectMacrobond())

        # dataframe
        seriesDates = collectSeriesMetaData(seriesName, connectMacrobond())
        df_values = pd.DataFrame(values, index=seriesDates)

        sectorName = sliceMacrobondSectorName(seriesName)
        countryName = sliceMacrobondCountryName(seriesName)

        df_values.columns = [countryName + "_" + sectorName]

        allSeries.append(df_values)
    return allSeries


def endog_checks(excel, endo_data):
    # Do we have a column for each row?
    numberColumns = len(endo_data.columns)
    assert numberColumns == excel.shape[0]

    # Original data: same number of observations for both countries and sectors?
    count_country = excel[['Country', 'Sector']].groupby(['Sector']).count()
    assert all(count_country['Country'].tolist()), "Data incomplete, count of countries differ"
    count_sectors = excel[['Country', 'Sector']].groupby(['Country']).count()
    assert all(count_sectors['Sector'].tolist()), "Data incomplete, count of sectors differ"


########################################
########################################

excel_source = "data/OriginalData/"
processed_data = "data/ProcessedData/"

allData_Excel = pd.read_excel(excel_source + "macrobond_series_eu_industries.xlsx")
data = collectData(allData_Excel)
endogenous_data_df = pd.concat(data, axis=1)
endogenous_data_df.index = pd.to_datetime(endogenous_data_df.index)
endogenous_data_df.to_csv(processed_data + "Endogenous_data_df.csv")

endog_checks(allData_Excel, endogenous_data_df)
