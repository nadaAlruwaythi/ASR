# Libraries to be used ------------------------------------------------------------

import streamlit as st
import requests
import json
import os
import torch
import numpy as np
from scipy.io import wavfile
from IPython.display import Audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# title and favicon ------------------------------------------------------------

st.set_page_config(
    page_title="Automatic Speech Recognition", layout="wide"
)
# App layout width -------------------------------------------------
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

# logo and header -------------------------------------------------


st.markdown("""
<style>
body {
  background: #9bd3ea; 
  background: -webkit-linear-gradient(to right, #9bd3ea, #493240); 
  background: linear-gradient(to right, #9bd3ea, #493240); 
  text-align:center;
}
</style>
    """, unsafe_allow_html=True)









c30, c31 = st.columns([2.5, 1])

with c30:
    # st.image("logo.jpg", width=350)
    st.header('Automatic Speech Recognition')
    st.caption('Automatic Speech Recognition (ASR), also known as Speech to Text (STT), is the task of transcribing a given audio to text. It has many applications, such as voice user interfaces.')


    

st.text("")

# region Main

# multi navbar -------------------------------------------------


def main():
    pages = {

        " Convert Speech To Text": API_key,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
            }
        )

    with st.sidebar:
        page = st.radio(" ", tuple(pages.keys()))

    pages[page]()


# endregion main

# Free mode -------------------------------------------------



# Custom API key mode -------------------------------------------------


def API_key():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:

        with st.form(key="my_form"):

            text_input = "NadaA"

            f = st.file_uploader("", type=[".wav"])

         
            submit_button = st.form_submit_button(label="Text")

    if not submit_button:

        st.stop()

    else:

        try:

            if f is not None:
                path_in = f.name
                # Get file size from buffer
                # Source: https://stackoverflow.com/a/19079887
                old_file_position = f.tell()
                f.seek(0, os.SEEK_END)
                getsize = f.tell()  # os.path.getsize(path_in)
                f.seek(old_file_position, os.SEEK_SET)
                getsize = round((getsize / 1000000), 1)
                # st.caption("The size of this file is: " + str(getsize) + "MB")
                # getsize

                if getsize < 30:  # File more than 30MB

                    # To read file as bytes:
                    bytes_data = f.getvalue()

                    api_token = text_input

                    headers = {"Authorization": f"Bearer {api_token}"}
                    API_URL = "https://api-inference.huggingface.co/models/kmfoda/wav2vec2-large-xlsr-arabic"
                    # processor = Wav2Vec2Processor.from_pretrained("kmfoda/wav2vec2-large-xlsr-arabic")
                    # model = Wav2Vec2ForCTC.from_pretrained("kmfoda/wav2vec2-large-xlsr-arabic",num_labels=1)
                    def query(data):
                        response = requests.request(
                            "POST",API_URL, headers=headers, data=data
                        )
                        return json.loads(response.content.decode("utf-8"))

                    data = query(bytes_data)

                   
                    values_view = data.values()
                    value_iterator = iter(values_view)
                    text_value = next(value_iterator)
                    text_value = text_value.lower()

                    st.success(text_value)
                 
                 
                    c0, c1 = st.columns([2, 2])

                    with c0:
                        st.download_button(
                            "Download",
                            text_value,
                            file_name=None,
                            mime=None,
                            key=None,
                            help=None,
                            on_click=None,
                            args=None,
                            kwargs=None,
                        )

                else:
                    st.error(
                        "size limted exceeded(30MB) "
                    )
                    st.stop()

            else:
                path_in = None
             

        except ValueError:
            "ValueError"


# Notes about the app -------------------------------------------------



    st.markdown("")

    st.markdown("")

if __name__ == "__main__":
    main()