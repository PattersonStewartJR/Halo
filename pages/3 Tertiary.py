import streamlit as st
import pandas as pd
import numpy as np
from utils.utils import prettify_mapname
import plotly.graph_objs as go

# Page Title and favicon
st.set_page_config(page_title='Halo Record', layout="wide")

st.write('Welcome to the app!')