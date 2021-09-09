import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.integrate import odeint

st.set_page_config(
    page_title="SIR Model",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("SIR Model")
st.write("Created by Felix Fernando")

col1, col2 = st.columns((1.25, 2))

def deriv(y, t, n, alpha, beta):
    S, I, R = y
    dSdt = -alpha*I*S/n
    dIdt = alpha*I*S/n - beta*I
    dRdt = beta*I
    return dSdt, dIdt, dRdt

with col1:
    alpha = st.slider("Infected Rate ", min_value=0.00001, max_value=1.00000, step=0.00001)
    beta = st.slider("Recovered Rate ", min_value=0.00001, max_value=1.00000, step=0.00001)
    n = st.number_input("Total Population", min_value=0, step=1)
    i0 = st.number_input("Initial Infected Population", min_value=0, step=1)
    r0 = st.number_input("Initial Recovered Population", min_value=0, step=1)

with col2:
    time = st.slider("Time Range", min_value=1 ,max_value=1000)
    y0 = n-i0-r0, i0, r0
    t = np.linspace(1,time,time)
    solve = odeint(deriv, y0, t, args=(n, alpha, beta))
    S, I, R = solve.T
    d = {'Susceptible' : S, 'Infected' : I, 'Recovered' : R}
    data = pd.DataFrame(data = d)
    st.line_chart(data=data, height=400, use_container_width=True)

col3, col4, col5= st.columns((1.25, 1.25, 1))
with col3 : 
    st.subheader("Data")
    st.write(data)
with col4:
    st.subheader("Data when Infected < 0.1")
    st.write(data.loc[data["Infected"] < 0.1])
with col5:
    st.subheader("Parameter")
    st.write("Infected Rate :", alpha)
    st.write("Recovered Rate :", beta)
    st.subheader("Basic Reproduction Rate : ")
    st.write("R0 = ", alpha/beta)
    st.subheader("Infected Population Peak : ")
    st.write("I : ", data["Infected"].max())
    st.write("t : ", data["Infected"].idxmax())