import lib 

def makeURL(keyECOS, keyKOSIS, queryYYYYMM):
    ## 건설국내수주액
    # 8.4.1. 국내건설수주액 : [901Y020][M]   /   총수주액[I42A][백만 원]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y020/M/201001/202209/I42A
    dfConstDomeOrderQuan = lib.apiCall.ecosApiCall(keyECOS, f"901Y020/M/201001/{queryYYYYMM}/I42A")
    dfConstDomeOrderQuan.rename(columns = {'DATA_VALUE':'CONST_DOME_ORDER_QUAN'}, inplace = True)

    ## 국내건설기성액
    # 8.4.2. 건설기성액 : [901Y104][M]   /   총기성액[I48A][백만 원]    /   경상[I37A]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y104/M/201001/202209/I48A/I37A
    dfConstRealPrice = lib.apiCall.ecosApiCall(keyECOS, f"901Y104/M/201001/{queryYYYYMM}/I48A/I37A")
    dfConstRealPrice.rename(columns = {'DATA_VALUE':'CONST_REAL_PRICE'}, inplace = True)

    ## 시도별건축착공현황 - KOSIS
    # https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&format=json&jsonVD=Y&userStatsId=chanlenium/116/DT_MLTM_2202/2/2/20230216134719&prdSe=M&newEstPrdCnt=300&prdInterval=1
    url = f'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&format=json&jsonVD=Y&userStatsId=chanlenium/116/DT_MLTM_2202/2/2/20230216134719&prdSe=M&newEstPrdCnt=500&prdInterval=1'
    dfConstBreakState =  lib.pd.DataFrame(lib.apiCall.kosisApiCall(url))
    dfConstBreakState = dfConstBreakState[['PRD_DE', 'DT']]  #  "UNIT_NM": "동㎡"
    dfConstBreakState = dfConstBreakState.loc[dfConstBreakState['PRD_DE'].astype(int) >= 201001]
    dfConstBreakState.rename(columns = {'PRD_DE':'STD_YM', 'DT':'CONST_BREAK_STATE'}, inplace = True)
    dfConstBreakState = dfConstBreakState.set_index('STD_YM')

    ## 미분양주택현황(서울,경기) 
    # 8.4.5 미분양주택현황 : [901Y074][M]   /   서울[I410B][호], 경기[I410I][호]
    # https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y074/M/201001/202209/I410B
    # https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y074/M/201001/202209/I410I
    dfConstUnsoldUrban = lib.apiCall.ecosApiCall(keyECOS, f"901Y074/M/201001/{queryYYYYMM}/I410B") + lib.apiCall.ecosApiCall(keyECOS, f"901Y074/M/201001/{queryYYYYMM}/I410I")
    dfConstUnsoldUrban.rename(columns = {'DATA_VALUE':'CONST_UNSOLD_URBAN'}, inplace = True)
    
    ## 미분양주택현황(지방) 
    # 8.4.5 미분양주택현황 : [901Y074][M]   /   전국[I410A][호]
    # https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y074/M/201001/202209/I410A
    dfConstUnsoldRural = lib.apiCall.ecosApiCall(keyECOS, f"901Y074/M/201001/{queryYYYYMM}/I410A")
    dfConstUnsoldRural.rename(columns = {'DATA_VALUE':'CONST_UNSOLD_RURAL'}, inplace = True)
    mergeRuralUrban = lib.pd.merge(left = dfConstUnsoldRural, right = dfConstUnsoldUrban, left_index = True, right_index = True)
    mergeRuralUrban['CONST_UNSOLD_RURAL'] = mergeRuralUrban['CONST_UNSOLD_RURAL'] - mergeRuralUrban['CONST_UNSOLD_URBAN']
    dfConstUnsoldRural = mergeRuralUrban['CONST_UNSOLD_RURAL']


    ## 건설해외수주량(출처: KOSIS)
    url = f'http://www.index.go.kr/openApi/xml_stts.do?userId=chanlenium&idntfcId={keyKOSIS}&statsCode=122103&period=201001:{queryYYYYMM}'
    response = lib.urlopen(url).read()
    xtree = lib.ET.fromstring(response)

    # '표' tag에서 '주기'값이 '월'인 tree를 찾아서 월별 데이터 시작 지점을 찾음
    for neighbor in xtree.iter("표"):
        if neighbor.attrib['주기'] == '월':
            for elem in neighbor.iter("분류1"):
                if elem.attrib['이름'] == '합계':
                    rootMonth = elem

    # 해외건설수주액 데이터 적제
    period = [x.attrib["주기"] for x in rootMonth]
    value = [x.text for x in rootMonth]

    dfConstOversea = lib.pd.DataFrame()
    dfConstOversea['STD_YM'] = period
    dfConstOversea['CONST_OVERSEA_ORDER_QUAN'] = value
    dfConstOversea['STD_YM'] = dfConstOversea['STD_YM'].astype(int)
    dfConstOversea = dfConstOversea.query("STD_YM >= 201001")
    dfConstOversea['STD_YM'] = dfConstOversea['STD_YM'].astype(str)
    dfConstOversea = dfConstOversea.set_index('STD_YM')


    ## 전국종합주택매매가격지수(출처: KOSIS 유형별 매매가격지수)
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=sales+&objL1=00+&objL2=a0+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=201001&endPrdDe={queryYYYYMM}&orgId=408&tblId=DT_40803_N0001'
    dfConstHousePrice = lib.pd.DataFrame(lib.apiCall.kosisApiCall(url))
    dfConstHousePrice = dfConstHousePrice[['PRD_DE', 'C2_NM', 'DT']]  # 원하는 컬럼만 뽑아냄(PRD_DE : 기준년월, DT : DATA_VALUE(100 = 202106))
    dfConstHousePrice['DT'] = lib.pd.to_numeric(dfConstHousePrice['DT'])
    dfConstHousePrice.rename(columns = {'PRD_DE':'STD_YM', 'DT':'CONST_HOUSE_PRICE'}, inplace = True)
    dfConstHousePrice = dfConstHousePrice[['STD_YM', 'CONST_HOUSE_PRICE']]
    dfConstHousePrice = dfConstHousePrice.set_index('STD_YM')

    # compile the list of dataframes you want to merge
    df_list = [dfConstDomeOrderQuan, dfConstRealPrice, dfConstOversea, dfConstBreakState, dfConstUnsoldUrban, dfConstUnsoldRural, dfConstHousePrice]
    # grab first dataframe
    constDataFrame = df_list[0]
    # loop through all but first data frame
    for to_merge in df_list[1:]:
        # result of merge replaces first or previously merged data frame w/ all previous fields
        constDataFrame = lib.pd.merge(left = constDataFrame, right = to_merge, left_index = True, right_index = True, how = "outer")

    return constDataFrame