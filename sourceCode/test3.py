import cv2
import numpy as np
import colorList
import os
import random

class PhotoStacker:
    def __init__(self,mother_pic_path,child_pics_path):
        self.mother_pic = cv2.imread(mother_pic_path)
        print("load Mother Picture Completed")
        self.sub_colors = []
        self.process_mother_pic()
        print("Process Mother Picture Completed")
        self.child_pics_path = child_pics_path
        self.child_pics = {"black":[],"white":[],"red":[],"gray":[],"orange":[],"yellow":[],"green":[],"cyan":[],"blue":[],"purple":[],"skin":[]}
        print("Start Stack Pictures...")
        self.get_pics(self.child_pics,child_pics_path)

    def get_pics(self,child_pics, pics_path):
        files = os.listdir(pics_path)
        for file in files:
            path = pics_path+"/"+file
            pic = cv2.imread(path)
            size = (100, 100)
            pic = cv2.resize(pic,size,interpolation=cv2.INTER_AREA)
            color = self.get_color(pic)
            child_pics[color].append(pic)

    def resize_pic(self,pic,coiffient):
        height,width = pic.shape[:2]
        size = (int(coiffient*height),int(coiffient*width))
        pic = cv2.resize(pic,size,interpolation=cv2.INTER_AREA)
        return pic

    def get_color(self, frame):
        #print('go in get_color')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maxsum = -100
        color = None
        color_dict = colorList.getColorList()
        for d in color_dict:
            mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
            binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
            binary = cv2.dilate(binary, None, iterations=2)
            img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            sum = 0
            for c in cnts:
                sum += cv2.contourArea(c)
            if sum > maxsum:
                maxsum = sum
                color = d

        return color

    def process_mother_pic(self):
        height,width = self.mother_pic.shape[:2]
        increment = 5
        x1 = 0
        x2 = x1+increment
        y1 = 0
        y2 = y1+increment
        row = 0
        column = 0
        while y2 <= height:
            column = 0
            x1 = 0
            x2 = x1+increment
            row_pic = []
            while x2 <= width:
                sub_pic = self.mother_pic[y1:y2,x1:x2]
                sub_color = self.get_color(sub_pic)
                row_pic.append(sub_color)
                x1 = x2
                x2 += increment
                column += 1
            y1 = y2
            y2 += increment
            row += 1
            self.sub_colors.append(row_pic)
        return None


    def get_pic_from_color(self,color):
        scale = random.random()*(len(self.child_pics[color])-1)
        return self.child_pics[color][int(scale)]


    def stack_pics(self):
        result = 0
        isColumnStart = False
        for index , row in enumerate(self.sub_colors):
            print("stacking picture ..., " + str((index+1)/len(self.sub_colors))[:5])
            row_pics = 0
            isRowStart = False
            for color in row:
                pic = self.get_pic_from_color(color)
                if not isRowStart:
                    row_pics = pic
                    isRowStart = True
                else:
                    row_pics = np.concatenate((row_pics,pic),axis=1)
            if not isColumnStart:
                result = row_pics
                isColumnStart = True
            else:
                result = np.concatenate((result,row_pics))
        return result









if __name__ == "__main__":
    path = "C:\\Users\\XinYuan Chen\\Desktop\\photoStacker\\motherPicture.jpg"
    path1 = "C:\\Users\\XinYuan Chen\\Desktop\\photoStacker\\photo"
    wedding = PhotoStacker(path,path1)
    print("saving result ...")
    cv2.imwrite("wedding.jpg",wedding.stack_pics())



