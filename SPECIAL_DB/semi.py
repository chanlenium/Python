import lib

def makeURL():
    semiDataFrame = lib.yf.download('^SOX',start = '2010-01-01')
    semiDataFrame = semiDataFrame[['Adj Close']]
    semiDataFrame['STD_YM'] = semiDataFrame.index.astype(str).str.slice(0,4) + semiDataFrame.index.astype(str).str.slice(5,7)
    semiDataFrame = semiDataFrame.groupby("STD_YM")['Adj Close'].mean() # 월평균
    semiDataFrame = semiDataFrame.to_frame()
    semiDataFrame.rename(columns = {'Adj Close':'SEMI_PHILADELPHIA'}, inplace = True)
    return semiDataFrame
