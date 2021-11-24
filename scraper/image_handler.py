import os
from math import ceil
import numpy as np
import cv2

def align_center(img,back_width):
    h,w,_=img.shape
    back = np.zeros((h,back_width,3),np.uint8)
    if w>back_width:
        border = (w - back_width) // 2
        back = img[0:h,border:border+back_width]
    else:
        border = (back_width-w)//2
        back[0:h,border:border+w] = img
    return back
def read_image(path) -> np.ndarray:
    return cv2.imdecode(np.fromfile(path,dtype=np.uint8),-1)
def shwo_img(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def get_cut_width(imgs):
    widths = [i.shape[1] for i in imgs]
    temp = {}
    for i in widths:
        if i in temp:
            temp[i] += 1
        else:
            temp[i] = 0
    ww = 0
    cnt = 0
    for i in temp:
        if cnt > temp[i]:
            continue
        elif cnt == temp[i]:
            ww = max(ww, i)
        else:
            ww = i
            cnt = temp[i]
    return ww+ceil(ww/90)*10

def concat_imgs_by_index(dir_path,out="combination"):
    files = os.listdir(dir_path)
    files.sort(key=lambda x:int(x.split(".",1)[0]))
    ret = None
    imgs = [read_image(os.path.join(dir_path,p)) for p in files]
    cut_width = get_cut_width(imgs)
    for img in imgs:
        img = align_center(img,cut_width)
        if ret is not None:
            ret = np.vstack((ret,img))
        else:
            ret = img
    chapter_name = os.path.basename(dir_path)
    cv2.imencode(".png",ret)[1].tofile(os.path.join(os.path.dirname(dir_path),chapter_name+"_"+out))
    # Image.fromarray(ret).save(os.path.join(os.path.dirname(dir_path),chapter_name+"_"+out))


if __name__ == '__main__':
    dir_path = os.path.join("datas", "Skeleton_Soldier_Couldn’t_Protect_the_Dungeon")
    for n in os.listdir(dir_path):
        print(n, os.path.isdir(os.path.join(dir_path, n)))
    # dir_path = os.path.join("datas","Skeleton_Soldier_Couldn’t_Protect_the_Dungeon","Chapter_3")
    # out = "combination.png"
    # concat_imgs_by_index(dir_path)
