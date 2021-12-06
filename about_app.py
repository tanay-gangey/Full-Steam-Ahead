import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

from hydralit import HydraHeadApp

#create a wrapper class
class AboutApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        col1 = st.columns(1)         
        col1, col2, col3 = st.columns(3)
        
        with col1:
            image = Image.open("Agarwal-Arav.jpg")
            st.image(image, width=200 )
            st.write("Arav Agarwal")
            st.write("arava@andrew.cmu.edu")
            st.write("Master of Science in Computational Data Science")

        with col2:
            image = Image.open("Gupta-Nikhil.jpg")
            st.image(image, width=200)
            st.write("Nikhil Gupta")
            st.write("nikhilgu@andrew.cmu.edu")
            st.write("Master of Science in Computational Data Science")

        with col3:
            image = Image.open("Virmani-Shubham.jpg")
            st.image(image, width=200)
            st.write("Shubham Virmani")
            st.write("svirmani@andrew.cmu.edu")
            st.write("Master of Science in Computational Data Science")
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            image = Image.open("Gangey-Tanay.jpg")
            st.image(image, width=200)
            st.write("Tanay Gangey")
            st.write("tgangey@andrew.cmu.edu")
            st.write("Master of Science in Computational Data Science")
        
        with col5:
            image = Image.open("Kumar-Urvashi-Priyam.jpg")
            st.image(image, width=200)
            st.write("Urvashi Priyam Kumar")
            st.write("upkumar@andrew.cmu.edu")
            st.write("Master of Science in Computational Data Science")
        
        with col6:
            image = Image.open("Stamper-John.jpg")
            st.image(image, width=200)
            st.write("John Stamper")
            st.write("jstamper@andrew.cmu.edu")
            st.write("Associate Professor, Human-Computer Interaction Institute")
    