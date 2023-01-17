from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import os


class AhrefsModel():

    def __init__(self, USERNAME, PASSWORD):
        self.username = USERNAME
        self.password = PASSWORD

    def mk_driver(self):
        options = webdriver.chrome.options.Options()
        # chrome_options = webdriver.ChromeOptions()
        options.add_argument("-headless")
        options.add_argument("-no-sandbox")
        self.profile_path = './Profile ahrefs'
        options.add_argument('--user-data-dir=' + self.profile_path)
        UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        options.add_argument('--user-agent=' + UA)

        driver = webdriver.Chrome(options=options)

        # driver = webdriver.Chrome(DRIVER_PATH,options=options)

        return driver

    def login_ahrefs(self, driver):
        target_url = "https://app.ahrefs.com/user/login"

        driver.get(target_url)
        sleep(5)

        username_input = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[1]/div/input')
        print("とれた！")

        username_input.send_keys(self.username)
        sleep(1)

        password_input = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[2]/div/div/input')
        password_input.send_keys(self.password)
        sleep(1)

        login_burron = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/button/div')
        login_burron.submit()
        sleep(5)
        driver.quit()

    def get_page_worth(self, data):
        driver = self.mk_driver()
        self.login_ahrefs(driver)
        df = pd.DataFrame()

        for i, url in enumerate(data['ドメイン'].to_list()):

            domain = urlparse(url).netloc

            if i == 0:
                input_place = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/input')
                input_place.send_keys(domain)

                serch_button = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/button')
                serch_button.click()
                sleep(7)

                top_subfolders = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[3]/div[2]/div[3]/a')
                top_subfolders.click()
                sleep(7)
            else:
                delete_button = driver.find_element(
                    By.XPATH, '//*[@id="clear_se_pe_target"]')
                delete_button.click()

                input_place_sec = driver.find_element(
                    By.XPATH, '//*[@id="se_pe_target"]')
                input_place_sec.send_keys(domain)

                serch_button_sec = driver.find_element(
                    By.XPATH, '//*[@id="se_pe_start_analysing"]')
                serch_button_sec.click()
                sleep(7)

            df_tmp = driver.find_element(
                By.XPATH, '//*[@id="main_se_data_table"]')

            html = df_tmp.get_attribute('outerHTML')
            df_tmp = pd.read_html(html)

            df_tmp = df_tmp[0].head(1)
            df_tmp.columns = ['#', 'トラフィック', 'トラフィック.1', '価値', 'キーワード', 'ページ', 'パス',
                              'トップキーワード', '検索ボリューム', '順位', '順位..1']

            df_tmp = df_tmp[['トラフィック', '価値', 'キーワード', 'ページ']]

            ahrefs_url = driver.current_url

            df_tmp.insert(0, 'ドメイン', domain)
            df_tmp.insert(5, 'ahrefs上位ページ取得URL', ahrefs_url)

            df = pd.concat([df, df_tmp], join='outer')
            print(f"{domain}完了")

        driver.quit()

    def get_page_worth_only_one(self, url):

        driver = self.mk_driver()
        self.login_ahrefs(driver)

        df = pd.DataFrame()

        domain = urlparse(url).netloc

        if domain:
            url = domain

        input_place = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/input')
        input_place.send_keys(domain)

        serch_button = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/button')
        serch_button.click()
        sleep(7)

        top_subfolders = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[3]/div[2]/div[3]/a')
        top_subfolders.click()
        sleep(7)

        df_tmp = driver.find_element(By.XPATH, '//*[@id="main_se_data_table"]')

        html = df_tmp.get_attribute('outerHTML')
        df_tmp = pd.read_html(html)

        df_tmp = df_tmp[0].head(1)
        df_tmp.columns = ['#', 'トラフィック', 'トラフィック.1', '価値', 'キーワード', 'ページ', 'パス',
                          'トップキーワード', '検索ボリューム', '順位', '順位..1']

        df_tmp = df_tmp[['トラフィック', '価値', 'キーワード', 'ページ']]

        ahrefs_url = driver.current_url

        df_tmp.insert(0, 'ドメイン', domain)
        df_tmp.insert(5, 'ahrefs上位ページ取得URL', ahrefs_url)

        df = pd.concat([df, df_tmp], join='outer')
        print(f"{domain}完了")

    def get_page_worth_2(self, data):
        driver = self.mk_driver()
        self.login_ahrefs(driver)
        df = pd.DataFrame()
        for i, domain in enumerate(data['ドメイン'].to_list()):
            if i == 0:
                input_place = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/input')
                input_place.send_keys(domain)

                serch_button = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div[1]/button')
                serch_button.click()
                sleep(7)

                top_subfolders = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[3]/div[2]/div[3]/a')
                top_subfolders.click()
                sleep(10)

            else:
                delete_button = driver.find_element(
                    By.XPATH, '//*[@id="clear_se_pe_target"]')
                delete_button.click()

                input_place_sec = driver.find_element(
                    By.XPATH, '//*[@id="se_pe_target"]')
                input_place_sec.send_keys(domain)

                serch_button_sec = driver.find_element(
                    By.XPATH, '//*[@id="se_pe_start_analysing"]')
                serch_button_sec.click()
                sleep(10)

            df_tmp = driver.find_element(
                By.XPATH, '//*[@id="main_se_data_table"]')

            html = df_tmp.get_attribute('outerHTML')
            df_tmp = pd.read_html(html)

            df_tmp = df_tmp[0].head(1)
            df_tmp.columns = ['#', 'トラフィック', 'トラフィック.1', '価値', 'キーワード', 'ページ', 'パス',
                              'トップキーワード', '検索ボリューム', '順位', '順位..1']

            df_tmp = df_tmp[['トラフィック', '価値', 'キーワード', 'ページ',]]

            ahrefs_url = driver.current_url

            df_tmp.insert(0, 'ドメイン', domain)
            df_tmp.insert(5, 'ahrefs上位ページ取得URL', ahrefs_url)

            df = pd.concat([df, df_tmp], join='outer')
            print(f"{domain}完了")
        driver.quit()
        return df
