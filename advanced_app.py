import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class AdvancedApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('Some advanced Analytics')
        st.info('Hello from Advanced page - ML model and related stuff here')