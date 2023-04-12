import lib

def makeURL(keyENARA, queryYYYYMM):
    url = f'http://www.index.go.kr/openApi/xml_stts.do?userId=chanlenium&idntfcId={keyENARA}&statsCode=115102&period=201001:{queryYYYYMM}'
    dataFrame = crawlData(url)
    return dataFrame

def crawlData(url):
    response = lib.urlopen(url).read()
    xtree = lib.ET.fromstring(response)

    ## '표' tag에서 '주기'값이 '월'인 tree를 찾아서 월별 데이터 시작 지점을 찾음
    for neighbor in xtree.iter("표"):
        if neighbor.attrib['주기'] == '월':
            rootMonth = neighbor

    ## '항목' tag에서 '이름'값에 따라 항목(수주랑, 건조량, 수주잔량)별 데이터 시작 지점을 찾음
    for child in rootMonth.iter("항목"):
        if child.attrib['이름'] == '수주량':
            sooju = child
        elif child.attrib['이름'] == '건조량':
            gunjo = child
        elif child.attrib['이름'] == '수주잔량':
            soojujan = child

    ## 수주량 데이터 적제
    period = [x.attrib["주기"] for x in sooju]
    soojuValue = [x.text for x in sooju]

    ## 건조량 데이터 적제
    gunjoValue = [x.text for x in gunjo]

    ## 수주잔량 데이터 적제
    soojujanValue = [x.text for x in soojujan]

    shipDataFrame = lib.pd.DataFrame()
    shipDataFrame['STD_YM'] = period
    shipDataFrame['SHIP_ORDER_AMOUNT'] = soojuValue  # 수주량
    shipDataFrame['SHIP_TONNAGE'] = gunjoValue  # 건조량
    shipDataFrame['SHIP_BACKLOG'] = soojujanValue # 수주잔량

    ## 클락슨 데이터 들어갈 자리 삽입
    shipDataFrame.insert(3, 'SHIP_KAJI', '')
    shipDataFrame.insert(5, 'SHIP_BOTTOMS', '')
    shipDataFrame["SHIP_BREAKUP"]=""

    shipDataFrame = shipDataFrame.set_index('STD_YM')
    return shipDataFrame