import imageio
import os

def fn_frame_reduction(filepath, n_frame ): 
      reader = imageio.get_reader(filepath)
      outputpath = filepath + '_converted' + ".mp4"

      fps = reader.get_meta_data()['fps']
      #print(fps)

      writer = imageio.get_writer(outputpath, fps=fps)
      c=1
      for frames in reader:
            if c%int(n_frame)==0:
                  writer.append_data(frames)
                  #print(f'Frame {frames}')
            c+=1
      #print("\nYOUR WORK IS DONE !!!")
      #os.startfile(outputpath)
      writer.close()
      
#fn_frame_reduction('.\media\short.mp4')
