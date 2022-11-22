import os
import pathlib
from random import randint
import streamlit as st
from uuid import uuid4

class Uploader:
    
    def __init__(self, output_path, callback) -> None:
        self.output_path = output_path
        self.callback = callback
        self.session_key = str(uuid4())
        
    def __upload(self):
        if self.uploaded_files is None:
            st.session_state["uploaded_files"] = "Upload a file first!"
        else:
            upload_path = os.path.join(self.output_path, str(uuid4()))
            os.mkdir(upload_path)
            for uploaded_file in self.uploaded_files:
                data = uploaded_file.getvalue()
                complete_name = os.path.join(upload_path, uploaded_file.name)
                
                destination_file = open(complete_name, "wb+")
                destination_file.write(data)
                destination_file.close()
                
        return upload_path                
                
    def ui(self):
        with st.form("my-form", clear_on_submit=True):
            self.uploaded_files = st.file_uploader(label="Add new File", accept_multiple_files=True)
            #st.button("Upload file to Sandbox", on_click=self.__upload)
            submitted = st.form_submit_button("UPLOAD!")
            if submitted:
                upload_path = self.__upload()            
                self.callback(upload_path)