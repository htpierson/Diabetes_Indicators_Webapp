import streamlit as st
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from pandas_profiling import ProfileReport
import math
import altair as alt

data = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv', 
                   sep = ',', encoding = 'utf-8')
data2 = pd.read_csv('diabetes_012_2.csv', sep = ',', encoding = 'utf-8')
data_corr = pd.read_csv('diabetes_012_corr.csv', sep = ',', encoding = 'utf-8')

tab1, tab2= st.tabs(["Data", "Correlation"])

with tab1:
    st.header('Diabetes Health Indicators')
    display = st.checkbox('Show Dataset')
    if display:
        st.dataframe(data2)
    
    select1 = st.selectbox(
        'Which Indicator would you like to observe?',
        ('HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker',
       'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits',
       'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost',
       'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age',
       'Education', 'Income'))

    alt.data_transformers.disable_max_rows()
    chart1 = alt.Chart(data2).mark_bar().encode(
    y='count()',
    x=alt.Y(select1),
    color = alt.Color('Diabetes_012', scale=alt.Scale(scheme='sinebow')),
    tooltip = ['Diabetes_012', 'count(Diabetes_012)']
    ).properties(
    height=400,
    width=200
    ).interactive()
    st.altair_chart(chart1, use_container_width=True)

with tab2:
    st.header('Diabetes Health Indicator Correlation')
    display2 = st.checkbox('Show Correlation of Diabetes to Indicators')
    if display2:
        st.dataframe(data_corr)
    
    selection = alt.selection_single(on = 'mouseover', nearest = True, fields=['Indicator'])
    color = alt.condition(selection,
                      alt.Color('Indicator:N', scale=alt.Scale(scheme='sinebow'), legend=None),
                      alt.value('lightgray'))
    
    bar = alt.Chart(data_corr).mark_bar().encode(
        x='Indicator',
        y='Correlation',
        color=color,
        tooltip='Correlation'
    )
    
    legend = alt.Chart(data_corr).mark_square().encode(
        y=alt.Y('Indicator', axis=alt.Axis(orient='right')),
        color=color
    ).add_selection(
    selection
    )
    chart2 = bar | legend
    st.altair_chart(chart2, use_container_width=True)

