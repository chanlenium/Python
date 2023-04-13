import lib

def makeURL(keyECOS, queryYYYYMM):
    # (1) 정유 수출입동향-수입
    # 8.4.11. 석유제품수급 : [901Y073][M]   /   수입[I46B][천배럴]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y073/M/201001/202211/I46B
    dfOilImportQuan = lib.apiCall.ecosApiCall(keyECOS, f"901Y073/M/201001/{queryYYYYMM}/I46B")
    dfOilImportQuan.rename(columns = {'DATA_VALUE':'OIL_IMPORT_QUAN'}, inplace = True)

    # (2) 정유 수출입동향-수출
    # 8.4.11. 석유제품수급 : [901Y073][M]   /   수출[I46D][천배럴]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y073/M/201001/202209/I46B
    dfOilExportQuan = lib.apiCall.ecosApiCall(keyECOS, f"901Y073/M/201001/{queryYYYYMM}/I46D")
    dfOilExportQuan.rename(columns = {'DATA_VALUE':'OIL_EXPORT_QUAN'}, inplace = True)

    # (3) 정유 수출입동향-내수판매
    # 8.4.11. 석유제품수급 : [901Y073][M]   /   국내소비[I46C][천배럴]
    # (Ex) https://ecos.bok.or.kr/api/StatisticSearch/MTSA07N58C5X8EB4LMJL/json/kr/1/100/901Y073/M/201001/202209/I46B
    dfOilDomeQuan = lib.apiCall.ecosApiCall(keyECOS, f"901Y073/M/201001/{queryYYYYMM}/I46C")
    dfOilDomeQuan.rename(columns = {'DATA_VALUE':'OIL_DOME_QUAN'}, inplace = True)

    # compile the list of dataframes you want to merge
    df_list = [dfOilImportQuan, dfOilExportQuan, dfOilDomeQuan]
    # grab first dataframe
    oilDataFrame = df_list[0]
    # loop through all but first data frame
    for to_merge in df_list[1:]:
        # result of merge replaces first or previously merged data frame w/ all previous fields
        oilDataFrame = lib.pd.merge(left = oilDataFrame, right = to_merge, left_index = True, right_index = True, how = "outer")

    ## 기타 데이터 삽입
    oilDataFrame['OIL_CRACK_MARGIN'] = ""

    return oilDataFrame