from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.parse import urlparse

USERNAME = "media_general@joint.works"
PASSWORD = "Jointinc"


class AhrefsModel():

    def __init__(self,USERNAME,PASSWORD):
        self.username = USERNAME
        self.password = PASSWORD

    def mk_driver(self):
        options = webdriver.chrome.options.Options()
        # options.add_argument("-headless")
        # options.add_argument("-no-sandbox")
        profile_path = './Profile ahrefs'
        options.add_argument('--user-data-dir=' + profile_path)
        driver = webdriver.Chrome(options=options)

        return driver


    def login_ahrefs(self,driver):
        target_url = "https://app.ahrefs.com/user/login"
        driver.get(target_url)
        sleep(5)

        username_input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[1]/div/input')
        print("とれた！")

        username_input.send_keys(self.username)
        sleep(1)

        password_input = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[2]/div/div/input')
        password_input.send_keys(self.password)
        sleep(1)

        login_burron = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/button/div')
        login_burron.submit()
        sleep(5)

    def get_page_worth(self, driver,data):
        
        df = pd.DataFrame()

        for domain in data['ドメイン'].to_list():
            domain_1 = urlparse(domain).netloc

            if domain_1:
                domain = domain_1

            print(domain)
            ahrefs_url = "https://app.ahrefs.com/positions-explorer/top-subfolders/subdomains/jp/all/all/all/all/all/all/all/1/traffic_desc?target="+domain+"%2F"

            driver.get(ahrefs_url)
            sleep(5)

            df_tmp = driver.find_element(By.XPATH,'//*[@id="main_se_data_table"]')

            html = df_tmp.get_attribute('outerHTML')
            df_tmp = pd.read_html(html)

            df_tmp = df_tmp[0].head(1)

            df_tmp = df_tmp[['トラフィック', '価値', 'キーワード']]
            df_tmp.insert(0,'ドメイン',domain)
            df_tmp.insert(4,'ahrefs上位ページ取得URL',ahrefs_url)

            df = pd.concat([df, df_tmp], join='outer')
            driver.quit()

        return df
        
    def get_page_worth_only_one(self,driver, url):

        df = pd.DataFrame()

        domain = urlparse(url).netloc

        if domain:
            url = domain

        print(url)
        ahrefs_url = "https://app.ahrefs.com/positions-explorer/top-subfolders/subdomains/jp/all/all/all/all/all/all/all/1/traffic_desc?target="+url+"%2F"

        driver.get(ahrefs_url)
        sleep(5)

        df_tmp = driver.find_element(By.XPATH,'//*[@id="main_se_data_table"]')

        html = df_tmp.get_attribute('outerHTML')
        df_tmp = pd.read_html(html)

        df_tmp = df_tmp[0].head(1)

        df_tmp = df_tmp[['トラフィック', '価値', 'キーワード']]
        df_tmp.insert(0,'ドメイン',url)
        df_tmp.insert(4,'ahrefs上位ページ取得URL',ahrefs_url)

        df = pd.concat([df, df_tmp], join='outer')
        driver.quit()

        return df
