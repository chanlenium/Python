import lib

# 자동차 산업협회 홈페이지 url로 이동
url = "https://www.kama.or.kr/MainController" 

def crawlData(driver):
    driver.get(url)
    driver.find_element(lib.By.XPATH, '//*[@id="gnb"]/li[1]/a[1]').click()
    lib.time.sleep(1)
    driver.find_element(lib.By.XPATH, '//*[@id="user_id"]').send_keys("kcredit")
    driver.find_element(lib.By.XPATH, '//*[@id="user_pw"]').send_keys("kcredit2019!")
    driver.find_element(lib.By.XPATH, '//*[@id="content"]/form/div/div/a').send_keys(lib.Keys.ENTER)
    lib.time.sleep(1)

    # 자동차통계DB(STATISTICS) 클릭
    driver.find_element(lib.By.XPATH, '//*[@id="wrap"]/div[2]/div/ul[2]/li[1]/a').send_keys(lib.Keys.ENTER)
    lib.time.sleep(1)

    # 조회조건 설정 : 2020년 1월 부터 최근년도 12월까지
    select = lib.Select(driver.find_element(lib.By.XPATH, '//*[@id="statsYear"]'))
    select.select_by_visible_text('2010년')
    select.select_by_value('2010')
    select = lib.Select(driver.find_element(lib.By.XPATH, '//*[@id="statsMonthE"]'))
    select.select_by_visible_text('12월')
    select.select_by_value('12')
    driver.find_element(lib.By.XPATH, '//*[@id="checkBox"]/table/tbody/tr[2]/td/label').click()
    driver.find_element(lib.By.XPATH, '//*[@id="checkBox"]/div/a').send_keys(lib.Keys.ENTER)

    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[1])
    lib.time.sleep(1)

    # Printing the whole body text
    # print(browser.find_element(By.XPATH, "/html/body").text)

    driver.find_element(lib.By.XPATH, '//*[@id="proceed-button"]').send_keys(lib.Keys.ENTER)
    lib.time.sleep(1)

    motorDataFrame = lib.pd.read_html(driver.page_source)[2]
    motorDataFrame.rename(columns=motorDataFrame.iloc[1], inplace =True)
    motorDataFrame = motorDataFrame.iloc[2:]
    motorDataFrame = motorDataFrame[~motorDataFrame['월별'].isnull()] # NaN제거

    # 월의 자릿수에 따라 앞에 '0'을 붙임
    def assignMonth(row): 
        if int(row) >= 10: 
            result = row 
        else: 
            result = '0' + row 
        return result

    motorDataFrame['STD_YM'] = motorDataFrame['년도'].str[0:-1:1].copy() + motorDataFrame['월별'].str[0:-1:1].copy().apply(assignMonth) # str[start:stop:step])


    motorDataFrame = motorDataFrame[['STD_YM', '생산', '내수', '수출(수량)', '수출(금액)']]
    motorDataFrame.rename(columns = {'생산' : 'MOTOR_PROD_QUAN', '내수' : 'MOTOR_DOME_QUAN', '수출(수량)' : 'MOTOR_EXPORT_QUAN', '수출(금액)' : 'MOTOR_EXPORT_SALES'}, inplace = True)
    motorDataFrame.set_index('STD_YM', inplace =True)

    motorDataFrame = motorDataFrame.loc[~(motorDataFrame==0).all(axis=1)]

    return motorDataFrame