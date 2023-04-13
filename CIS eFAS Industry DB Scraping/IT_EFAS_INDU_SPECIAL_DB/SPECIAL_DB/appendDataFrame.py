import lib

today = lib.date.today()

def appendDf(fileName):
    ## 수기 입력한 데이터 합치기
    ## 순서 : 수기 입력한 엑셀파일을 업로드 -> 파일을 읽어들임(read_excel) -> 합치기 -> 엑셀파일 반출(to_excel)

    # BLANK_IT_EFAS_INDU_SPECIAL_DB와 IT_EFAS_INDU_SPECIAL_DB을 읽음
    BLANK_IT_EFAS_INDU_SPECIAL_DB = lib.pd.read_excel(f'C:/Users/dcoh/Desktop/EFAS/SPECIAL_DB/BLANK_IT_EFAS_INDU_SPECIAL_DB.xlsx')
    IT_EFAS_INDU_SPECIAL_DB = lib.pd.read_excel(f'C:/Users/dcoh/Desktop/EFAS/SPECIAL_DB/{fileName}.xlsx')
    IT_EFAS_INDU_SPECIAL_DB.rename(columns={ IT_EFAS_INDU_SPECIAL_DB.columns[0]: "STD_YM" }, inplace = True)

    # BLANK_IT_EFAS_INDU_SPECIAL_DB와 IT_EFAS_INDU_SPECIAL_DB의 길이를 맞춤
    cutoff = min(max(BLANK_IT_EFAS_INDU_SPECIAL_DB['STD_YM']), max(IT_EFAS_INDU_SPECIAL_DB['STD_YM']))
    BLANK_IT_EFAS_INDU_SPECIAL_DB = BLANK_IT_EFAS_INDU_SPECIAL_DB[BLANK_IT_EFAS_INDU_SPECIAL_DB['STD_YM'] <= cutoff]
    IT_EFAS_INDU_SPECIAL_DB = IT_EFAS_INDU_SPECIAL_DB[IT_EFAS_INDU_SPECIAL_DB['STD_YM'] <= cutoff]

    # 데이터 합치기
    IT_EFAS_INDU_SPECIAL_DB[BLANK_IT_EFAS_INDU_SPECIAL_DB.columns.values.tolist()] = BLANK_IT_EFAS_INDU_SPECIAL_DB[BLANK_IT_EFAS_INDU_SPECIAL_DB.columns.values.tolist()].values
    IT_EFAS_INDU_SPECIAL_DB = IT_EFAS_INDU_SPECIAL_DB.set_index('STD_YM')
    print(lib.tabulate(IT_EFAS_INDU_SPECIAL_DB, headers='keys', tablefmt='psql'))

    # 파일 반출
    IT_EFAS_INDU_SPECIAL_DB.to_excel(f'C:/Users/dcoh/Desktop/EFAS/SPECIAL_DB/final_IT_EFAS_INDU_SPECIAL_DB.xlsx')

    return None