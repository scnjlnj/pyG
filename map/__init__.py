from model import MapManager
import cv2, os, numpy
if __name__ == '__main__':
    mm = MapManager()
    m=mm.init_map(shape=(40,24))
    mm.auto_fill_map(m)
    m.show()
    cv2.waitKey()
    # img1 = cv2.imread(os.path.join("res","wall.png"))
    # # img2 = cv2.imread(os.path.join("res","wood.png"))
    # # img3 = numpy.vstack([numpy.hstack([img2]*10),numpy.hstack([img1]*10)])
    # img3 = numpy.zeros((40,40,3))
    # # img3 = numpy.vstack([img1,img2])
    # # cv2.imshow("img",img1)
    # # cv2.imshow("img2",img2)
    # cv2.imshow("append",img3)
    # cv2.waitKey()
