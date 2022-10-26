import win32com.client
import matplotlib.pyplot as plt
import pandas as pd
import pytest


#https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test


c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database

s = d.FetchOneSeries("usgdp")

raw1 = pd.read_excel("macrobond_codes_international_sectormodel.xlsx")

countries=raw1["Country"]
print(countries)

#print(raw1[raw1.Country=="Sweden"])
ls1 = []
countryList = []
countryDFList = []
for i in countries:
    print(i)
    #country = raw1.iloc[i, 1]
    # if country in countryList:
    #     break
    # countryList.append(country)

    countryData = raw1[raw1.Country == i]

    print(countryData)

    data1 = []
    for j in range(0,countryData.shape[0]):
        macbondCode = countryData.Macrobond_series_id.iloc[j]
        print(macbondCode)
        Variable = countryData.Variable.iloc[j]
        print(Variable)


        s = d.FetchOneSeries(macbondCode)
        print(len(s.Values))
        data1.append(pd.DataFrame(s.Values))

    countryDf = pd.concat(data1, axis=1, ignore_index=True)
    countryDf.columns=countryData['Variable']
    countryDf['Country']=countryData['Country']
    countryDFList.append(countryDf)


zz=pd.concat(countryDFList)
zz.to_csv("tmp.csv")

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
