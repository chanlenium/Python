Industry DB for the KCIS Enterpirse Finance Analytics System
=============

# Data scraping using Python Colab

## What is [Python](https://en.wikipedia.org/wiki/Python_(programming_language), "python wiki link") language?
[![Python](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/729px-Python_logo_and_wordmark.svg.png)](https://www.python.org/)

### Programming language developed with intuitive and concise grammar, gaining the most popularity 
(Reference: [tiobe-index](https://www.tiobe.com/tiobe-index/, "tiobe-index link"))
### Special features of Python

<ol type="1">
  <li><b>Script language</b></li>
  Python is a Script language in which interpreters read source codes line by line at a run-time and execute it immediately without a compilation.<br>
  This makes it easy to code while immediately viewing and modifying the execution results.<br>
  <br>
  <li><b>Dynamic typing</b></li>
  Python does not specify the datatype of a variable, but can specify a value simply by declaring it.<br> 
  The data type of the variable is determined when the code is executed.<br>
  <br>
  <li><b>General-purpose programming language</b></li>
  A general-purpose programming language (GPL) is a programming language designed to be used for building software in a wide variety of application domains, across a multitude of hardware configurations and operating systems. 
</ol>


## Python editor [Colab](https://colab.research.google.com/?hl=ko, "Colab link") (Colaboratory)
* Can make python script and excute it in browser immediately
* No need to install a developing configuration
* Use virtual CPU/Memory for free

## Let's dive in [Colab](https://colab.research.google.com/?hl=ko, "Colab link")!!
[<img src="https://mcgrawect.princeton.edu/wp-content/uploads/2020/10/colab_lg.png" width="600">](https://colab.research.google.com/)



# Getting Started Data scraping using Python Colab
## (Goal) Scraping [ECOS Open API](https://ecos.bok.or.kr/api/) data and making excel file

|No|Column ID|Column Name|PK|
|:--:|:---|:---|:--:|
|1|STD_YM|기준년월|Y|
|2|GDP_WON_SIL|GDP(원계열, 실질)|N|
|3|GDP_WON_MYUNG|GDP(원계열, 명목)|N|
|4|GDP_GAE_SIL|GDP(계절조정, 실질)|N|
|5|GDP_GAE_MYUNG|GDP(계절조정, 명목)|N|
|6|INDU_GDP_WON|GDP 성장률(원계열, 실질) - 전년동기비|N|
|7|INDU_GDP_GAE|GDP 성장률(계절조정, 실질) - 전기비|N|
|8|INDU_OPERATING_WON|전산업생산지수_농림어업제외(원계열)|N|
|9|INDU_OPERATING_GAE|전산업생산지수_농림어업제외(계절조정)|N|
|10|INDU_MANU_OPER_WON|제조업 생산지수(원계열)|N|
|11|INDU_MANU_OPER_GAE|제조업 생산지수(계절조정)|N|
|12|INDU_SERV_OPER_GYUNG|서비스업 생산지수(경상지수)|N|
|13|INDU_SERV_OPER_BUL|서비스업 생산지수(불변지수)|N|
|14|INDU_SERV_OPER_GAE|서비스업 생산지수(계절조정지수)|N|
|15|INDU_CONSALE_GYUNG|소매업태별 판매액지수(경상지수)|N|
|16|INDU_CONSALE_BUL|소매업태별 판매액지수(불변지수)|N|
|17|INDU_CONSALE_GAE|소매업태별 판매액지수(계절조정지수)|N|
|18|EXCHANGE_WON_DOL|원달러 환율|N|
|19|INTERATE_RATE_KORIBOR3|시장금리 (KORIBOR 3개월)|N|
|20|MANU_PRICE|물가 - 생산자 물가지수(에너지, 식료품 제외)|N|
|21|OIL_PRICE_DUBAI|유가(Dubai)|N|


**Step 1. Get an authentication key for ECOS Open API service**

Sign up(or Sing in) and request to issue an authentication key

<img src="https://wikidocs.net/images/page/144514/kor02.png" width="600">
  
**Step 2. Search OPEN API and check how to use it**

Reference: [Development Specification Document](https://ecos.bok.or.kr/api/#/DevGuide/DevSpeciflcation) and [Statistical Code Search](https://ecos.bok.or.kr/api/#/DevGuide/StatisticalCodeSearch)

```
(Sample Example)
https://ecos.bok.or.kr/api/StatisticSearch/sample/xml/kr/1/10/200Y001/A/2015/2021/10101/?/?/?
```
|No|Coulum ID|Column Name|PK|ECOS API Path|
|:--:|:---|:---|:--:|:--|
|1|STD_YM|기준년월|Y||
|2|GDP_WON_SIL|GDP(원계열, 실질)|N|2.1.2.1.4. 경제활동별 GDP 및 GNI(원계열, 실질, 분기) : [200Y006][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]|
|3|GDP_WON_MYUNG|GDP(원계열, 명목)|N|2.1.2.1.3. 경제활동별 GDP 및 GNI(원계열, 명목, 분기) : [200Y005][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]|
|4|GDP_GAE_SIL|GDP(계절조정, 실질)|N|2.1.2.1.2. 경제활동별 GDP 및 GNI(계절조정, 실질, 분기) : [200Y004][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]|
|5|GDP_GAE_MYUNG|GDP(계절조정, 명목)|N|2.1.2.1.1. 경제활동별 GDP 및 GNI(계절조정, 명목, 분기) : [200Y003][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]|
|6|INDU_GDP_WON|GDP 성장률(원계열, 실질) - 전년동기비|N|2.1.1.2. 주요지표(분기지표) : [200Y002][Q]   /   국내총생산(GDP)(실질, 원계열, 전년동기비) [10211][%]|
|7|INDU_GDP_GAE|GDP 성장률(계절조정, 실질) - 전기비|N|2.1.1.2. 주요지표(분기지표) : [200Y002][Q]   /   국내총생산(GDP)(실질, 계절조정, 전기비) [10111][%]|
|8|INDU_OPERATING_WON|전산업생산지수_농림어업제외(원계열)|N|8.1.4. 전산업생산지수(농림어업제외) : [901Y033][M]  /  전산업생산지수(농림어업 제외) : [A00][2015=100]  /  원계열 : [1]|
|9|INDU_OPERATING_GAE|전산업생산지수_농림어업제외(계절조정)|N|8.1.4. 전산업생산지수(농림어업제외) : [901Y033][M]  /  전산업생산지수(농림어업 제외) : [A00][2015=100]  /  계절조정 : [2]|
|10|INDU_MANU_OPER_WON|제조업 생산지수(원계열)|N|8.3.1. 광업/제조업 - 산업별 생산/출하/재고 지수 : [901Y032][M]  /  제조업 : [I11AC][2015=100]  /  생산지수(원지수) : [1]|
|11|INDU_MANU_OPER_GAE|제조업 생산지수(계절조정)|N|8.3.1. 광업/제조업 - 산업별 생산/출하/재고 지수 : [901Y032][M]  /  제조업 : [I11AC][2015=100]  /  생산지수(계절조정) : [2]|
|12|INDU_SERV_OPER_GYUNG|서비스업 생산지수(경상지수)|N|8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  경상지수 : [1]|
|13|INDU_SERV_OPER_BUL|서비스업 생산지수(불변지수)|N|8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  불변지수 : [2]|
|14|INDU_SERV_OPER_GAE|서비스업 생산지수(계절조정지수)|N|8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  계절조정지수 : [3]|
|15|INDU_CONSALE_GYUNG|소매업태별 판매액지수(경상지수)|N|8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  경상지수 : [I74A]|
|16|INDU_CONSALE_BUL|소매업태별 판매액지수(불변지수)|N|8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  불변지수 : [I74B]|
|17|INDU_CONSALE_GAE|소매업태별 판매액지수(계절조정지수)|N|8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  계절조정지수 : [I74C]|
|18|EXCHANGE_WON_DOL|원달러 환율|N|3.1.2.1. 주요국 통화의 대원화환율 : [731Y004][M]   /   원/미국달러(매매기준율) : [0000001][원]   /   평균자료 : [0000100]|
|19|INTERATE_RATE_KORIBOR3|시장금리 (KORIBOR 3개월)|N|1.3.2.2 시장금리(월,분기,년) : [721Y001][M]   /   KORIBOR(3개월) : [1025000][연%]|
|20|MANU_PRICE|물가 - 생산자 물가지수(에너지, 식료품 제외)|N|4.1.1.2. 생산자물가지수(특수분류) : [404Y015][M]   /   식료품에너지이외 : [S520AA][2015=100]|
|21|OIL_PRICE_DUBAI|유가(Dubai)|N|9.1.6.3. 국제상품가격 : [902Y003][M]   /   Dubai(현물) : [4010102][U$/bbl]|

## Open Colab and typing scripts to scrap Open API data

### Scraping a single data column

**Step 1. Import library**
```
import requests
import pandas as pd
from datetime import date
```

**Step 2. Request and get data from URL**
```
url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/200Y006/Q/2020Q1/2022Q3/1400'
r = requests.get(url)
```

**Step 3. Parsing url data to [JSON](https://en.wikipedia.org/wiki/JSON, "Json wiki link") format and coverting json to pandas dataframe format**
```
jo = r.json()
df = pd.DataFrame(jo['StatisticSearch']['row']) # Convert json data to dataframe
df = df[['TIME', 'DATA_VALUE']] # Select only the desired columns
```

**Step 4. Rename column and convert data type**
```
df.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
df['STD_YM'] = df['STD_YM'].str.replace('Q1$', '03', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q2$', '06', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q3$', '09', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q4$', '12', regex=True)
```

**Step 5. Set Index and export excel file**
```
df = df.set_index('STD_YM')
today = date.today()
df.to_excel(f'{today}_EcosExample.xlsx')
```

### Scraping two data columns and merging them (Define helper function and Join columns)
**Step 1. Raw coding for scaping two data columns**
```
## GDP(원계열, 실질)
url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/200Y006/Q/2010Q1/2022Q3/1400'
r = requests.get(url)
jo = r.json()
GDP_WON_SIL = pd.DataFrame(jo['StatisticSearch']['row'])
GDP_WON_SIL = GDP_WON_SIL[['TIME', 'DATA_VALUE']]
GDP_WON_SIL.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
GDP_WON_SIL.rename(columns = {'DATA_VALUE':'GDP_WON_SIL'}, inplace = True)
GDP_WON_SIL['DATA_VALUE'] = pd.to_numeric(GDP_WON_SIL['DATA_VALUE'])
GDP_WON_SIL['STD_YM'] = GDP_WON_SIL['STD_YM'].str.replace('Q1$', '03', regex=True)
GDP_WON_SIL['STD_YM'] = GDP_WON_SIL['STD_YM'].str.replace('Q2$', '06', regex=True)
GDP_WON_SIL['STD_YM'] = GDP_WON_SIL['STD_YM'].str.replace('Q3$', '09', regex=True)
GDP_WON_SIL['STD_YM'] = GDP_WON_SIL['STD_YM'].str.replace('Q4$', '12', regex=True)
GDP_WON_SIL = GDP_WON_SIL.set_index('STD_YM')
  
## 제조업 생산지수(원계열)
url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/901Y032/M/201001/202209/I11AC/1'
r = requests.get(url)
jo = r.json()
INDU_MANU_OPER_WON = pd.DataFrame(jo['StatisticSearch']['row'])
INDU_MANU_OPER_WON = INDU_MANU_OPER_WON[['TIME', 'DATA_VALUE']]
INDU_MANU_OPER_WON.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
INDU_MANU_OPER_WON.rename(columns = {'DATA_VALUE':'INDU_MANU_OPER_WON'}, inplace = True)
INDU_MANU_OPER_WON['DATA_VALUE'] = pd.to_numeric(INDU_MANU_OPER_WON['DATA_VALUE'])
INDU_MANU_OPER_WON = INDU_MANU_OPER_WON.set_index('STD_YM')
```

**Step 2. Bind common parts(URL call process) and Make helper function**
```
def ecosApiCall(url_tail):
  url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{url_tail}'
  r = requests.get(url)
  jo = r.json()
  df = pd.DataFrame(jo['StatisticSearch']['row'])
  df = df[['TIME', 'DATA_VALUE']]
  df.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
  df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
  df['STD_YM'] = df['STD_YM'].str.replace('Q1$', '03', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q2$', '06', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q3$', '09', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q4$', '12', regex=True)
  df = df.set_index('STD_YM')
  return df
  
# (1) GDP(원계열, 실질)
# 2.1.2.1.4. 경제활동별 GDP 및 GNI(원계열, 실질, 분기) : [200Y006][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y006/Q/2010Q1/2020Q4/1400
GDP_WON_SIL = ecosApiCall(f"200Y006/Q/2010Q1/{queryYYYYQQ}/1400")
GDP_WON_SIL.rename(columns = {'DATA_VALUE':'GDP_WON_SIL'}, inplace = True)

# (9) 제조업 생산지수(원계열)
# 8.3.1. 광업/제조업 - 산업별 생산/출하/재고 지수 : [901Y032][M]  /  제조업 : [I11AC][2015=100]  /  생산지수(원지수) : [1]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y032/M/201001/202209/I11AC/1
INDU_MANU_OPER_WON = ecosApiCall(f"901Y032/M/201001/{queryYYYYMM}/I11AC/1")
INDU_MANU_OPER_WON.rename(columns = {'DATA_VALUE':'INDU_MANU_OPER_WON'}, inplace = True)
```

**Step 3. Merge columns**
 ```
 Merged_TB = pd.merge(left = GDP_WON_SIL, right = INDU_MANU_OPER_WON, left_index = True, right_index = True, how = "outer")
 ```
 
### Scraping more than two data columns and merging them (Loop)
**Step 1. Scrap multiple data columns using helper function**
```
def ecosApiCall(url_tail):
  url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/{url_tail}'
  r = requests.get(url)
  jo = r.json()
  df = pd.DataFrame(jo['StatisticSearch']['row'])
  df = df[['TIME', 'DATA_VALUE']]
  df.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
  df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
  df['STD_YM'] = df['STD_YM'].str.replace('Q1$', '03', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q2$', '06', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q3$', '09', regex=True)
  df['STD_YM'] = df['STD_YM'].str.replace('Q4$', '12', regex=True)
  df = df.set_index('STD_YM')
  return df

# (1) GDP(원계열, 실질)
# 2.1.2.1.4. 경제활동별 GDP 및 GNI(원계열, 실질, 분기) : [200Y006][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y006/Q/2010Q1/2020Q4/1400
GDP_WON_SIL = ecosApiCall(f"200Y006/Q/2010Q1/{queryYYYYQQ}/1400")
GDP_WON_SIL.rename(columns = {'DATA_VALUE':'GDP_WON_SIL'}, inplace = True)

# (2) GDP(원계열, 명목)
# 2.1.2.1.3. 경제활동별 GDP 및 GNI(원계열, 명목, 분기) : [200Y005][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y005/Q/2010Q1/2020Q4/1400
GDP_WON_MYUNG = ecosApiCall(f"200Y005/Q/2010Q1/{queryYYYYQQ}/1400")
GDP_WON_MYUNG.rename(columns = {'DATA_VALUE':'GDP_WON_MYUNG'}, inplace = True)

# (3) GDP(계절조정, 실질)
# 2.1.2.1.2. 경제활동별 GDP 및 GNI(계절조정, 실질, 분기) : [200Y004][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y004/Q/2010Q1/2020Q4/1400
GDP_GAE_SIL = ecosApiCall(f"200Y004/Q/2010Q1/{queryYYYYQQ}/1400")
GDP_GAE_SIL.rename(columns = {'DATA_VALUE':'GDP_GAE_SIL'}, inplace = True)

# (4) GDP(계절조정, 명목)
# 2.1.2.1.1. 경제활동별 GDP 및 GNI(계절조정, 명목, 분기) : [200Y003][Q]   /   국내총생산(시장가격, GDP) : [1400][십억원]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y004/Q/2010Q1/2020Q4/1400
GDP_GAE_MYUNG = ecosApiCall(f"200Y003/Q/2010Q1/{queryYYYYQQ}/1400")
GDP_GAE_MYUNG.rename(columns = {'DATA_VALUE':'GDP_GAE_MYUNG'}, inplace = True)

# (5) GDP 성장률(원계열, 실질) - 전년동기비
# 2.1.1.2. 주요지표(분기지표) : [200Y002][Q]   /   국내총생산(GDP)(실질, 원계열, 전년동기비) [10211][%]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y002/Q/2010Q1/2020Q4/10211
INDU_GDP_WON = ecosApiCall(f"200Y002/Q/2010Q1/{queryYYYYQQ}/10211")
INDU_GDP_WON.rename(columns = {'DATA_VALUE':'INDU_GDP_WON'}, inplace = True)

# (6) GDP 성장률(계절조정, 실질) - 전기비
# 2.1.1.2. 주요지표(분기지표) : [200Y002][Q]   /   국내총생산(GDP)(실질, 계절조정, 전기비) [10111][%]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/200Y002/Q/2010Q1/2020Q4/10111
INDU_GDP_GAE = ecosApiCall(f"200Y002/Q/2010Q1/{queryYYYYQQ}/10111")
INDU_GDP_GAE.rename(columns = {'DATA_VALUE':'INDU_GDP_GAE'}, inplace = True)

# (7) 전산업생산지수_농림어업제외(원계열)
# 8.1.4. 전산업생산지수(농림어업제외) : [901Y033][M]  /  전산업생산지수(농림어업 제외) : [A00][2015=100]  /  원계열 : [1]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y033/M/201001/202209/A00/1
INDU_OPERATING_WON = ecosApiCall(f"901Y033/M/201001/{queryYYYYMM}/A00/1")
INDU_OPERATING_WON.rename(columns = {'DATA_VALUE':'INDU_OPERATING_WON'}, inplace = True)

# (8) 전산업생산지수_농림어업제외(계절조정)
# 8.1.4. 전산업생산지수(농림어업제외) : [901Y033][M]  /  전산업생산지수(농림어업 제외) : [A00][2015=100]  /  계절조정 : [2]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y033/M/201001/202209/A00/2
INDU_OPERATING_GAE = ecosApiCall(f"901Y033/M/201001/{queryYYYYMM}/A00/2")
INDU_OPERATING_GAE.rename(columns = {'DATA_VALUE':'INDU_OPERATING_GAE'}, inplace = True)

# (9) 제조업 생산지수(원계열)
# 8.3.1. 광업/제조업 - 산업별 생산/출하/재고 지수 : [901Y032][M]  /  제조업 : [I11AC][2015=100]  /  생산지수(원지수) : [1]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y032/M/201001/202209/I11AC/1
INDU_MANU_OPER_WON = ecosApiCall(f"901Y032/M/201001/{queryYYYYMM}/I11AC/1")
INDU_MANU_OPER_WON.rename(columns = {'DATA_VALUE':'INDU_MANU_OPER_WON'}, inplace = True)

# (10) 제조업 생산지수(계절조정)
# 8.3.1. 광업/제조업 - 산업별 생산/출하/재고 지수 : [901Y032][M]  /  제조업 : [I11AC][2015=100]  /  생산지수(계절조정) : [2]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y032/M/201001/202209/I11AC/2
INDU_MANU_OPER_GAE = ecosApiCall(f"901Y032/M/201001/{queryYYYYMM}/I11AC/2")
INDU_MANU_OPER_GAE.rename(columns = {'DATA_VALUE':'INDU_MANU_OPER_GAE'}, inplace = True)

# (11) 서비스업 생산지수(경상지수)
# 8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  경상지수 : [1]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y038/M/201001/202209/I51A/1
INDU_SERV_OPER_GYUNG = ecosApiCall(f"901Y038/M/201001/{queryYYYYMM}/I51A/1")
INDU_SERV_OPER_GYUNG.rename(columns = {'DATA_VALUE':'INDU_SERV_OPER_GYUNG'}, inplace = True)

# (12) 서비스업 생산지수(불변지수)
# 8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  불변지수 : [2]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y038/M/201001/202209/I51A/2
INDU_SERV_OPER_BUL = ecosApiCall(f"901Y038/M/201001/{queryYYYYMM}/I51A/2")
INDU_SERV_OPER_BUL.rename(columns = {'DATA_VALUE':'INDU_SERV_OPER_BUL'}, inplace = True)

# (13) 서비스업 생산지수(계절조정지수)
# 8.5.1. 서비스업 - 산업별 서비스업생산지수 : [901Y038][M]  /  총지수 : [I51A][2015=100]  /  계절조정지수 : [3]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y038/M/201001/202209/I51A/3
INDU_SERV_OPER_GAE = ecosApiCall(f"901Y038/M/201001/{queryYYYYMM}/I51A/3")
INDU_SERV_OPER_GAE.rename(columns = {'DATA_VALUE':'INDU_SERV_OPER_GAE'}, inplace = True)

# (14) 소매업태별 판매액지수(경상지수)
# 8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  경상지수 : [I74A]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y098/M/201001/202209/I74A/I74A
INDU_CONSALE_GYUNG = ecosApiCall(f"901Y098/M/201001/{queryYYYYMM}/I74A/I74A")
INDU_CONSALE_GYUNG.rename(columns = {'DATA_VALUE':'INDU_CONSALE_GYUNG'}, inplace = True)

# (15) 소매업태별 판매액지수(불변지수)
# 8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  불변지수 : [I74B]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y098/M/201001/202209/I74B/I74B
INDU_CONSALE_BUL = ecosApiCall(f"901Y098/M/201001/{queryYYYYMM}/I74B/I74B")
INDU_CONSALE_BUL.rename(columns = {'DATA_VALUE':'INDU_CONSALE_BUL'}, inplace = True)

# (16) 소매업태별 판매액지수(계절조정지수)
# 8.5.3. 서비스업 - 소매업태별 판매액지수 : [901Y098][M]  /  총지수 : [I74A][2015=100]  /  계절조정지수 : [I74C]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y098/M/201001/202209/I74C/I74C
INDU_CONSALE_GAE = ecosApiCall(f"901Y098/M/201001/{queryYYYYMM}/I74C/I74C")
INDU_CONSALE_GAE.rename(columns = {'DATA_VALUE':'INDU_CONSALE_GAE'}, inplace = True)

# (17) 원달러 환율
# 3.1.2.1. 주요국 통화의 대원화환율 : [731Y004][M]   /   원/미국달러(매매기준율) : [0000001][원]   /   평균자료 : [0000100]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/731Y004/M/201001/202208/0000001/0000100
EXCHANGE_WON_DOL = ecosApiCall(f"731Y004/M/201001/{queryYYYYMM}/0000001/0000100")
EXCHANGE_WON_DOL.rename(columns = {'DATA_VALUE':'EXCHANGE_WON_DOL'}, inplace = True)

# (18) 시장금리 (KORIBOR 3개월)
# 1.3.2.2 시장금리(월,분기,년) : [721Y001][M]   /   KORIBOR(3개월) : [1025000][연%]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/721Y001/M/201001/202208/1025000
INTERATE_RATE_KORIBOR3 = ecosApiCall(f"721Y001/M/201001/{queryYYYYMM}/1025000")
INTERATE_RATE_KORIBOR3.rename(columns = {'DATA_VALUE':'INTERATE_RATE_KORIBOR3'}, inplace = True)

# (19) 물가 - 생산자 물가지수(에너지, 식료품 제외) (산연)
# 4.1.1.2. 생산자물가지수(특수분류) : [404Y015][M]   /   식료품에너지이외 : [S520AA][2015=100]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/404Y015/M/201001/202208/S520AA
MANU_PRICE = ecosApiCall(f"404Y015/M/201001/{queryYYYYMM}/S520AA")
MANU_PRICE.rename(columns = {'DATA_VALUE':'MANU_PRICE'}, inplace = True)

# (20) 유가(Dubai)
# 9.1.6.3. 국제상품가격 : [902Y003][M]   /   Dubai(현물) : [4010102][U$/bbl]
# (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/902Y003/M/201001/202208/4010102
OIL_PRICE_DUBAI = ecosApiCall(f"902Y003/M/201001/{queryYYYYMM}/4010102")
OIL_PRICE_DUBAI.rename(columns = {'DATA_VALUE':'OIL_PRICE_DUBAI'}, inplace = True)
```

<font color='red' style='bold'>Step 2.</font> **Merge columns using `For-loop` and export `.xlxs` file**
```
# compile the list of dataframes you want to merge such as [GDP_WON, GDP_GAE, OIL_PRICE_DUBAI ... ]
df_list = [GDP_WON_SIL, GDP_WON_MYUNG, GDP_GAE_SIL, GDP_GAE_MYUNG, INDU_GDP_WON, INDU_GDP_GAE, INDU_OPERATING_WON, INDU_OPERATING_GAE, INDU_MANU_OPER_WON, INDU_MANU_OPER_GAE, INDU_SERV_OPER_GYUNG, INDU_SERV_OPER_BUL, INDU_SERV_OPER_GAE, INDU_SERV_OPER_GYUNG, INDU_SERV_OPER_BUL, INDU_SERV_OPER_GAE, EXCHANGE_WON_DOL, INTERATE_RATE_KORIBOR3, MANU_PRICE, OIL_PRICE_DUBAI]
# grab first dataframe
IT_EFAS_MACRO_ECON_DB = df_list[0]
# loop through all but first data frame
for to_merge in df_list[1:]:
    # result of merge replaces first or previously merged data frame w/ all previous fields
    IT_EFAS_MACRO_ECON_DB = pd.merge(left = IT_EFAS_MACRO_ECON_DB, right = to_merge, left_index = True, right_index = True, how = "outer")

today = date.today()
IT_EFAS_MACRO_ECON_DB.to_excel(f'{today}_IT_EFAS_MACRO_ECON_DB.xlsx')
```

Refer to the uploaded file for more additional information.
