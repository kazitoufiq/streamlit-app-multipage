import os
import streamlit as st

HOME_LOCATION='C:/Users/kwadud/OneDrive - GHD/WellingtonWaterDemo2/' 

def file_selector(folder_path=HOME_LOCATION):
    filenames = os.listdir(folder_path)
    
    vid_files =  list(filter(lambda x: '.mp4' in x, filenames))
    
    selected_filename = st.selectbox('Select a raw video footage', vid_files)
    csv_file = selected_filename.replace('.mp4', '.csv')
    
    infer_video = selected_filename.replace('.mp4', '_Infer.mp4') 
    
    image_folder = selected_filename.replace('.mp4', '_Frame')
    
    original_image_folder = selected_filename.replace('.mp4', '_Original')
    
    range_csv = selected_filename.replace('.mp4', '_Range.csv')
     
  
    return os.path.join(folder_path, selected_filename), selected_filename, os.path.join(folder_path, infer_video) , os.path.join(folder_path, csv_file), image_folder, original_image_folder, os.path.join(folder_path, range_csv)
