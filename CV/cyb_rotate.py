import cv2
import numpy as np

def cw_rotate_crop(img, angle):
    '''
    顺时针旋转angle度，自动裁剪，不留存黑边
    '''
    imgH, imgW = img.shape[:2]
    if angle % 90 == 0:
        rotation_mat = cv2.getRotationMatrix2D((imgW/2, imgH/2), angle, 1.)
        return cv2.warpAffine(img, rotation_mat, (imgW, imgH))

    P = np.array([[0, 0, 1],
                 [imgW, 0, 1],
                 [imgW, imgH, 1],
                 [0, imgH, 1]])
    rotation_mat = cv2.getRotationMatrix2D((imgW/2, imgH/2), angle, 1.)
    RP = np.dot(rotation_mat, P.T).T
    p1, p2, p3, p4 = RP[:]
    x1, y1 =  p1[:]
    x2, y2 =  p2[:]
    x3, y3 =  p3[:]
    x4, y4 =  p4[:]
    angle = angle % 360
    x0, y0 = imgW / 2, imgH / 2
    if 0 <= angle < 90 or 180 <= angle < 270:
        yy1 = (y1 - y0) / (x1 - x0) * (0 - x0) + y0
        xx2 = (x2 - x0) / (y2 - y0) * (0 - y0) + x0
        yy3 = (y3 - y0) / (x3 - x0) * (imgW - x0) + y0
        xx4 = (x4 - x0) / (y4 - y0) * (imgH - y0) + x0
        src = [[0, yy1], [xx2,  0], [imgW, yy3], [xx4, imgH]]
    if 90 <=angle < 180 or 270 <= angle < 360:
        xx1 = (x1 - x0) / (y1 - y0) * (0 - y0) + x0
        yy2 = (y2 - y0) / (x2 - x0) * (imgW - x0) + y0
        xx3 = (x3 - x0) / (y3 - y0) * (imgH - y0) + x0
        yy4 = (y4 - y0) / (x4 - x0) * (0 - x0) + y0
        src = [[xx1, 0], [imgW,  yy2], [xx3, imgH], [0, yy4]]

    #xx1 = (x2 - x1)/(y2 - y1)*(0 - y1) + x1 # y1 = 0
    #yy2 = (y1 - y4)/(x1 - x4)*(0 - x1) + y1 # x1 = 0
    #xx3 = (x3 - x4)/(y3 - y4)*(imgH - y4) + x4 # y1 = imgH
    #yy4 = (y3 - y2)/(x3 - x2)*(imgW - x2) + y2 # x1 = imgW
    #src = [[xx1, 0], [0, yy2], [xx3, imgH], [imgW, yy4]]

    dst = [[0, 0], [imgW, 0], [imgW, imgH], [0, imgH]]
    M = cv2.getPerspectiveTransform(np.array(src[:], dtype=np.float32), np.array(dst[:], dtype=np.float32))
    d_mat = cv2.warpPerspective(img, M, (imgW, imgH))
    return d_mat

def keep_size_rotate(img, angle):
    '''
    保持原图大小resize
    '''
    pass

def rotate(img, angle, type=0):
    '''
    type: 0,1,2
    0: opencv_rotate,
    1: keep_size,
    2: cw_rotate_crop,
    '''
    if type==0:
        return img
    if type==1:
        return keep_size_rotate(img, angle)
    if type==2:
        return cw_rotate_crop(img, angle)
