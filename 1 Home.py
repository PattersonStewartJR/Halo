import streamlit as st
import pandas as pd
import numpy as np
from utils.utils import prettify_mapname
import plotly.graph_objs as go

# Page Title and favicon
st.set_page_config(page_title='Halo Record', layout="wide", page_icon='pics/favicon.ico')

# Data Load & Data Wrangling
df1 = pd.read_excel('Halo Record.xlsx')
df1 = df1.dropna(subset=['W/L'])
df1['Map Name Pretty'] = df1['Map'].apply(prettify_mapname)
df1['Teamed'] = df1['Teamed'].apply(prettify_mapname)

# Sidebar UI Elements
solo_display = st.sidebar.checkbox(label='Solo', value=True)
duo_display = st.sidebar.checkbox(label='Duo', value=True)
rank_range = st.sidebar.slider('Select a range of values',int(df1['Rank'].min()), int(df1['Rank'].max()), (int(df1['Rank'].min()), int(df1['Rank'].max())), step=1)
map_selection = st.sidebar.multiselect(
   label='Maps', 
   options=list(df1['Map'].unique()),
   label_visibility ="collapsed",
   format_func = prettify_mapname,
   placeholder='Choose Map(s)')

# Image of Selected Map
if len(map_selection)>0:
    st.sidebar.image('pics/'+map_selection[0]+'.png', 
                     caption=prettify_mapname(map_selection[0]))

# Data Filtering By Solo/Duo
df2 = df1.copy(deep=True)
if solo_display and not duo_display:
    df2 = df2[df2['Teamed']=='solo']
elif duo_display and not solo_display:
    df2 = df2[df2['Teamed']!='solo']
    
# Data Filtering By Map Selection
if len(map_selection)>0:
    df2 = df2[df2['Map'].isin(map_selection)]
    
# Data Filtering By Rank Range
df2 = df2[df2['Rank']>=rank_range[0]]
df2 = df2[df2['Rank']<=rank_range[1]]

# Metric Cards 
column1, column2, column3 = st.columns([1, 1, 1])
with column1:
    st.metric('Win Rate', value=f"{len(df2[df2['W/L']=='W'])/len(df2):.0%}")
with column2:
    st.metric('KD Spread (Net)', value=sum(df2['Spread']))
with column3:
    st.metric('KD Spread (Average)', value=round(sum(df2['Spread'])/len(df2), 1))
    

tab1, tab2 = st.tabs(["Graph", "Data"])

with tab1:


    # Hover Template Elements
    hover_data=df2[['Map Name Pretty', 'Teamed']]
    hover_template='<br>'.join(['Map: <b>%{customdata[0]}</b>','KD Spread: <b>%{y}</b>','Solo/Duo: <b>%{customdata[1]}</b>'])
    config={'displaylogo': False, "modeBarButtonsToRemove": ['pan2d','lasso2d','toImage','zoomIn2d','zoomOut2d']}

    # Plot of KD Spread
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.index, 
                            y=df2.Spread, 
                            line=dict(dash='solid', color='rgb(124, 252, 0)'),
                            customdata=hover_data,
                            hovertemplate=hover_template,
                            name=''))
    fig.add_trace(go.Scatter(x=df2.index, 
                            y=df2.Spread.where(df2.Spread < 0), 
                            mode='markers', 
                            marker=dict(color='white', symbol='circle-open-dot'),
                            customdata=hover_data,
                            hovertemplate=hover_template,
                            name=''))
    fig.add_trace(go.Scatter(x=df2.index, 
                            y=df2.Spread.where(df2.Spread > 0), 
                            mode='markers', 
                            marker=dict(color='white', symbol='circle'),
                            customdata=hover_data,
                            hovertemplate=hover_template,
                            name=''))
    fig.add_hline(y=0, line_color="white")
    fig.update_layout(showlegend=False)
    fig.update_layout(title={'text': "KD Spread Over Time", 'y':0.82, 'x':0.12, 'xanchor': 'center', 'yanchor': 'top'})
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config=config)

with tab2:
    st.dataframe(df2)