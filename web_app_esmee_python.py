import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

DB_USER = "deliverable_taskforce"
DB_PASSWORD = "learn_sql_2024"
DB_HOSTNAME = "training.postgres.database.azure.com"
DB_NAME = "deliverable"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:5432/{DB_NAME}")

df = pd.read_sql_query(
    """
    select r2.datetime::date as dt, count(*) as countPerDay, r.location_city as city
    from restaurants r
    join reviews r2 on r.restaurant_id = r2.restaurant_id
    where
        (r.location_city = 'Amsterdam' or r.location_city = 'Rotterdam' or r.location_city = 'Groningen')
        and r2.datetime >= '2023-01-01' and r2.datetime <='2023-12-31'
    group by dt, city
    """,
    con=engine,
)
# print(df)

data = df.groupby(["city"], as_index=False)["countperday"].mean()
st.data_editor(data)

# group_labels = ["Amsterdam", "Rotterdam", "Groningen"]
df = df.sort_values("dt")
# data2 = df.groupby(["city"], as_index=False)
# st.data_editor(data2)
# px.line(df.sort_values("dt"), x="dt", y="countperday", color="city")
# filter_time = st.slider("Days", 0, 365)
# print(df["dt"].min())
mint = df["dt"].min()
maxt = df["dt"].max()
# st.sidebar.slider
filter_time = st.slider("Days", min_value=mint, max_value=maxt, value=[mint, maxt])
# filtered_df = df.loc[(df["dt"] >= filter_time[0]) and (df["dt"] <= filter_time[1])]
filtered_df = df.loc[((df["dt"] >= filter_time[0]) & (df["dt"] <= filter_time[1]))]

st.plotly_chart(px.line(filtered_df, x="dt", y="countperday", color="city"))
