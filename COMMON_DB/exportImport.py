import lib

# startYYYY = 2022
# endYYYY = 2023
# currentMM = 1

induUrlList = [
    ['14', '의약', 'https://istans.or.kr/in/newInTab.do?scode=3'],
    ['26', '반도체', 'https://istans.or.kr/in/newInTab.do?scode=4'],
    ['27', '디스플레이', 'https://istans.or.kr/in/newInTab.do?scode=5'],
    ['29', '컴퓨터', 'https://istans.or.kr/in/newInTab.do?scode=6'],
    ['30', '통신기기', 'https://istans.or.kr/in/newInTab.do?scode=7'],
    ['31', '가전', 'https://istans.or.kr/in/newInTab.do?scode=8'],
    ['32', '정밀기기', 'https://istans.or.kr/in/newInTab.do?scode=9'],
    ['34', '전지', 'https://istans.or.kr/in/newInTab.do?scode=10'],
    ['41', '항공', 'https://istans.or.kr/in/newInTab.do?scode=11'],
    ['12', '석유화학', 'https://istans.or.kr/in/newInTab.do?scode=14'],
    ['13', '정밀화학', 'https://istans.or.kr/in/newInTab.do?scode=15'],
    ['28', '기타 전자부품', 'https://istans.or.kr/in/newInTab.do?scode=17'],
    ['33', '전기기기', 'https://istans.or.kr/in/newInTab.do?scode=18'],
    ['35', '일반목적기계', 'https://istans.or.kr/in/newInTab.do?scode=19'],
    ['36', '특수목적기계', 'https://istans.or.kr/in/newInTab.do?scode=20'],
    ['37', '자동차', 'https://istans.or.kr/in/newInTab.do?scode=21'],
    ['40', '기타 수송장비', 'https://istans.or.kr/in/newInTab.do?scode=23'],
    ['11', '석유정제', 'https://istans.or.kr/in/newInTab.do?scode=33'],
    ['16', '고무', 'https://istans.or.kr/in/newInTab.do?scode=82'],
    ['17', '플라스틱', 'https://istans.or.kr/in/newInTab.do?scode=83'],
    ['18', '유리', 'https://istans.or.kr/in/newInTab.do?scode=84'],
    ['19', '세라믹', 'https://istans.or.kr/in/newInTab.do?scode=85'],
    ['20', '시멘트', 'https://istans.or.kr/in/newInTab.do?scode=86'],
    ['21', '기타 비금속 광물', 'https://istans.or.kr/in/newInTab.do?scode=87'],
    ['22', '철강', 'https://istans.or.kr/in/newInTab.do?scode=88'],
    ['23', '비철금속', 'https://istans.or.kr/in/newInTab.do?scode=89'],
    ['24', '주조', 'https://istans.or.kr/in/newInTab.do?scode=90'],
    ['25', '조립금속', 'https://istans.or.kr/in/newInTab.do?scode=91'],
    ['39', '조선', 'https://istans.or.kr/in/newInTab.do?scode=92'],
    ['3', '음식료', 'https://istans.or.kr/in/newInTab.do?scode=94'],
    ['4', '섬유', 'https://istans.or.kr/in/newInTab.do?scode=96'],
    ['5', '의류', 'https://istans.or.kr/in/newInTab.do?scode=97'],
    ['6', '가죽·신발', 'https://istans.or.kr/in/newInTab.do?scode=98'],
    ['7', '목재', 'https://istans.or.kr/in/newInTab.do?scode=99'],
    ['8', '제지', 'https://istans.or.kr/in/newInTab.do?scode=100'],
    ['9', '인쇄', 'https://istans.or.kr/in/newInTab.do?scode=101'],
    ['10', '기타 제조업', 'https://istans.or.kr/in/newInTab.do?scode=103']
    ]

def initBrowser():
    browser = lib.webdriver.Chrome(service=lib.Service(lib.ChromeDriverManager().install()))
    return browser

def closeBrowser(browser):
    browser.close()


def refineData(data, efasCode, efasName, isExport):
    print("Refine시작")
    data.reset_index(drop=False)
    data.iloc[0, 0] = efasName
    data.columns = data.iloc[0]
    data = data[1:2]
    if isExport:
        data = lib.pd.melt(data, id_vars=efasName, value_name='EXPORT_MDOLLAR').sort_values(efasName)
    else:
        data = lib.pd.melt(data, id_vars=efasName, value_name='balanceOfTrade_MDOLLAR').sort_values(efasName)
    data.rename(columns={0 : 'STD_YM'}, inplace = True)
    data['STD_YM'] = data['STD_YM'].str.replace('년 ', '')
    data['STD_YM'] = data['STD_YM'].str.replace('월', '')
    data.reset_index(drop=True, inplace=True)
    data.insert(2,'EFAS_CD',efasCode)
    data.insert(3,'EFAS_NM',efasName)
    data.drop(columns = efasName, inplace=True)
    data = data.sort_values(by=['STD_YM'])
    return data


def crawlData(url, isExport, browser, YYYY, endMM, efasCode, efasName):
    browser.get(url)
    lib.time.sleep(5)
    # 조회조건 설정을 위해 해당 iframe으로 이동 : "newSuTabMain > searchFrame"
    browser.switch_to.frame("newInTabMain")
    browser.switch_to.frame("searchFrame")
    browser.find_element(lib.By.XPATH, '//*[@id="sub-tabs"]/li[8]/a').send_keys(lib.Keys.ENTER) # 국제 무역 클릭
    lib.time.sleep(2)
    if isExport:
        browser.find_element(lib.By.XPATH, '//*[@id="grid71"]').send_keys(lib.Keys.ENTER) # 수출 클릭
    else:
        browser.find_element(lib.By.XPATH, '//*[@id="grid73"]').send_keys(lib.Keys.ENTER) # 무역수지
    lib.time.sleep(2)
    browser.switch_to.frame("gridFrame")  # GridFrame으로 이동
    print(browser.find_element(lib.By.XPATH, '//*[@id="gridTitle"]').text)
    lib.time.sleep(2)
    # 조회조건 설정 : 2020년 1월 (Xpath로 검색하면 동일 이름을 갖은 select 속성이 아닌 다른 element가 있어서 error 발생하므로 Full Xpath로 구현)
    elem = browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[1]/select')
    select = lib.Select(elem)
    select.select_by_visible_text('월')
    select.select_by_value('4')
    #print(select.first_selected_option.get_attribute("value"))
    lib.time.sleep(1)
    select = lib.Select(browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[1]/select')) # 시작년
    select.select_by_visible_text(str(YYYY))
    select.select_by_value(str(YYYY))
    lib.time.sleep(1)
    select = lib.Select(browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[2]/select')) # 시작월
    select.select_by_visible_text('1')
    select.select_by_value('1')
    lib.time.sleep(1)
    select = lib.Select(browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div[1]/select')) # 종료년
    select.select_by_visible_text(str(YYYY))
    select.select_by_value(str(YYYY))
    lib.time.sleep(1)
    select = lib.Select(browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div[2]/select')) # 종료월
    select.select_by_visible_text(str(endMM))
    select.select_by_value(str(endMM))
    print(select.first_selected_option.get_attribute("value"))
    #browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/a').send_keys(Keys.ENTER) # 조회버튼 클릭
    element = browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/a')
    print(browser.find_element(lib.By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/a').text)
    browser.execute_script("arguments[0].click();", element)
    lib.time.sleep(10)
    dfHeader = lib.pd.read_html(browser.page_source)[2]
    dfBody = lib.pd.read_html(browser.page_source)[4]
    induName = lib.pd.read_html(browser.page_source)[3]
    dfBody.iloc[:,0] = induName.iloc[:,[1]].values
    #result = dfHeader.append(dfBody)
    result = lib.pd.concat([dfHeader, dfBody])
    browser.switch_to.default_content()
    lib.WebDriverWait(browser, 5).until(lib.EC.frame_to_be_available_and_switch_to_it((lib.By.ID,"newInTabMain")))
    closeBrowser(browser)
    refinedResult = refineData(result, efasCode, efasName, isExport)
    return refinedResult


# Creating an empty Dictionary
efasDict = {}
def makeExportImportDB(startYYYY, endYYYY, currentMM):
    for elem in induUrlList:
        efasCode = elem[0]  # 코드
        efasName = elem[1]  # 코드명
        efasCodeExportImportUrl = elem[2]     # URL
        result = lib.pd.DataFrame()
        for yyyy in range(startYYYY, endYYYY + 1):
            print(efasName, yyyy)
            endMM = currentMM if yyyy == endYYYY else 12
            exportData = crawlData(efasCodeExportImportUrl, True, initBrowser(), yyyy, endMM, efasCode, efasName)
            balanceOfTradeData = crawlData(efasCodeExportImportUrl, False, initBrowser(), yyyy, endMM, efasCode, efasName)
            merged = exportData.merge(balanceOfTradeData, left_on=['STD_YM', 'EFAS_CD', 'EFAS_NM'], right_on=['STD_YM', 'EFAS_CD', 'EFAS_NM'], how="outer")
            merged['IMPORT_MDOLLAR'] = merged['EXPORT_MDOLLAR'] - merged['balanceOfTrade_MDOLLAR']
            merged.drop(columns = ['balanceOfTrade_MDOLLAR'], inplace=True)
            merged = merged.drop_duplicates()
            merged = merged.iloc[0:]
            result = lib.pd.concat([result, merged])
        efasDict[efasName] = result

    dfEfasExportImort = lib.pd.DataFrame()
    for elem in efasDict.values():
        dfEfasExportImort = lib.pd.concat([dfEfasExportImort, elem])

    dfEfasExportImort.set_index('STD_YM', inplace=True)
    dfEfasExportImort = dfEfasExportImort.sort_values(['STD_YM', 'EFAS_CD'], ascending = [True, True])

    dfEfasExportImort = lib.pd.DataFrame()
    for elem in efasDict.values():
        dfEfasExportImort = lib.pd.concat([dfEfasExportImort, elem])

    dfEfasExportImort.set_index('STD_YM', inplace=True)
    dfEfasExportImort = dfEfasExportImort.sort_values(['STD_YM', 'EFAS_CD'], ascending = [True, True])
    dfEfasExportImort = dfEfasExportImort[dfEfasExportImort.EXPORT_MDOLLAR.notnull() & dfEfasExportImort.IMPORT_MDOLLAR.notnull()]
    print(lib.tabulate(dfEfasExportImort, headers='keys', tablefmt='psql'))
    dfEfasExportImort.to_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/additionalExportImport.xlsx')