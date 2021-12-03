import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class AboutApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('About Us')
        st.info('Hello from the About page - contact details of the team here (and Prof Stamper (pic should be apple pie))')
        