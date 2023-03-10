import streamlit as st
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.parse import urlparse

from modules import AhrefsModel
from PIL import Image

IMG_PATH = './tmp_dir'


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def upload_csv():

    data = st.file_uploader("ファイルアップロード", type='csv')

    USERNAME = st.text_input(
        'メールアドレスを入力', key=str, placeholder='example.com')
    PASSWORD = st.text_input(
        'パスワードを入力', key=int,  placeholder='01234567')

    if USERNAME and PASSWORD:
        if data:
            second_image = Image.open('./img/harumasamama mogumogu.png')

            st.image(second_image, width=300)
            data = pd.read_csv(data, encoding="utf-8")

            am = AhrefsModel(USERNAME, PASSWORD)

            df = am.get_page_worth_2(data)

            st.success('Done!!!', icon="✅")
            df.to_csv('./output/output.csv',
                      index=False)

            st.dataframe(df)
            df = convert_df(df)
            button = st.download_button(
                label="Download",
                data=df,
                file_name='output.csv',
                mime='text/csv',
            )

            if button:
                third_image = Image.open('./img/harumake6.png')
                st.image(third_image, width=300)
