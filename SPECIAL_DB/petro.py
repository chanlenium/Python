import lib

def makeURL(ironDataFrame):
    petroDataFrame = lib.pd.DataFrame()
    petroDataFrame['STD_YM'] = ironDataFrame.index
    petroDataFrame['PETRO_EXPORT_QUAN'] = ""
    petroDataFrame['PETRO_DOME_QUAN'] = ""
    petroDataFrame = petroDataFrame.set_index('STD_YM')
    return petroDataFrame

