from collections import OrderedDict
from plotly.express import scatter, scatter_3d
import pandas as pd
import streamlit as st
import time
import numpy as np
import hydralit as hy
from home_app import HomeApp
from steam_dataset_app import SteamDatasetApp
from covid_dataset_app import CovidDatasetApp
from advanced_app import AdvancedApp
from about_app import AboutApp
from location_viz import LocationVizApp


app = hy.HydraApp(title='Full Steam Ahead',
                  hide_streamlit_markers=True, use_navbar=True, navbar_sticky=True)

app.add_app("Home", is_home=True, app=HomeApp())
app.add_app("Steam Dataset", app=SteamDatasetApp())
app.add_app("COVID-19 Dataset", app=CovidDatasetApp())
app.add_app("Location Visualization", app=LocationVizApp())
app.add_app("Advanced", app=AdvancedApp())
app.add_app("About", app=AboutApp())


app.run()
