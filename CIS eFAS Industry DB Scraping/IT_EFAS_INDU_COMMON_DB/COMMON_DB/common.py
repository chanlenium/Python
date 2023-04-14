import lib

# initialize list of lists
mappingData = [['1', '농림어업', ''],
['2', '광업', ''],
['3', '음식료', '(1401)음식료'],
['4', '섬유', '(1403)섬유'],
['5', '의류', '(1404)의류'],
['6', '가죽신발', '(1405)가죽·신발'],
['7', '목재', '(1406)목재'],
['8', '제지', '(1407)제지'],
['9', '인쇄', '(1408)인쇄'],
['10' '기타 제조업', '(1410)기타 제조업'],
['11', '석유정제', '(1301)석유정제'],
['12', '석유화학', '(1201)석유화학'],
['13', '정밀화학', '(1202)정밀화학'],
['14', '의약', '(1101)의약'],
['15', '타이어', ''],
['16' '(1302)고무'],
['17', '플라스틱', '(1303)플라스틱'],
['18', '유리', '(1304)유리'],
['19', '세라믹', '(1305)세라믹'],
['20', '시멘트', '(1306)시멘트'],
['21', '기타 비금속 광물', '(1307)기타 비금속 광물'],
['22', '철강', '(1308)철강'],
['23', '비철금속', '(1309)비철금속'],
['24', '주조', '(1310)주조'],
['25', '조립금속', '(1311)조립금속'],
['26', '반도체', '(1102)반도체'],
['27', '디스플레이', '(1103)디스플레이'],
['28', '기타 전자부품', ''],
['29', '컴퓨터', '(1104)컴퓨터'],
['30', '통신기기', '(1105)통신기기'],
['31', '가전', '(1106)가전'],
['32', '정밀기기', '(1107)정밀기기'],
['33', '전기기기', '(1204)전기기기'],
['34', '전지', '(1108)전지'],
['35', '일반목적기계', '(1205)일반목적기계'],
['36', '특수목적기계', '(1206)특수목적기계'],
['37', '자동차', '(1207)자동차'],
['38', '자동차부품', ''],
['39', '조선', '(1312)조선'],
['40', '기타 수송장비', '(1209)기타 수송장비'],
['41', '항공', '(1109)항공'],
['42', '가구', '(1409)가구'],
['43', '전기가스수도', ''],
['44', '폐수처리및자원재활용', ''],
['45', '건설', ''],
['46', '도소매', '(2101)도·소매업'],
['47', '육상창고', ''],
['48', '해운', ''],
['49', '항공운송', ''],
['50', '숙박·음식점', '(2401)숙박·음식점'],
['51', '출판', '(2201)출판'],
['52', '방송', '(2202)방송'],
['53', '통신', '(2203)통신'],
['54', '정보', '(2204)정보'],
['55', '금융·보험', '(2205)금융·보험'],
['56', '부동산', '(2206)부동산'],
['57', '전문·과학기술', '(2208)전문·과학기술'],
['58', '사업시설관리서비스', '(2209)사업시설관리서비스'],
['59', '사업지원', '(2210)사업지원'],
['60', '임대', '(2207)임대'],
['61', '공공행정', ''],
['62', '교육', '(2303)교육'],
['63', '의료·보건', '(2304)의료·보건'],
['64', '사회복지', '(2305)사회복지'],
['65', '예술·스포츠·여가', '(2402)예술·스포츠·여가'],
['66', '기타 서비스','(2403)기타 서비스']]
 
# Create the pandas DataFrame
dfEFAStoISTANSMAP = lib.pd.DataFrame(mappingData, columns=['EFAS_CD', 'EFAS_NM', 'ISTANS_NM'])


def iSTANSCall(istansUrl, fromYYYY, fromMM):
    browser = lib.webdriver.Chrome(service=lib.Service(lib.ChromeDriverManager().install()))
    browser.get(istansUrl)  # Get data from istansUrl
    lib.time.sleep(10) 
    # Move to inner iframe to set query condition ("newSuTabMain > searchFrame")
    browser.switch_to.frame("newSuTabMain")
    browser.switch_to.frame("searchFrame")
    # Set query condition : From JAN 2010
    select = lib.Select(browser.find_element(lib.By.XPATH, '//*[@id="df_period"]'))
    print(select.first_selected_option.get_attribute("value"))
    select.select_by_visible_text('월')
    select.select_by_value('4')
    lib.time.sleep(5)
    select = lib.Select(browser.find_element(lib.By.XPATH, '//*[@id="from_year_month"]'))
    select.select_by_visible_text(fromYYYY)
    select.select_by_value(fromYYYY)
    lib.time.sleep(5)
    select = lib.Select(browser.find_element(lib.By.XPATH, '//*[@id="from_month"]'))
    select.select_by_visible_text(fromMM)
    select.select_by_value(fromMM)
    lib.time.sleep(5)
    browser.find_element(lib.By.XPATH, '//*[@id="resultDiv"]/div[1]/div[1]/a').send_keys(lib.Keys.ENTER)  # Click 'Query' button
    print("진행중_1")
    lib.time.sleep(10)
    # Get HTML page source (Append Header, Body, and induName)
    dfHeader = lib.pd.read_html(browser.page_source)[2]
    dfBody = lib.pd.read_html(browser.page_source)[4]
    induName = lib.pd.read_html(browser.page_source)[3]
    dfBody.iloc[:,0] = induName.iloc[:,[1]].values
    dfIStansResult = dfHeader.append(dfBody)
    print("진행중_2")
    # Refine Dataframe
    dfIStansResult.reset_index(drop=False)
    dfIStansResult.iloc[0, 0] = 'iStansInduNM'
    dfIStansResult.columns = dfIStansResult.iloc[0]
    dfIStansResult = dfIStansResult[1:]
    # Chage data to long type using 'melt' function
    dfIStansResult = lib.pd.melt(dfIStansResult, id_vars=['iStansInduNM'], value_name='indexValue').sort_values('iStansInduNM')
    dfIStansResult.rename(columns={0 : 'STD_YM'}, inplace = True)
    dfIStansResult['STD_YM'] = dfIStansResult['STD_YM'].str.replace('년 ', '')
    dfIStansResult['STD_YM'] = dfIStansResult['STD_YM'].str.replace('월', '')
    dfIStansResult = dfIStansResult.reset_index().merge(dfEFAStoISTANSMAP, left_on='iStansInduNM', right_on='ISTANS_NM', how="inner")       
    # Move browser to main Frame
    browser.switch_to.default_content()
    lib.WebDriverWait(browser, 10).until(lib.EC.frame_to_be_available_and_switch_to_it((lib.By.ID,"newSuTabMain")))
    browser.close()
    return dfIStansResult


def makeCommonDB(fromYYYY, fromMM):
    # 생산지수(원지수) : Istans > 주제별 통계 > 산업동향지수 > 생산지수(원지수)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S120" 
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfPRODUC_INDEX = iSTANSCallResult.rename(columns = {'indexValue':'PRODUC_INDEX'})

    # 서비스업생산지수(원지수, 불변지수) : Istans > 주제별 통계 > 산업동향지수 > 서비스업생산지수(불변지수)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S358" 
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfServPRODUC_INDEX = iSTANSCallResult.rename(columns = {'indexValue':'PRODUC_INDEX'})
    dfPRODUC_INDEX = dfPRODUC_INDEX.append(dfServPRODUC_INDEX)
    dfPRODUC_INDEX = dfPRODUC_INDEX[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'PRODUC_INDEX']]
    dfPRODUC_INDEX.drop_duplicates(inplace=True)
    print(lib.tabulate(dfPRODUC_INDEX, headers='keys', tablefmt='psql'))

    # 생산지수(계절조정) : Istans > 주제별 통계 > 산업동향지수 > 생산지수(계절조정)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S350" 
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfPRODUC_INDEX_GAE = iSTANSCallResult.rename(columns = {'indexValue':'PRODUC_INDEX_GAE'})

    # 서비스업생산지수(계절조정) : Istans > 주제별 통계 > 산업동향지수 > 생산지수(계절조정)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S359" 
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfServPRODUC_INDEX_GAE = iSTANSCallResult.rename(columns = {'indexValue':'PRODUC_INDEX_GAE'})
    dfPRODUC_INDEX_GAE = dfPRODUC_INDEX_GAE.append(dfServPRODUC_INDEX_GAE)
    dfPRODUC_INDEX_GAE = dfPRODUC_INDEX_GAE[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'PRODUC_INDEX_GAE']]
    dfPRODUC_INDEX_GAE.drop_duplicates(inplace=True)
    print(lib.tabulate(dfPRODUC_INDEX_GAE, headers='keys', tablefmt='psql'))

    # 출하지수(원지수) : Istans > 주제별 통계 > 산업동향지수 > 출하지수(원지수)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S351"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfSHIPMENT_INDEX = iSTANSCallResult.rename(columns = {'indexValue':'SHIPMENT_INDEX'})
    dfSHIPMENT_INDEX = dfSHIPMENT_INDEX[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'SHIPMENT_INDEX']]
    dfSHIPMENT_INDEX.drop_duplicates(inplace=True)
    print(lib.tabulate(dfSHIPMENT_INDEX, headers='keys', tablefmt='psql'))

    # 출하지수(계절조정) : Istans > 주제별 통계 > 산업동향지수 > 출하지수(계절조정)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S352"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfSHIPMENT_INDEX_GAE = iSTANSCallResult.rename(columns = {'indexValue':'SHIPMENT_INDEX_GAE'})
    dfSHIPMENT_INDEX_GAE = dfSHIPMENT_INDEX_GAE[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'SHIPMENT_INDEX_GAE']]
    dfSHIPMENT_INDEX_GAE.drop_duplicates(inplace=True)
    print(lib.tabulate(dfSHIPMENT_INDEX_GAE, headers='keys', tablefmt='psql'))

    # 재고지수(원지수) : Istans > 주제별 통계 > 산업동향지수 > 재고지수(원지수)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S353"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfINVENTORY_INDEX = iSTANSCallResult.rename(columns = {'indexValue':'INVENTORY_INDEX'})
    dfINVENTORY_INDEX = dfINVENTORY_INDEX[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'INVENTORY_INDEX']]
    dfINVENTORY_INDEX.drop_duplicates(inplace=True)
    print(lib.tabulate(dfINVENTORY_INDEX, headers='keys', tablefmt='psql'))

    # 재고지수(계절조정) : Istans > 주제별 통계 > 산업동향지수 > 재고지수(계절조정)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S354"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfINVENTORY_INDEX_GAE = iSTANSCallResult.rename(columns = {'indexValue':'INVENTORY_INDEX_GAE'})
    dfINVENTORY_INDEX_GAE = dfINVENTORY_INDEX_GAE[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'INVENTORY_INDEX_GAE']]
    dfINVENTORY_INDEX_GAE.drop_duplicates(inplace=True)
    print(lib.tabulate(dfINVENTORY_INDEX_GAE, headers='keys', tablefmt='psql'))

    # 가동률지수(원지수) : Istans > 주제별 통계 > 산업동향지수 > 가동률지수(원지수)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S355"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfOPER_RATE_INDEX = iSTANSCallResult.rename(columns = {'indexValue':'OPER_RATE_INDEX'})
    dfOPER_RATE_INDEX = dfOPER_RATE_INDEX[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'OPER_RATE_INDEX']]
    dfOPER_RATE_INDEX.drop_duplicates(inplace=True)
    print(lib.tabulate(dfOPER_RATE_INDEX, headers='keys', tablefmt='psql'))

    # 가동률지수(계절조정) : Istans > 주제별 통계 > 산업동향지수 > 가동률지수(계절조정)
    url = "https://istans.or.kr/su/newSuTab.do?scode=S356"
    iSTANSCallResult = iSTANSCall(url, fromYYYY, fromMM)
    dfOPER_RATE_INDEX_GAE = iSTANSCallResult.rename(columns = {'indexValue':'OPER_RATE_INDEX_GAE'})
    dfOPER_RATE_INDEX_GAE = dfOPER_RATE_INDEX_GAE[['STD_YM', 'EFAS_CD', 'EFAS_NM', 'OPER_RATE_INDEX_GAE']]
    dfOPER_RATE_INDEX_GAE.drop_duplicates(inplace=True)
    print(lib.tabulate(dfOPER_RATE_INDEX_GAE, headers='keys', tablefmt='psql'))

    # compile the list of dataframes you want to merge
    df_list = [dfPRODUC_INDEX, dfPRODUC_INDEX_GAE, dfSHIPMENT_INDEX, dfSHIPMENT_INDEX_GAE, dfINVENTORY_INDEX, dfINVENTORY_INDEX_GAE, dfOPER_RATE_INDEX, dfOPER_RATE_INDEX_GAE]
    # grab first dataframe
    IT_EFAS_INDU_COMMON_DB= df_list[0]
    # loop through all but first data frame
    for to_merge in df_list[1:]:
        # result of merge replaces first or previously merged data frame w/ all previous fields
        IT_EFAS_INDU_COMMON_DB = IT_EFAS_INDU_COMMON_DB.merge(to_merge, left_on=['STD_YM', 'EFAS_CD', 'EFAS_NM'], right_on=['STD_YM', 'EFAS_CD', 'EFAS_NM'], how="outer")
        
    IT_EFAS_INDU_COMMON_DB.drop_duplicates(inplace=True)
    IT_EFAS_INDU_COMMON_DB.set_index('STD_YM', inplace=True)
    IT_EFAS_INDU_COMMON_DB['EFAS_CD'] = lib.pd.to_numeric(IT_EFAS_INDU_COMMON_DB['EFAS_CD'])
    IT_EFAS_INDU_COMMON_DB = IT_EFAS_INDU_COMMON_DB.sort_values(['STD_YM', 'EFAS_CD'], ascending = [True, True])
    IT_EFAS_INDU_COMMON_DB['EFAS_CD'] = IT_EFAS_INDU_COMMON_DB['EFAS_CD'].astype(str)

    #IT_EFAS_INDU_COMMON_DB.to_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/additionalCommon.xlsx')
    IT_EFAS_INDU_COMMON_DB.to_excel('../COMMON_DB/additionalCommon.xlsx')
    print(lib.tabulate(IT_EFAS_INDU_COMMON_DB, headers='keys', tablefmt='psql'))