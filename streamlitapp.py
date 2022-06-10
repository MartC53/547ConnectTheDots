from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import PIL
import time
import tifffile as tiff
import base64
import requests
from model2 import prediction
import matplotlib.pyplot as plt
from io import BytesIO
from tifffile import imread, imwrite
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from IPython.display import clear_output
from numpy import expand_dims
from matplotlib import pyplot
from PIL import Image
import streamlit as st
import numpy as np



st.title("Connect the Dots")
st.subheader("Quantitative Isothermal Amplification Machine Learning")
st.write('The goal of this project is to develop the quantified model to predict the cps of input figure')
         
col1, col2 = st.columns(2)
col1.metric('Team Member', 'Coleman Martin ')
col2.metric('Team Member', 'Xuetao Ma')
col3, col4 = st.columns(2)
col3.metric('Team Member', 'Hsuan-Yu Chen')
col4.metric('Team Member', 'Shuyan Zhao')

         
pic,model= st.columns(2)
pic.write('Here is the original picture')


pic.subheader('Original picture-30cps')
@st.cache(allow_output_mutation=True)
def load_pic_img(file_name):
    ex_pic = PIL.Image.open(file_name)
    return ex_pic
e_pic=load_pic_img('Datasets/streamlit_profile/30.2.tiff')
## test 
resized_e_pic = e_pic.resize((200, 200))
pic.image(resized_e_pic)

model.write('Here is the picture after model output')
model.subheader('model processing picture')


@st.cache(allow_output_mutation=True)
def load_model_img(file_name):
    ex_model = PIL.Image.open(file_name)
    return ex_model
ex_model=load_model_img('Datasets/streamlit_profile/processing.png')
resized_ex = ex_model.resize((200, 200))
model.image(resized_ex)


photo_names = ["<select>", "30.tif", "100.tif", "300.tif",
               "1000.tif", "3000.tif", "10000.tif","30000.tif" ,"100000.tif"]

photo_dir = "Datasets/All/test/"
photo_list = st.sidebar.selectbox('Select an image:', list(photo_names))




file = st.file_uploader("Upload the image that you are wanting to processing here, either browse or drag ", type=("tif"))
if file is not None:
    st.image(file)
    st.header('Uploaded image')
    file_buffer=prediction(file)
    st.header(file_buffer)
    

    

    
   

if photo_list != "<select>" and file is None:
    st.title("Selected image")
    st.image("{}{}".format(photo_dir, photo_list))
    list_buffer = prediction("{}{}".format(photo_dir, photo_list))
    st.header(list_buffer)
    
    
   


