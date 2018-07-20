import cv2
import numpy as np
import os
import argparse
import logging

class Finder:

    def __init__(self, templates_path,images_path,output,coor_path):

        self.result={}
        self.templates=self.load_temp(templates_path)
        self.images=self.load_img(images_path)
        self.compare_dir(self.images,self.templates)
        self.plot_images(output)
        with open(coor_path+'/coordinates.list','w') as f:
            f.write(str(self.result))




    #def func(self):



    def compare_dir(self,images,templates):

        res={}
        for ipath in images:
            res[ipath]={}
            for tkey in templates:
                loc,w,h=self.compare(templates[tkey],ipath)
                coor=self.loc2coordinates(loc,w,h)
                res[ipath][tkey]=coor


        self.result=res


    def compare(self,template,image,threshold = 0.9):
        img_rgb = cv2.imread(image)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        return loc,w,h

    def loc2coordinates(self,loc,w,h):
        coor=[]
        for pt in zip(*loc[::-1]):
            coor.append((pt, (pt[0] + w, pt[1] + h)))
        return coor


    def load_img(self,directory):

            lst=[]
            for di in [directory]:
                #res=[]
                for file in os.listdir(di):
                    #res.append(cv2.imread(di+file,cv2.IMREAD_GRAYSCALE))
                    lst.append(di+"/"+file)

            return lst




    def load_temp(self,directory):

        dic={}
        for di in [directory]:
            #res=[]
            for file in os.listdir(di):
                #res.append(cv2.imread(di+file,cv2.IMREAD_GRAYSCALE))
                dic[file]=cv2.imread(di+'/'+file,0)

        return dic

    def plot_images(self,detected_path):
        if not os.path.exists(detected_path):
            os.makedirs(detected_path)
            print('folder created')

        for ipath in self.images:
            img_rgb = cv2.imread(ipath)
            for tkey in self.result[ipath]:
                if self.result[ipath][tkey]!=[]:
                    for xy in self.result[ipath][tkey]:
                        cv2.rectangle(img_rgb, xy[0],xy[1] , (0,255,255), 2)
            cv2.imwrite(detected_path+'/'+ipath.split('/')[2],img_rgb)


    #def get_objects(self, img):

def main():



    finder=Finder(templates_path="static/temp",
                images_path="static/img",
                  output="static/detected",
                  coor_path="static")

    #finder.func()
