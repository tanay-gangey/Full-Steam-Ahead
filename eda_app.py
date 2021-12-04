import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class InitialEDAApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.markdown("<h1 style='text-align: center;'>About the initial EDA</h1>", unsafe_allow_html=True)
        st.info('Hello from the Iniital EDA Page - initial EDA over here')