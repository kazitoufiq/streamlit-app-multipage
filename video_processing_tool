import streamlit as st
import os
import pandas as pd
import video_meta_data as meta
import frame_reduction as fr
import video_to_frame as vtf
from PIL import Image
import time
import mimetypes
import cv2

path = ".\media"

def main():

    st.title("Video Preprocessing Tool for Computer Vision")
    image_file = st.file_uploader("Upload Video File")  # , type=['png','jpeg','jpg', 'mp4']
    
    if image_file is not None:
        file_details = {"FileName":image_file.name,"FileType":image_file.type}
        st.write(file_details)
        
        #img = load_image(image_file)
        #st.image(img)
        with open(os.path.join("media",image_file.name),"wb") as f: 
            f.write(image_file.getbuffer())         
        st.success("Saved File") 
    
    result_file_selector = file_selector()
    
    
    if mimetypes.guess_type(result_file_selector[1])[0].startswith('video'):
        vid_file = open(result_file_selector[0], "rb").read()
        st.video(vid_file)
        st.text(result_file_selector[0])
        analysis = meta.video_mata_data(result_file_selector[0])
        meta_table = pd.DataFrame.from_dict(analysis,  orient='index')
        st.info("Video Matadata of original video")
        st.table(meta_table)
        
    else:
         pass
         #image_file = open(result_file_selector[0], "rb").read()
         #st.image(image_file)
         
     
    if st.checkbox('Go ahead with conversion?'):
        
        options = list(range(2,11))
        frame_selection= st.selectbox('Every n-th frame to be selected:', options ) 
        st.write('You selected:', frame_selection)
        
        agree= st.checkbox('Run Conversion')
        if agree:
            with st.spinner('Wait for the conversion...'):
                fr.fn_frame_reduction(path+ "\\" + result_file_selector[1], frame_selection)
                st.code('Conversion done with selection of every ' + str(frame_selection) + ' frame of the orginal video' )
                processed_file=path+ "\\" + result_file_selector[1] + '_converted' + ".mp4"
                vid_file = open(processed_file, "rb").read()
                st.video(vid_file)
                analysis = meta.video_mata_data(processed_file)
                meta_table = pd.DataFrame.from_dict(analysis,  orient='index')
                st.info("Video Metadata after processing")
                st.table(meta_table)
        
        
        extract_to_image= st.checkbox('Extract to Frames?')
        if extract_to_image:
            
            col1, col2 = st.beta_columns([5, 5])
            with col1:
                width_selection= st.text_input('Select Width:', 416 ) 
            with col2:    
                height_selection= st.text_input('Select Height:', 416 ) 
           
            st.write('Selected: Width ', width_selection, 'and Height ', height_selection )
            
            proceed= st.checkbox('Confirm to proceed?')
            
            if proceed:
            
                with st.spinner('Wait for extraction of frames...'):
                   vtf.vid_to_frame(processed_file, int(width_selection), int(height_selection) )
            
            st.text("Conversion to frames completed!")
                

def file_selector(folder_path=path):

    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox("Select Video file", filenames) #select file with st select box
    return os.path.join(folder_path, selected_filename), selected_filename


def load_image(image_file):
	img = Image.open(image_file)
	return img 



if __name__ == "__main__":
    main()
