import cv2
import os
import shutil

#path = 'C:/Users/kwadud/OneDrive - GHD/Client Al-Ain/'

def vid_to_frame(path, width, height):
    
      vidcap = cv2.VideoCapture(path)
      success, image = vidcap.read()
      count = 1
      #print(path)
      
      save_image_dir=path.split("\\")[2].replace(".mp4_converted.mp4", "")
      
      #print(path.split("\\")[2].replace(".mp4_converted.mp4", ""))
      
      os.mkdir(save_image_dir)
      
      src_dir = os.getcwd() 

      # gets the current working dir
      #dest_dir = os.path.join(src_dir, save_image_dir)
      image_save_path = src_dir + "\\" + save_image_dir
      
      #print(image_save_path)
      
      while success:
            
            dim = (width, height)
            resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            
            cv2.imwrite(os.path.join(image_save_path, f"{save_image_dir}_{count}.jpg"), resized)    # save frame as JPEG file
            success,image = vidcap.read()
            #print('Read a new frame: ', success)
            count += 1
           
