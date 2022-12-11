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

|제목|내용|설명|
|:---|---:|:---:|
|왼쪽정렬|오른쪽정렬|중앙정렬|
|왼쪽정렬|오른쪽정렬|중앙정렬|
|왼쪽정렬|오른쪽정렬|중앙정렬|

1. Get an authentication key for ECOS Open API service

Signup(or Singin) and request to issue an authentication key
  <img src="https://wikidocs.net/images/page/144514/kor02.png" width="600">
  
2. Search OPEN API and check how to use it

Reference: [Development Specification Document](https://ecos.bok.or.kr/api/#/DevGuide/DevSpeciflcation) and [Statistical Code Search](https://ecos.bok.or.kr/api/#/DevGuide/StatisticalCodeSearch)

```
(Sample Example)
https://ecos.bok.or.kr/api/StatisticSearch/sample/xml/kr/1/10/200Y001/A/2015/2021/10101/?/?/?
```
|제목|내용|설명|
|:---|---:|:---:|
|왼쪽정렬|오른쪽정렬|중앙정렬|
|왼쪽정렬|오른쪽정렬|중앙정렬|
|왼쪽정렬|오른쪽정렬|중앙정렬|

## Open Colab and typing scripts to scrap Open API data
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

Refer to the uploaded file for more additional information :-)
