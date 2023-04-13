import lib

today = lib.date.today()

def appendDf(cutoffYYYYMM):
    # additionalCommon와 additionalExportImport를 합쳐서 additionalCommon_IT_EFAS_COMMON_DB를 만듦
    additionalCommon = lib.pd.read_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/additionalCommon.xlsx')
    additionalCommon['STD_YM'] = additionalCommon['STD_YM'].astype(str)
    additionalCommon['EFAS_CD'] = additionalCommon['EFAS_CD'].astype(str)
    print(lib.tabulate(additionalCommon, headers='keys', tablefmt='psql'))

    additionalExportImport = lib.pd.read_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/additionalExportImport.xlsx')
    additionalExportImport['STD_YM'] = additionalExportImport['STD_YM'].astype(str)
    additionalExportImport['EFAS_CD'] = additionalExportImport['EFAS_CD'].astype(str)
    print(lib.tabulate(additionalExportImport, headers='keys', tablefmt='psql'))

    df = lib.pd.concat([additionalCommon, additionalExportImport], axis = 1)
    additionalCommon_IT_EFAS_COMMON_DB = df.loc[:, ~df.columns.duplicated()]
    print(lib.tabulate(df, headers='keys', tablefmt='psql'))
    additionalCommon_IT_EFAS_COMMON_DB.to_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/additionalCommon_IT_EFAS_COMMON_DB.xlsx')

    # 기존 적재파일(IT_EFAS_INDU_COMMON_DB.xlsx) 오픈
    IT_EFAS_INDU_COMMON_DB = lib.pd.read_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/IT_EFAS_INDU_COMMON_DB.xlsx')
    IT_EFAS_INDU_COMMON_DB = IT_EFAS_INDU_COMMON_DB.loc[IT_EFAS_INDU_COMMON_DB['STD_YM'] < cutoffYYYYMM]
    IT_EFAS_INDU_COMMON_DB['STD_YM'] = IT_EFAS_INDU_COMMON_DB['STD_YM'].astype(str)
    IT_EFAS_INDU_COMMON_DB['EFAS_CD'] = IT_EFAS_INDU_COMMON_DB['EFAS_CD'].astype(str)
    print(lib.tabulate(IT_EFAS_INDU_COMMON_DB, headers='keys', tablefmt='psql'))

    updatedIT_EFAS_INDU_COMMON_DB = lib.pd.concat([IT_EFAS_INDU_COMMON_DB, additionalCommon_IT_EFAS_COMMON_DB], axis = 0, ignore_index=True)
    print(lib.tabulate(updatedIT_EFAS_INDU_COMMON_DB, headers='keys', tablefmt='psql'))
    #updatedIT_EFAS_INDU_COMMON_DB = updatedIT_EFAS_INDU_COMMON_DB.reset_index(drop=True)
    updatedIT_EFAS_INDU_COMMON_DB.to_excel(f'C:/Users/dcoh/Desktop/EFAS/COMMON_DB/{today}_updatedIT_EFAS_INDU_COMMON_DB.xlsx', index=False)
