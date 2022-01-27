from numpy.lib.polynomial import _binary_op_dispatcher
import streamlit as st
import os
from PIL import Image
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import altair as alt
from sklearn.cluster import DBSCAN
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import re
import base64
import matplotlib.pyplot as plt

from file_selector import *

result_file_selector = file_selector()
#df_range= pd.read_csv(result_file_selector[3])

df = pd.read_csv(result_file_selector[3])
selected_cols = ['Condition (Main Code)', 
                                   'Code Type',
                                   'Severity (Quantification)',
                                   'PositionTo (Longitudinal Distance)',
                                   'Circumferential location, Position From',
                                   'Circumferential location, Position To',
                                   'PhotoNumber (Photograph Reference)',
                                   'frame_index', 'Score'
                                    ]
df= df[selected_cols]

def main():
      menu=['inspection', 'analysis']
      choice = st.sidebar.selectbox("Inspecta AI", menu)
      if choice == 'inspection':
            st.title("Inspecta - GHD.AI")
            st.markdown("## Sewer Video Analytics Model")
            #result_file_selector = file_selector()
            
            #st.write('You selected `%s`' % result_file_selector[0])
            st.markdown("### Raw Footage of Sewer Inspection")
            st.text("\n")
            st.text(result_file_selector[1])
            
    
            vid_file = open(result_file_selector[0], "rb").read()
            st.video(vid_file)
            st.text("\n")
            
            
            if st.checkbox('Apply Inspecta Trained model for inference/detection'):
                  st.markdown("### Deep Learning Algorithm Detecting Defect Types")
                  st.success('Video footage with detection from Inspecta AI Model')
                  st.text("\n")
                  vid_file_U = open( result_file_selector[2], "rb").read()
                  st.video(vid_file_U)
    
                  dfw = pd.read_csv(result_file_selector[3])
                
    
                
                  
                  if st.checkbox('Click to See detection details'):
                        st.subheader('Detection Details')
                        st.dataframe(df)
                        csv = df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
                        st.markdown(href, unsafe_allow_html=True) 
 
                 
 
                  cbar= alt.Chart(df).mark_bar().encode(
                  x='count():Q',
                  y='Condition (Main Code)',
                  color='Condition (Main Code)',
                  tooltip=[ 'Condition (Main Code)']
                   )
    
                  double_chart = cbar + cbar.mark_text(dx=10).encode(text='count()')
    
                  st.altair_chart(double_chart, use_container_width=True)
                  st.markdown("### Defects by Location")
                  
                  domain = ['L', 'M', 'S', 'Ignore']
                  range_ = ['red', 'orange', 'blue', 'gray']
    
                  c =alt.Chart(df).mark_point().encode(
                  x='PositionTo (Longitudinal Distance)',
                  y='Condition (Main Code)',
                  color=alt.Color('Severity (Quantification)', 
                                  scale=alt.Scale(domain=domain, range=range_))
                  )
                  
                       
                  st.altair_chart(c, use_container_width=True)
                  
                  
                             #no_of_frames = len(os.listdir(path + result_file_selector[4]))
                  no_of_frames = 53120
                  detected_frame = len(df['frame_index'])
                  no_of_frames_with_detection = len(pd.unique(df['frame_index']))
        
                  st.info(f'No. of Frames - Original {no_of_frames:,} Vs Frames with Detection {no_of_frames_with_detection:,}' )
                  ratio = no_of_frames_with_detection/no_of_frames
            
                  ratio2 = no_of_frames_with_detection/no_of_frames
            
                  st.success(f'{ratio:.2%} of frames detected with defects')
            
                  st.success(f'Detected defects: {detected_frame}')
                  
                  col1, col2 = st.beta_columns([5, 5])
                  selected_frame = st.select_slider('Select frame with defect(s)', options= df['frame_index'].tolist())
    
                  with col1:
                        
                        or_image_frame = Image.open(HOME_LOCATION  + result_file_selector[5] + '/PCC_SWP002568_080421_PRLC_D_GHD.mpg_converted.mp4_' + str(selected_frame) + '.jpg')
        
                        st.write("Selected Original Frame: ", selected_frame)
                        st.image(or_image_frame, caption='Selected original frame', use_column_width=True)#print(result_file_selector[4])
        
                       
    
                  with col2:
        #st.table(df)
                        image_frame = Image.open(HOME_LOCATION  + result_file_selector[4] + '/mask_PCC_SWP002568_080421_PRLC_D_GHD.mpg_converted.mp4_' + str(selected_frame) + '.jpg')
                        st.write("Selected Defect Detected frame: ", selected_frame)
                        
                        st.image(image_frame, caption='Selected defect detected frame', use_column_width=True)
        
                        
                  dfw1 =dfw.rename(columns={'name': 'defect', 'frame_x':'frame' })
                  selected_cols_2 = ['frame_index', 'Condition (Main Code)', 'Severity (Quantification)', 'PositionTo (Longitudinal Distance)', 'Score']
                  dfw1 = dfw[selected_cols_2]
                  st.table(dfw1.loc[dfw1['frame_index'] == selected_frame])
            
      
      else:
            st.subheader("Analysis")
            #result_file_selector = file_selector()
            #df_range
            def list_to_range(num_list, start, end, segment_length):
                  range_list = [[int(i) - int(i%segment_length), int(i) - int(i%segment_length) + segment_length] for i in num_list]
                  return range_list
            #segment_length = 4  # vary by selection
            st.markdown("### Defects density analysis along distance using score")
            segment_length = st.select_slider('Select Segment Length', options= [1,5,10,15,20])
            st.write("Selected segment length",segment_length)
            position_values = sorted(list(df["PositionTo (Longitudinal Distance)"]))
            from_distance = position_values[0]
            to_distance = position_values[-1]

            df["distance_range"] = list_to_range(list(df["PositionTo (Longitudinal Distance)"]), 
                                         from_distance, to_distance, segment_length)
            
            result = []
            for idx in df.index:
                  result.append("".join(str(df['distance_range'].loc[idx])))

            df['segment'] =  result 
            
            total_score = sum(df['Score'])
            st.info(f'Total Score: {total_score} | Mean Score: {total_score/118:.2}')
          
      
            
            df_final_series = df.groupby(['segment'])['Score'].sum()
            df_final=pd.DataFrame(df_final_series)
            df_final['Segment'] = df_final.index
            df_final.reset_index(inplace=True, drop=True)
            
            
            
            
            df_final.sort_values(by='Score', ascending=False, inplace=True)
            
            cbar_segment= alt.Chart(df_final).mark_bar().encode(
                  x='Score',
                  y='Segment',
                  color='Segment',
                  tooltip=[ 'Score']
                   )
            
            st.altair_chart(cbar_segment, use_container_width=True)
            print(type(df_final))
            st.dataframe(df_final)
            
            selected_segment = st.select_slider('Select Segment', options= df['segment'].tolist())
            st.table(df.loc[df['segment'] == selected_segment])




if __name__ == '__main__':
      main()
