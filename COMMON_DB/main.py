import common
import exportImport
import appendDataFrame

# addtionalCommonDB 데이터 추출시 사용할 parameter (조회 시작 년월)
# 데이터 타입(string)에 신경쓸것
commonDBfromYYYY = '2023'
commonDBfromMM = '1'

# additionalExportImport 데이터 추출시 사용할 parameter (조회 시작년, 조회 종료년, 조회 종료월)
startYYYY = int(commonDBfromYYYY)
toYYYY = 2023
toMM = 1

# appendDataFrame 실행 시 기존 적재된 DB에서 cutoff해야할 시점(commonDBfromYYYY + commonDBfromMM)
#cutoffYYYYMM = 202201
cutoffMM = '0' + commonDBfromMM if len(commonDBfromMM) == 1 else commonDBfromMM
cutoffYYYYMM = int(commonDBfromYYYY + cutoffMM)

common.makeCommonDB(commonDBfromYYYY, commonDBfromMM)
exportImport.makeExportImportDB(startYYYY, toYYYY, toMM)
appendDataFrame.appendDf(cutoffYYYYMM)