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


1. Get an authentication key for ECOS Open API service

Signup(or Singin) and request to issue an authentication key
  <img src="https://wikidocs.net/images/page/144514/kor02.png" width="600">
  
2. Search OPEN API and check how to use it

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

1. Import library
```
import requests
import pandas as pd
from datetime import date
```

2. Request and get data from URL
```
url = f'https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/1000/200Y006/Q/2020Q1/2022Q3/1400'
r = requests.get(url)
```

3. Parsing url data to [JSON](https://en.wikipedia.org/wiki/JSON, "Json wiki link") format and coverting json to pandas dataframe format
```
jo = r.json()
df = pd.DataFrame(jo['StatisticSearch']['row']) # Convert json data to dataframe
df = df[['TIME', 'DATA_VALUE']] # Select only the desired columns
```

4. Rename column and convert data type
```
df.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
df['DATA_VALUE'] = pd.to_numeric(df['DATA_VALUE'])
df['STD_YM'] = df['STD_YM'].str.replace('Q1$', '03', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q2$', '06', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q3$', '09', regex=True)
df['STD_YM'] = df['STD_YM'].str.replace('Q4$', '12', regex=True)
```

5. Set Index and export excel file
```
df = df.set_index('STD_YM')
today = date.today()
df.to_excel(f'{today}_EcosExample.xlsx')
```

### Scraping two data columns and merging them (Define helper function and Join columns)
1. Raw coding for scaping two data columns

2. Bind common parts(URL call process) and Make helper function

3. Merge columns
 
### Scraping more than two data columns and merging them (Loop)
1. Raw coding for scaping two data columns

Refer to the uploaded file for more additional information :-)
