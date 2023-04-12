import lib

## ECOS API CALL function
def ecosApiCall(keyECOS, url_tail):
  url = f'https://ecos.bok.or.kr/api/StatisticSearch/{keyECOS}/json/kr/1/1000/{url_tail}'
  r = lib.requests.get(url)
  jo = r.json()
  df = lib.pd.DataFrame(jo['StatisticSearch']['row'])
  df = df[['TIME', 'DATA_VALUE']]
  df.rename(columns = {'TIME' : 'STD_YM'}, inplace = True)
  df['DATA_VALUE'] = lib.pd.to_numeric(df['DATA_VALUE'])
  df = df.set_index('STD_YM')
  return df

## KOSIS API CALL function
def kosisApiCall(url):
    context = lib.ssl.SSLContext(lib.ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('C:/Users/dcoh/AppData/Local/.certifi/cacert.pem')
    context.check_hostname = False
    r = lib.requests.get(url)
    return r.json()