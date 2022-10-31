import pandas as pd

from base_functions import *
import pmdarima as pm

from statsmodels.tsa.stattools import adfuller, kpss

##### Should difference in our auto-Arima?

from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic import constr, PositiveInt


@dataclass
class timeseries:
    name: str
    index: str
    data:  float

def differenceOfNot(series: timeseries, ALPHA: int):
    '''
    Run multiple tests on a series to determine if differencing is necessary.

    :param series: time series
    :return: an integer indicating the needed difference, if any
    :reference: https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e

    todo: check if more than one difference is needed.
    '''

    pass





dataNamesLocation ="data/sectorDataAll.csv"
data1= pd.read_csv(dataNamesLocation, index_col=[0], infer_datetime_format=True)
data1.index = pd.to_datetime(data1.index)

values=data1.iloc[:, 10].dropna()

print(values.name)
print(values.index.dtype)

# plt.plot(values)
# plt.show()

ALPHA = 0.01

# Augmented Dickey-Fuller ADF
# Kwiatkowski-Phillips-Schmidt-Shin KPSS
# Osborn-Chui-Smith-Birchenhall OCSB for seasonal differencing
# Canova-Hansen CH for seasonal differencing

# pmdarima - ADF test - should we difference?
# ADF null hypothesis: the series is not stationary
def ADF_pmd(x):
    adf_test = pm.arima.stationarity.ADFTest(alpha=ALPHA)
    res = adf_test.should_diff(x)
    conclusion = "non-stationary" if res[0] > ALPHA else "stationary"
    resdict = {"should we difference? ":res[1], "p-value ":res[0], "conclusion":conclusion}
    return resdict

# call the ADF test:
resADF = ADF_pmd(values)

# # print test result dictionary:
# print("ADF test result for original data:")
# [print(key, ":", value) for key,value in resADF.items()]
#
# # pmdarima - KPSS test -  should we difference?
# # null hypothesis: the series is at least trend stationary
# def KPSS_pmd(x):
#     kpss_test = pm.arima.stationarity.KPSSTest(alpha=ALPHA)
#     res = kpss_test.should_diff(x)
#     conclusion = "not stationary" if res[0] <= ALPHA else "stationary"
#     resdict = {"should we difference? ":res[1], "p-value ":res[0], "conclusion":conclusion}
#     return resdict
#
# # call the KPSS test:
# resKPSS = KPSS_pmd(values)
#
# # print test result dictionary:
# print("KPSS test result for original data:")
# [print(key, ":", value) for key,value in resKPSS.items()]
#
# # compare ADF and KPSS result
# test_values = zip(resADF.values(), resKPSS.values())
# dict_tests = dict(zip(resADF.keys(), test_values))
# df_tests = pd.DataFrame().from_dict(dict_tests).transpose()
# df_tests.columns = ["ADF", "KPSS"]
# print("Stationarity test results for original data:")
# df_tests
#
# # pmdarima also offers methods that suggest the order of first differencing, based on either ADF or the KPSS test
#
# n_adf = pm.arima.ndiffs(values, test="adf")
# n_kpss = pm.arima.ndiffs(values, test="kpss")
# n_diffs = {"ADF ndiff":n_adf, "KPSS ndiff":n_kpss}
# print("recommended order of first differencing for original data:")
# [print(key, ":", value) for key,value in n_diffs.items()]
#
#
#
# # We apply the ADF and KPSS tests of statsmodels.stattools:
#
#
# # statsmodels - ADF test
# # null hypothesis: There is a unit root and the series is NOT stationary
# # Low p-values are preferable
# # get results as a dictionary
# def ADF_statt(x):
#      adf_test = adfuller(x, autolag="aic")
#      t_stat, p_value, _, _, _, _  = adf_test
#      conclusion = "non-stationary (unit root)" if p_value > ALPHA else "stationary"
#      res_dict = {"ADF statistic":t_stat, "p-value":p_value, "should we difference?": (p_value > ALPHA), "conclusion": conclusion}
#      return res_dict
#
#
# # call the ADF test:
# resADF = ADF_statt(values)
#
# # print dictionary of test results:
# print("ADF test result for original data:")
# # [print(key, ":", f'{value:.3f}') for key,value in resADF.items()]
# [print(key, ":", value) for key,value in resADF.items()]
#
# # statsmodels - KPSS test
# # more detailed output than pmdarima
# # null hypothesis: There series is (at least trend-)stationary
# # High p-values are preferable
# # get results as a dictionary
# def KPSS_statt(x):
#      kpss_test = kpss(x)
#      t_stat, p_value, _, critical_values  = kpss_test
#      conclusion = "stationary" if p_value > ALPHA else "not stationary"
#      res_dict = {"KPSS statistic":t_stat, "p-value":p_value, "should we difference?": (p_value < ALPHA), "conclusion": conclusion}
#      return res_dict
#
#
# # call the KPSS test:
# resKPSS = KPSS_statt(values)
#
# # print dictionary of test results:
# # [print(key, ":", f'{value:.3f}') for key,value in resKPSS.items()]
# print("KPSS test result for original data:")
# [print(key, ":", value) for key,value in resKPSS.items()]
#
#
# ####################################################
#
# from pmdarima.preprocessing import BoxCoxEndogTransformer
# from pmdarima.pipeline import Pipeline
#
# # Plot an auto-correlation:
# #pm.plot_acf(pm.c(values))
# #
# model1 = pm.auto_arima(values, start_p=0, start_q=0,
#                              max_p=4, max_q=4, m=4,
#                              start_P=0, seasonal=True,
#                              d=1, D=1, trace=False,
#                              error_action='ignore',  # don't want to know if an order does not work
#                              suppress_warnings=True,  # don't want convergence warnings
#                              stepwise=True)  # set to stepwise
#
# print(model1.summary())
#
# plt.plot(model1.resid())
# plt.show()
#
# from pmdarima.arima import CHTest
# import numpy as np
#
#
# print(CHTest(m=4).estimate_seasonal_differencing_term(values))
#



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