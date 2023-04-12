import lib

def init_Webdriver():
    options = lib.webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = lib.webdriver.Chrome(executable_path="C:/Users/dcoh/Downloads/chromedriver.exe", chrome_options=options)
    return driver