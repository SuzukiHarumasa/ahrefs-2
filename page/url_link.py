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


def url_link():
    st.write("URLを入力！")

    url = st.text_input('URLを入力', placeholder='example.com')

    USERNAME = st.text_input(
        'メールアドレスを入力', key=str, placeholder='example.com')
    PASSWORD = st.text_input(
        'パスワードを入力', key=int,  placeholder='01234567')

    if USERNAME and PASSWORD:

        am = AhrefsModel(USERNAME, PASSWORD)

        if url:
            second_image = Image.open('./img/harumasamama mogumogu.png')

            if USERNAME and PASSWORD:

                df = am.get_page_worth_only_one(url)

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
