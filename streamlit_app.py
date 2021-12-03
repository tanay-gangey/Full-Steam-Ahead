from collections import OrderedDict
from plotly.express import scatter, scatter_3d
import pandas as pd
import streamlit as st
import time
import numpy as np
import hydralit as hy
from home_app import HomeApp
from dataset_app import DatasetApp
from eda_app import InitialEDAApp
from advanced_app import AdvancedApp
from about_app import AboutApp


app = hy.HydraApp(title='Full Steam Ahead',hide_streamlit_markers=True,use_navbar=True, navbar_sticky=True)

app.add_app("Home", is_home=True, app=HomeApp())
app.add_app("Dataset", app=DatasetApp())
app.add_app("Initial Analysis", app=InitialEDAApp())
app.add_app("Advanced", app=AdvancedApp())
app.add_app("About", app=AboutApp())


app.run()