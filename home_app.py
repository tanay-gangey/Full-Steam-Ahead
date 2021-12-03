import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class HomeApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('Full Steam Ahead!')
        st.info('Hello from Home - main story here')