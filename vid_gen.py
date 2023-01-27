import cv2
import sys
import os
import numpy as np
import glob

def img_gen_main():
    files = glob.glob('*.jpg')
    files = sorted(files)
    imgs = []
    for file_ in files:
        imgs.append(cv2.imread(file_))
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    out = cv2.VideoWriter('heat.avi', fourcc, 10, (imgs[0].shape[1],imgs[0].shape[0]))
    for img in imgs:
        for x in range(10):
            vid_gen_main(img, out)
    cv2.destroyAllWindows()
    out.release()

def vid_gen_main(frame, out):
#    vid_im = nd_arr_transform(frame)
   out.write(frame)

if __name__ == '__main__':
    img_gen_main()