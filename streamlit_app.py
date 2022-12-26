import streamlit as st
from modules import AhrefsModel
from page.upload_csv import upload_csv
from page.url_link import url_link
from multiapp import MultiApp

app = MultiApp()
app.add_app("CSVをアップロード！", upload_csv)
app.add_app("URLを入力！", url_link)
app.run()