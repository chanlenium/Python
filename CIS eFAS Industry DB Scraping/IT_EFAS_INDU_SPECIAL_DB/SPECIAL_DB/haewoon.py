import lib

def makeURL(keyECOS, queryYYYYMM, driver):
    ## (통계청KOSIS) 컨테이너 화물수송 현황
    startYYYYMM = 201101
    endYYYYMM = int(queryYYYYMM)
    yyyyMM_list = list(range(startYYYYMM, endYYYYMM, 100))

    def kosisContainerApi(yyyyMM):
        s_yyyyMM = str(yyyyMM)
        e_yyyyMM = str(yyyyMM + 11)
        url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=13103114674T.0003+&objL1=13102114674A.01+13102114674A.02+13102114674A.03+13102114674A.04+13102114674A.05+13102114674A.06+13102114674A.07+13102114674A.08+13102114674A.09+13102114674A.10+13102114674A.11+13102114674A.12+13102114674A.13+13102114674A.14+13102114674A.15+13102114674A.16+13102114674A.17+13102114674A.18+13102114674A.19+13102114674A.20+13102114674A.21+13102114674A.22+13102114674A.23+13102114674A.24+13102114674A.25+13102114674A.26+13102114674A.27+13102114674A.28+13102114674A.29+13102114674A.30+&objL2=13102114674B.01+13102114674B.02+&objL3=13102114674C.01+13102114674C.02+13102114674C.03+13102114674C.04+13102114674C.05+&objL4=13102114674D.0006+&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe={s_yyyyMM}&endPrdDe={e_yyyyMM}&orgId=146&tblId=DT_MLTM_1312'
        r = lib.requests.get(url)
        jo = r.json()
        df = lib.pd.DataFrame(jo)
        df = df[['PRD_DE', 'C1_NM', 'C2_NM', 'C3_NM', 'DT']]  # C1_NM:항구명, C2_NM:국적구분(국적선/외국선), C3_NM:구분(내항/외항입항/외항출항/입항환적/출항환적, DT:화물수송량(R/T)
        df['DT'] = df['DT'].astype(float) # df['DT'] = pd.to_numeric(df['DT'])
        df.rename(columns = {'PRD_DE':'STD_YM', 'DT':'HAEWOON_CONT'}, inplace = True)
        df = df.set_index('STD_YM')
        return df

    dfCONT = lib.pd.DataFrame()
    for elem in yyyyMM_list:
        if(dfCONT.empty):
            dfCONT = kosisContainerApi(elem)
        else:
            dfCONT = lib.pd.concat([dfCONT, kosisContainerApi(elem)])
        dfCONT = dfCONT.groupby('STD_YM').sum(numeric_only=True)
        #dfCONT = dfCONT.groupby(level = 'STD_YM').transform('sum')
        #dfCONT = dfCONT.groupby('STD_YM').sum(numeric_only=True)



    ## (통계청KOSIS) 수출입 화물수송 현황
    # (수출입 따로 보는 경우) url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=13103114675T.0001+&objL1=13102114675A.01+&objL2=13102114675B.01+&objL3=13102114675C.0002+13102114675C.0003+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=201101&endPrdDe={queryYYYYMM}&orgId=146&tblId=DT_MLTM_1316'
    # (수출입 합쳐 보는 경우) 
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=13103114675T.0001+&objL1=13102114675A.01+&objL2=13102114675B.01+&objL3=13102114675C.0001+&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=201101&endPrdDe={queryYYYYMM}&orgId=146&tblId=DT_MLTM_1316'
    dfTRANS = lib.pd.DataFrame(lib.apiCall.kosisApiCall(url))
    dfTRANS = dfTRANS[['PRD_DE', 'C3_NM', 'DT']]  # (수출입 따로 보는경우) C3_NM:수출/수입/전체,   (수출입 같이 보는경우)C_NM:전체
    dfTRANS['DT'] = round(lib.pd.to_numeric(dfTRANS['DT']) / 1000, 0) # 천톤단위로 변환
    dfTRANS = dfTRANS[['PRD_DE', 'DT']]
    dfTRANS.rename(columns = {'PRD_DE':'STD_YM', 'DT':'HAEWOON_TRANS'}, inplace = True)
    dfTRANS = dfTRANS.set_index('STD_YM')


    ## 유가(Dubai) 추가 (ECOS)
    # 9.1.6.3. 국제상품가격 : [902Y003][M]   /   Dubai(현물) : [4010102][U$/bbl]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/902Y003/M/201001/202208/4010102
    dfDUBAI = lib.apiCall.ecosApiCall(keyECOS, f"902Y003/M/201001/{queryYYYYMM}/4010102")
    dfDUBAI.rename(columns = {'DATA_VALUE':'HAEWOON_DUBAI'}, inplace = True)



    ## (통계청KOSIS) 국내화물수송량 : 화물수송실적 - 내항화물입항현황 - 연안화물선(입항) - 화물(단위: R/T)
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=13103114676T.0003+&objL1=13102114676A.001+&objL2=13102114676B.0002+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=201101&endPrdDe={queryYYYYMM}&orgId=146&tblId=DT_MLTM_1314'
    dfDomeTrans =  lib.pd.DataFrame(lib.apiCall.kosisApiCall(url))
    dfDomeTrans = dfDomeTrans[['PRD_DE', 'ITM_NM', 'C1_NM', 'C2_NM', 'DT']]  # ITM_NM:화물, C1_NM:총계, C2_NM:연안화물선(입항)
    dfDomeTrans['DT'] = round(lib.pd.to_numeric(dfDomeTrans['DT']) / 1000, 0) # 천톤단위로 변환
    dfDomeTrans = dfDomeTrans[['PRD_DE', 'DT']]
    dfDomeTrans.rename(columns = {'PRD_DE':'STD_YM', 'DT':'HAEWOON_DOME_TRANS'}, inplace = True)
    dfDomeTrans = dfDomeTrans.set_index('STD_YM')




    ## (TradLinx) 컨테이너 운임지표 : CCFI, SCFI
    # Data reference : Go to TradLinx homepage
    url = "https://www.tradlinx.com/freight-index" 
    driver.get(url)
    
    # Select Month because we need monthly data
    driver.find_element(lib.By.XPATH, '/html/body/application/div/container-freight/div/div[2]/div/div[1]/div[3]/drp-input/div/div/span[2]').click()
    driver.find_element(lib.By.XPATH, '/html/body/application/div/container-freight/div/div[2]/div/div[1]/div[3]/drp-input/div/div[2]/ul/li[2]').click() 

    print(driver.find_element(lib.By.XPATH, '/html/body/application/div/container-freight/div/div[2]/div/div[1]/div[3]/drp-input/div/div/span[2]').text)

    driver.find_element(lib.By.XPATH, '/html/body/application/div/container-freight/div/div[2]/div/div[1]/div[4]/div/i').click() # Pick calendar
    driver.implicitly_wait(5)
    lib.time.sleep(5)

    # Set query condition : Select start day as '2020.1.1'
    # Click 'JAN'
    while driver.find_element(lib.By.CLASS_NAME, 'dtp-actual-month').text != 'JAN':
        driver.find_element(lib.By.CLASS_NAME, "dtp-select-month-before").click()
    # Click '2010'
    while driver.find_element(lib.By.CLASS_NAME, 'dtp-actual-year').text != '2010':
        driver.find_element(lib.By.CLASS_NAME, "dtp-select-year-before").click()
    # Click 'day 1'
    driver.find_element(lib.By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div[1]/table/tbody/tr[2]/td[6]/a").click()

    # Make sure that the selected day is 2010. JAN. 1
    print(driver.find_element(lib.By.CLASS_NAME, 'dtp-actual-year').text)
    print(driver.find_element(lib.By.CLASS_NAME, 'dtp-actual-month').text)
    print(driver.find_element(lib.By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div[1]/table/tbody/tr[2]/td[6]/a").text)
    print(driver.find_element(lib.By.CLASS_NAME, 'dtp-btn-ok').text)

    driver.find_element(lib.By.CLASS_NAME, 'dtp-btn-ok').click()
    lib.time.sleep(5)
    #print(browser.find_element(By.XPATH, "/html/body").text)
    containerDataFrame = lib.pd.read_html(driver.page_source)[1]

    containerDataFrame = containerDataFrame.transpose()
    containerDataFrame.columns = containerDataFrame.iloc[0]
    containerDataFrame = containerDataFrame[1:]
    containerDataFrame['STDYM'] = containerDataFrame.index.str.replace(" ", "")

    containerDataFrame.columns.name = None  # Delete column name 'Date All'
    containerDataFrame.reset_index(drop=True, inplace=True) # index reset
    containerDataFrame.set_index('STDYM', inplace=True) # Set index as 'STDYM'

    dfSCFI = containerDataFrame[['SCFI']]
    dfSCFI.rename(columns = {'SCFI':'HAEWOON_SCFI'}, inplace = True)
    dfCCFI = containerDataFrame[['CCFI']]
    dfCCFI.rename(columns = {'CCFI':'HAEWOON_CCFI'}, inplace = True)

    # compile the list of dataframes you want to merge
    df_list = [dfSCFI, dfCCFI, dfCONT, dfTRANS, dfDUBAI, dfDomeTrans]
    # grab first dataframe
    haewoonDataFrame = df_list[0]
    # loop through all but first data frame
    for to_merge in df_list[1:]:
        # result of merge replaces first or previously merged data frame w/ all previous fields
        haewoonDataFrame = lib.pd.merge(left = haewoonDataFrame, right = to_merge, left_index = True, right_index = True, how = "outer")


    # 기타 데이터 삽입
    haewoonDataFrame.insert(0, 'HAEWOON_BDI', '')
    haewoonDataFrame.insert(2, 'HAEWOON_WS', '')

    return haewoonDataFrame