import streamlit as st
from pydub import AudioSegment, silence
import speech_recognition as sr
import os

st.set_page_config(
    page_title="Automatic Speech Recognition", layout="wide"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
body {
  background: #eff3f4; 
  background: -webkit-linear-gradient(to right, #eff3f4, #493240); 
  background: linear-gradient(to right, #eff3f4, #493240); 
  text-align:center;
}
</style>
    """, unsafe_allow_html=True)

st.header('Automatic Speech Recognition')
st.caption('Automatic Speech Recognition (ASR), also known as Speech to Text (STT), is the task of transcribing a given audio to text. It has many applications, such as voice user interfaces.')


recog=sr.Recognizer()
final_result=""
st.write('For English')
audio=st.file_uploader("Upload Your Audio File", type=['wav'])
if audio:
    st.audio(audio)
    audio_segment=AudioSegment.from_file(audio)
    chunks=silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS-20, keep_silence=100)
    for index,chunk in enumerate(chunks):
        chunk.export(str(index)+".wav", format="wav")
        with sr.AudioFile(str(index)+".wav") as source:
            recorded=recog.record(source)
            try:
                text=recog.recognize_google(recorded,language='ar')
                final_result=final_result+" "+text
                print(text)
            except:
                print("None")
                final_result=final_result+" Unaudible"
    with st.form("Result"): 
        result=st.text_area("TEXT", value=final_result) 
        d_btn=st.form_submit_button("Download")    
        if d_btn:
            envir_var=os.environ
            usr_loc=envir_var.get('USERPROFILE')
            loc=usr_loc+"\Downloads\\transcript.txt"
            with open(loc, 'w') as file:
                file.write(result)
                
                
                
st.write('For Arabic')
audi=st.file_uploader("Upload Your Audio File", type=['mp3', 'wav'])
if audi:
    st.audio(audi)
    audio_segment=AudioSegment.from_file(audi)
    chunks=silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS-20, keep_silence=100)
    for index,chunk in enumerate(chunks):
        chunk.export(str(index)+".wav", format="wav")
        with sr.AudioFile(str(index)+".wav") as source:
            recorded=recog.record(source)
            try:
                text=recog.recognize_google(recorded)
                final_result=final_result+" "+text
                print(text)
            except:
                print("None")
                final_result=final_result+" Unaudible"
    with st.form("Result"): 
        result=st.text_area("TEXT", value=final_result) 
        d_btn=st.form_submit_button("Download")    
        if d_btn:
            envir_var=os.environ
            usr_loc=envir_var.get('USERPROFILE')
            loc=usr_loc+"\Downloads\\transcript.txt"
            with open(loc, 'w') as file:
                file.write(result)