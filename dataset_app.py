import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class DatasetApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('dataset info')
        st.info('Hello from the Dataset Page - dataset provenance,stats viz and cleaning info over here')