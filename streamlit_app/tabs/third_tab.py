import streamlit as st
import pandas as pd
import numpy as np

import add_datas.postgres.config as config
from sqlalchemy import create_engine

try:
    engine = create_engine(config.DATABASE_URL)
    query = "select * from klines limit 1;"
    df = pd.read_sql(query, engine)
except Exception as e:
    print(e)
    print('Trying locally for dev')
    DATABASE_URL = "postgresql://ubuntu:postgres@localhost:5432/crypto_db"
    engine = create_engine(DATABASE_URL)

title = "Data from Postgresql"
sidebar_name = title


def run():

    st.title(title)

    st.markdown(
        """
        This is the data ingested in postgresql
        """
    )
    interval = st.selectbox("Choose the INTERVAL", config.INTERVALS)
    symbol = st.selectbox("Choose the SYMBOL", config.SYMBOLS)


    query = f"select count(*) from klines where interval_id=(select interval_id from interval where interval_name='{interval}') AND symbol_id =(select symbol_id from symbol where symbol_name='{symbol}');"
    df = pd.read_sql(query, engine)
    st.markdown('Will display lines:')
    st.write(df.head())
    query = f"select * from klines where interval_id=(select interval_id from interval where interval_name='{interval}') AND symbol_id =(select symbol_id from symbol where symbol_name='{symbol}');"
    df = pd.read_sql(query, engine)
    #st.write(pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")))
    #st.write(df.head())
        
    prices, dates = [],[]
    for index,kline in df.iterrows():
        prices.append(kline['close'])
        dates.append(kline['close_time'])
    chart_data = pd.DataFrame(prices, dates)
    st.line_chart(chart_data)
