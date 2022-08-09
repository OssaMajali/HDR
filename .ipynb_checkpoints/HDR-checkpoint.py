# from win32com.client import Dispatch
import tensorflow as tf
import cv2
import os
from PIL import Image, ImageEnhance
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_drawable_canvas import st_canvas
import plotly.express as px
import plotly.graph_objects as go

model = tf.keras.models.load_model("model.h5")
def preprocessing(img):
    try:
        img =  255 - cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        img =  img.astype('uint8')
        img =  img/255
        img = img.reshape((-1, 28, 28, 1))
        return img
    except Exception as e:
        st.error(e)
        
def main():
    # Create a canvas component
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            Header {visibility: hidden;}
            .stSpinner > div > div {border-top-color: #C8AD7F;}
            .stMarkdown {
            display: grid;
            place-items: left;
            }
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.title("Handwritten Digit Recognition using CNN")
    col1, col2 = st.columns((2))
    __1, __2,__3 = st.columns((3))
    with col1:
        canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=24,
        stroke_color="#C8AD7F",
        background_color= "#eee",
        height=300,
        width = 300,
        key="full_app",
    )
    if canvas_result.image_data is not None:
        image = canvas_result.image_data
        
        if __2.button("Show Predictions"):
            img =  255 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img =  img.astype('uint8')
            img =  img/255
            img = cv2.resize(img,(28,28))
            img.resize(1,28,28,1)
            prediction = model.predict(img)
            probabilityValue = np.amax(prediction)
            
            labels = ['0','1','2','3','4','5','6','7','8','9'] 
            #ypred = pd.DataFrame({'pred': pd.Series(model.predict(img))})
            prediction = pd.DataFrame({'pred': pd.Series(model.predict(img)[0]), 'class':labels})


            fig2 = px.histogram(prediction,x='class',y='pred',color='class', color_discrete_sequence=['#C8AD7F'] )
            
            fig2.update_layout(autosize=False,width=700,height=500,title_text='Sampled Results',
                xaxis_title_text='Class',
                yaxis_title_text='Prediction', )
            
            col2.image(img,width=300)
            st.code(f"Probability value : {'%.2f'%probabilityValue}")
            st.code(f"Value : {np.argmax(model.predict(img))}")
            st.write(fig2)
            
       

    

    


if __name__ == '__main__':
    main()
