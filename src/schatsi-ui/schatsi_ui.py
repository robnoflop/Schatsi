
import glob
import os
from time import sleep
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from components.uploader import Uploader
from schatsi.jobs.parallel_job import ParallelJob
from schatsi.jobs.single_job import SingleJob


UPLOAD_PATH = r"C:\repos\Schatsi\data\input"
OUTPUT_PATH = r"C:\repos\Schatsi\data\output"
METADATA_PATH = r"C:\repos\Schatsi\data\metadata"



def upload_done(upload_path):
    job = SingleJob(upload_path, OUTPUT_PATH, METADATA_PATH + "/functional_terms.csv", METADATA_PATH + "/negative_terms.csv")
    job.process()
    st.session_state.plotter.create_plot()

class Plotter():

    def __init__(self) -> None:
        self.plot_container = st.empty()

    def create_plot(self):
        df = pd.read_csv(OUTPUT_PATH + "\schatsi_ranking.csv")
        df = df.drop_duplicates()
        df.filename = "file_" + df.filename

        fig = px.bar(df, x="rank", y="filename", color='cluster', orientation='h')
        fig.update_layout(height=15*len(df.filename.unique()))
        fig.update_layout( yaxis={'categoryorder':'total ascending'})
        
        self.plot_container.plotly_chart(fig, use_container_width=True, key="plot")


st.set_page_config(layout="wide")
    
Uploader(UPLOAD_PATH, upload_done).ui()

plotter = Plotter()
st.session_state.plotter = plotter
plotter.create_plot()

    