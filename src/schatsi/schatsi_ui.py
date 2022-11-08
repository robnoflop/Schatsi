import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np



df1 = pd.read_csv(r"C:\repos\Schatsi\data\output\schatsi_ranking.csv")
df2 = pd.read_csv(r"C:\repos\Schatsi\data\output\documents.csv")

df = df1.merge(df2, on="filename", how="left")
df.title = np.where(df['title'].isna() , df['filename'], df['title'])

fig = px.bar(df, x="rank", y="title", color='cluster', orientation='h')
fig.update_layout(height=15*len(df.filename.unique()))
fig.update_layout( yaxis={'categoryorder':'total ascending'})

st.set_page_config(layout="wide")
st.plotly_chart(fig, use_container_width=True)

