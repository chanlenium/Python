import lib

def makeURL(queryYYYYMM):
    url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NjgwMjNjNTc0NTBlZWM5Y2JjMmQ0YWEyNTIzMjhhNmM=&itmId=16363AAA0+&objL1=15363AA1AA+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=201001&endPrdDe={queryYYYYMM}&orgId=363&tblId=TX_36301_A000'
    ironDataFrame = lib.pd.DataFrame(lib.apiCall.kosisApiCall(url))
    # 원하는 컬럼만 뽑아냄(PRD_DE : 기준년월, DT : 조강생산량(천 톤))
    ironDataFrame = ironDataFrame[['PRD_DE', 'DT']] 
    ironDataFrame['DT'] = lib.pd.to_numeric(ironDataFrame['DT'])
    ironDataFrame.rename(columns = {'PRD_DE':'STD_YM'}, inplace = True)
    ironDataFrame.rename(columns = {'DT':'STEEL_CRUDE_QUAN'}, inplace = True)
    ironDataFrame = ironDataFrame.set_index('STD_YM')

    # 철강협회 데이터 들어갈 자리 삽입
    ironDataFrame.insert(0, 'STEEL_EXPORT_QUAN', '')
    ironDataFrame.insert(1, 'STEEL_DOME_QUAN', '')

    # 철광석 가격(출처: FRED)
    dfSteelPrice = lib.fdr.DataReader('FRED:PIORECRUSDM', '2010-01')
    dfSteelPrice['STD_YM'] = dfSteelPrice.index.astype(str).str.slice(0,4) + dfSteelPrice.index.astype(str).str.slice(5,7)
    dfSteelPrice.rename(columns = {'PIORECRUSDM':'STEEL_PRICE'}, inplace = True)
    dfSteelPrice = dfSteelPrice.set_index('STD_YM')

    ironDataFrame = lib.pd.merge(left = ironDataFrame, right = dfSteelPrice, left_index = True, right_index = True, how = "outer")
    return ironDataFrame