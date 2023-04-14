# pip install webdriver_manager --trusted-host pypi.org --trusted-host files.pythonhosted.org
# pip install certifi --trusted-host pypi.org --trusted-host files.pythonhosted.org
# pip install --upgrade tabulate --trusted-host pypi.org --trusted-host files.pythonhosted.org
# pip install openpyxl --trusted-host pypi.org --trusted-host files.pythonhosted.org
import lib

today = lib.date.today()

##### 조회년월
queryYYYYMM = '202302'
##### 조회분기
queryYYYYQQ = '2022Q4'
##### ECOS KEY (한국은행)
keyECOS = 'MTSA07N58C5X8EB4LMJL'
##### KOSIS KEY (통계청)
keyKOSIS = '7AA431187D1220S0'
##### eNaraIndex KEY (e나라지표)
keyENARA = '7AA431187D1220S0'


### 자동차 산업 (출처 : 차동차 산업협회)
# MOTOR_PROD_QUAN : 자동차산업동향-생산수량(대)
# MOTOR_DOME_QUAN : 자동차산업동향-내수판매량(대)
# MOTOR_EXPORT_QUAN : 자동차산업동향-수출수량(대)
# MOTOR_EXPORT_SALES : 자동차산업동향-수출금액(천 달러)
driver  = lib.webdriver.Chrome(service=lib.Service(lib.ChromeDriverManager().install()))
motorDataFrame = lib.motor.crawlData(driver)
print(lib.tabulate(motorDataFrame, headers='keys', tablefmt='psql'))
driver.close()  # 브라우저 닫기

### 조선 산업 (출처 : e나라지표-수주량, 건조량, 수주잔량   /   클락슨-신조선가지수, 선복량, 해체량)
# SHIP_ORDER_AMOUNT : 선박 수주량(CGT)
# SHIP_TONNAGE : 선박 건조량(CGT)
# SHIP_KAJI : (클락슨)신조선가지수
# SHIP_BACKLOG : 선박 수주잔량(CGT)
# SHIP_BOTTOMS : (클락슨)선박 선복량(DWT)
# SHIP_BREAKUP : (클락슨)선박 해체량(DWT)
# (Ex) http://www.index.go.kr/openApi/xml_stts.do?userId=chanlenium&idntfcId=7AA431187D1220S0&statsCode=115102&period=201001:202211'
shipDataFrame = lib.ship.makeURL(keyENARA, queryYYYYMM)
print(lib.tabulate(shipDataFrame, headers='keys', tablefmt='psql'))

### 철강 산업 (출처 : KOSIS철강통계조사-조강생산량(천 톤)   /   철강협회-수출량, 내수판매량   /   Fred(IMF)-철광석가격)
# STEEL_EXPORT_QUAN : (철강협회)철강 수출량(톤)
# STEEL_DOME_QUAN : (철강협회)철강 내수판매량(톤)
# STEEL_CRUDE_QUAN : 조강생산량(천 톤)
# STEEL_PRICE : (Fred)철광석 가격(Million dollar per Metric Ton)
ironDataFrame = lib.steel.makeURL(queryYYYYMM)
print(lib.tabulate(ironDataFrame, headers='keys', tablefmt='psql'))

### 석유화학 산업 (출처 : 한국석유화학협회-3대유도품수출량, 3대유도품내수판매량)
# PETRO_EXPORT_QUAN : (석유화학협회)3대유도품수출량
# PETRO_DOME_QUAN : (석유화학협회)3대유도품내수판매량
petroDataFrame = lib.petro.makeURL(ironDataFrame)
print(lib.tabulate(petroDataFrame, headers='keys', tablefmt='psql'))

### 반도체 산업 (출처 : 야후파이낸스-필라델피아반도체지수)
# SEMI_PHILADELPHIA : 필라델피아지수
semiDataFrame = lib.semi.makeURL()
print(lib.tabulate(semiDataFrame, headers='keys', tablefmt='psql'))

### 정유 산업 (출처 : ECOS-수입현황,수출현황,내수판매량   /   싱가포르정제마진,두바이크랙마진)
# OIL_IMPORT_QUAN : 정유 수출입동향-수입
# OIL_EXPORT_QUAN  : 정유 수출입동향-수출
# OIL_DOME_QUAN : 정유 수출입동향-내수판매량
# OIL_CRACK_MARGIN : 두바이 크랙마진
oilDataFrame = lib.oil.makeURL(keyECOS, queryYYYYMM)
print(lib.tabulate(oilDataFrame, headers='keys', tablefmt='psql'))

### 해운 산업 (클락슨-BDI,SCFI,VLCC,CCFI   /   통계청KOSIS-컨테이너수송현황,수출입화물수송)
# HAEWOON_BDI : 해운 운임지수-BDI(벌크선)
# HAEWOON_SCFI : 해운 운임지수-SCFI(컨테이너선)
# HAEWOON_WS : 해운 운임지수-VLCC-WS(유조선)
# HAEWOON_CCFI : 해운 운임지수-CCFI
# HAEWOON_CONT : 해운 운임지수-컨테이너수송현황 (TEU)
# HAEWOON_TRANS : 해운 운임지수-수출입 화물수송 (R/T)
# HAEWOON_DUBAI : 두바이 유가
# HAEWOON_DOME_TRANS : 해운 국내 화물수송량 (톤)
driver  = lib.webdriver.Chrome(service=lib.Service(lib.ChromeDriverManager().install()))
haewoonDataFrame = lib.haewoon.makeURL(keyECOS, queryYYYYMM, driver)
print(lib.tabulate(haewoonDataFrame, headers='keys', tablefmt='psql'))
driver.close()

### 건설 산업 (ECOS-건설국내수주량, 건설국내기성액, 건설해외수주량, 시도별건축착공현황(KOSIS), 미분양주택현황(서울,경기), 미분양주택현황(지방), 전국종합주택매매가격지수)
# CONST_DOME_ORDER_QUAN : 건설국내수주량
# CONST_REAL_PRICE : 건설국내기성액
# CONST_OVERSEA_ORDER_QUAN : 건설해외수주량
# CONST_BREAK_STATE : 시도별건축착공현황
# CONST_UNSOLD_URBAN : 미분양주택현황(서울,경기)
# CONST_UNSOLD_RURAL : 미분양주택현황(지방)
# CONST_HOUSE_PRICE : 전국종합주택매매가격지수
constDataFrame = lib.const.makeURL(keyECOS, keyKOSIS, queryYYYYMM)
print(lib.tabulate(constDataFrame, headers='keys', tablefmt='psql'))

### 모두 합치기
df_list = [motorDataFrame, shipDataFrame, ironDataFrame, petroDataFrame, semiDataFrame, oilDataFrame, haewoonDataFrame, constDataFrame]
# grab first dataframe
IT_EFAS_INDU_SPECIAL_DB = df_list[0]
# loop through all but first data frame
for to_merge in df_list[1:]:
    # result of merge replaces first or previously merged data frame w/ all previous fields
    IT_EFAS_INDU_SPECIAL_DB = lib.pd.merge(left = IT_EFAS_INDU_SPECIAL_DB, right = to_merge, left_index = True, right_index = True, how = "outer")

IT_EFAS_INDU_SPECIAL_DB.to_excel('../IT_EFAS_INDU_SPECIAL_DB/SPECIAL_DB/IT_EFAS_INDU_SPECIAL_DB.xlsx')
print(lib.tabulate(IT_EFAS_INDU_SPECIAL_DB, headers='keys', tablefmt='psql'))

today = lib.date.today()
lib.appendDataFrame.appendDf("IT_EFAS_INDU_SPECIAL_DB", today)

