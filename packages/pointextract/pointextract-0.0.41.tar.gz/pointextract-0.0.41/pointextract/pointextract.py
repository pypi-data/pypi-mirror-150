#import and function
#import and function
from time import sleep
import os,cv2,time # type: ignore  
import seaborn as sns  # type: ignore
from skimage.measure import block_reduce  # type: ignore
import plotly.graph_objects as go  # type: ignore
import numpy as np
import matplotlib.image as mpimg
from tqdm import trange, tqdm
import open3d as o3d
from matplotlib.image import imread
from mpl_toolkits import mplot3d
from matplotlib.pyplot import figure
import random
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.image import imread
import matplotlib.cm as cm
from PIL import Image, ImageStat
import shutil

OUTPUT_FOLDER_2DIMG = None
OUTPUT_FOLDER_3DIMG = None

def build_on_each_folder(folder_path, THRESAHOLDED_BOX_NUMBER, BACKGROUND_NUMBER, downsampletimes=0):
    #Aply read_singlefolder_process_to_png() here
    lst = os.listdir(folder_path)
    #lst=sorted(lst, key=lambda x : int(os.path.splitext(x)[0]))
    lst = sorted(lst)
    arrays3D_list = []
    for file in lst:
        full_path = os.path.join(folder_path, file)
        if os.path.isdir(full_path):
            print('working on:', full_path)
            read_singlefolder_process_to_png(
                full_path, THRESAHOLDED_BOX_NUMBER, BACKGROUND_NUMBER, outputname='AUTO')


def read_singlefolder_process_to_png(in_folder_path, THRESAHOLDED_BOX_NUMBER, BACKGROUND_NUMBER, outputname):
    if outputname == 'AUTO':
        newfoldername = in_folder_path.replace('/', '_')
    else:
        newfoldername = outputname
    global OUTPUT_FOLDER_2DIMG
    if "/" != OUTPUT_FOLDER_2DIMG[-1]:
        OUTPUT_FOLDER_2DIMG = OUTPUT_FOLDER_2DIMG+'/'
    if not os.path.exists(newfoldername):
        os.makedirs(OUTPUT_FOLDER_2DIMG+newfoldername)
        print('Creating folder:', OUTPUT_FOLDER_2DIMG+newfoldername)
    lst = os.listdir(in_folder_path)
    lst = sorted(lst)
    final_x = 999999
    final_y = 999999
    final_hplusy = -99999
    final_wplusx = -99999
    print('Applying THRESAHOLDED_BOX_NUMBER')
    for i in tqdm(lst, ncols=80):
        if i.endswith(".tiff") or i.endswith(".png"):
            add = str(in_folder_path)+"/"+str(i)
            img = cv2.imread(add, cv2.IMREAD_GRAYSCALE)
            #print(img.shape)
            _, thresholded = cv2.threshold(
                img, THRESAHOLDED_BOX_NUMBER, 255, cv2.THRESH_BINARY)
            #cv2.imwrite("1thresholded.jpg", thresholded)
            bbox = cv2.boundingRect(thresholded)
            x, y, w, h = bbox
            #print(bbox)
            if x != 0:
                if x < final_x:
                    final_x = x
                if y < final_y:
                    final_y = y
                if y+h > final_hplusy:
                    final_hplusy = y+h
                if x+w > final_wplusx:
                    final_wplusx = x+w
    print('final box size:', final_x, final_y, final_wplusx, final_hplusy)
    print('Applying BACKGROUND_NUMBER')
    counter = 1
    for i in tqdm(lst, ncols=80):
        if i.endswith(".tiff") or i.endswith(".png"):
            add = str(in_folder_path)+"/"+str(i)
            img = cv2.imread(add, cv2.IMREAD_GRAYSCALE)
            ###DONOT FLIP FOR TIFF IMAGE!###
            #img = cv2.flip(img, 1 )
            #foreground = img[final_y:final_hplusy, final_x:final_wplusx]
            #####DO DOWNSAMPLE HERE!!!!#######
            #for j in range(0,downsampletimes):
            # img = cv2.pyrDown(img)
            foreground = img
            foreground[foreground < BACKGROUND_NUMBER] = 0
            finalName = OUTPUT_FOLDER_2DIMG + \
                newfoldername+'/'+str(counter)+".png"
            #print('finalName:',finalName)
            cv2.imwrite(finalName, foreground)
            counter = counter+1
    print('done')


def build_3dpointArray_on_SingleFolder(folder_path, downsample_size=1, heightrate=1):
    #apply read_All_image_in_Folder()->extract_pixel()
    #lst = os.listdir(folder_path)
    #lst=sorted(lst, key=lambda x : int(os.path.splitext(x)[0]))
    in_funtime = time.time()
    #for file in lst:
    #if file != '.ipynb_checkpoints' :
    #full_path = os.path.join(folder_path, file)
    full_path = folder_path
    print('Working on:', full_path)
    print('Start extracting pixels',  time.time()-in_funtime)
    nppoints, npcolor = read_All_image_in_Folder(full_path, heightrate)
    print('Convert to numpy',  time.time()-in_funtime)
    finalshape = 0
    for i in nppoints:
        finalshape = finalshape+i.shape[0]
    fill_loc = np.zeros(finalshape*3)
    pointer = 0
    for i in tqdm(nppoints, ncols=80):
        for j in i.flatten():
            fill_loc[pointer] = j
            pointer = pointer+1

    nppoints = fill_loc.reshape(finalshape, 3)

    fill_col = np.zeros(finalshape*3)
    pointer = 0
    for i in tqdm(npcolor, ncols=80):
        for j in i.flatten():
            fill_col[pointer] = j
            pointer = pointer+1

    npcolor = fill_col.reshape(finalshape, 3)
    return nppoints, npcolor


def array_saveto_pcd(nppoints, npcolor, name):
    in_funtime = time.time()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(nppoints)
    pcd.colors = o3d.utility.Vector3dVector(npcolor)
    print('Saving',  time.time()-in_funtime)
    o3d.io.write_point_cloud(OUTPUT_FOLDER_3DIMG+str(name)+".pcd", pcd)
    print('END',  time.time()-in_funtime)

    '''
            with open('/home/lxh442/CodeWorkSpace/MDLE-B/output.txt', 'w') as f:
                f.write(str(nppoints.shape)+str(npcolor.shape))
            #nppoints=np.array(points)
            #npcolor=np.array(color_of_points)
            print('Final point shape:',nppoints.shape)
            print('Convert to o3d',  time.time()-in_funtime)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(nppoints)
            pcd.colors = o3d.utility.Vector3dVector(npcolor)
            print('Saving',  time.time()-in_funtime)
            down_pcd = pcd.voxel_down_sample(downsample_size)
            del pcd
            o3d.io.write_point_cloud(OUTPUT_FOLDER_3DIMG+str(file)+".pcd", down_pcd)
            print('END',  time.time()-in_funtime)
    '''


def read_All_image_in_Folder(in_folder_path, heightrate):
    #apply extract_pixel() on all images inlst=sorted(lst, key=lambda x : int(os.path.splitext(x)[0]))ONE folder
    lst = os.listdir(in_folder_path)
    if '.ipynb_checkpoints' in lst:
        lst.remove('.ipynb_checkpoints')
    lst = sorted(lst, key=lambda x: int(os.path.splitext(x)[0]))
    order = 1
    if heightrate != 1:
        lst = lst[0:int(len(lst)*heightrate)]
    #get current time in seconds
    start_time = time.time()
    #!!!!MAY have layer[] here!!!!
    lst = lst
    list_col = []
    list_loc = []
    for file in lst:
        if file.endswith(".png"):
            fullfile = in_folder_path+'/'+file
            #print('image loc',fullfile)
            location, color = extract_pixel(fullfile, order)
            #print(location)
            list_loc.append(location)
            list_col.append(color)
            #location_list = np.vstack([location_list,location])
            #color_list = np.vstack([color_list,color])
            del location, color
            usedtime = round(time.time()-start_time, 1)
            totaltime = round((time.time()-start_time)/order*len(lst), 1)
            remaintime = round(totaltime-usedtime, 1)
            print('working on layer: ', order, 'Used time:', usedtime,
                  'Reamin time:', remaintime, 'Total time', totaltime, end='\r')
            order = order+1
    #return list_loc,list_col
    #print('start concatenate time,',int(time.time()-start_time))
    #location_list=np.concatenate(list_loc)
    #color_list=np.concatenate(list_col)
    #print('location_list',location_list.shape,color_list.shape)
    #print('end concatenate time,',int(time.time()-start_time))
    print('Extract all pixel on all images!')
    return list_loc, list_col


def extract_pixel(file_name, order):
    ##update##
    #img = imread(file_name)
    #print(img.shape)
    Limg = Image.open(file_name).convert('L')
    img = np.asarray(Limg)
    label_x = np.array(list(range(0, img.shape[1])))
    label_y = np.array(list(range(0, img.shape[0])))
    X, Y = np.meshgrid(label_x, label_y)
    points_xyzrgb = np.column_stack(
        (Y.ravel(), X.ravel(), img.ravel(), img.ravel(), img.ravel()))
    points_xyzrgb = pd.DataFrame(points_xyzrgb, columns=[
                                 'x', 'y', 'r', 'g', 'b'])
    points_xyzrgb['z'] = order
    points_xyzrgb = points_xyzrgb[points_xyzrgb['r'] != 0]
    points_xyz = points_xyzrgb[['x', 'y', 'z']]
    points_rgb = points_xyzrgb[['r', 'g', 'b']]
    #convert to array
    points_xyz = points_xyz.values
    points_rgb = points_rgb.values
    points_rgb = points_rgb/255.0
    #sort by x
    #points_xyz=points_xyz[points_xyz[:,0].argsort()]
    #del points_xyzrgb,points_xyz,points_rgb
    return points_xyz, points_rgb

#testadd='/home/lxh442/mdle/B-cots/Reconstructed data/2108NoellSandia-XCT-Data/As-ReceivedParts/169_TVS_Samp01a07_060321_01_4x_B2_1s_LE5_80k10W_2p8um_recon'
#read_singlefolder_process_to_png(testadd,30,30)


def extractpoints_from2D_build3Dobj(input_folder, output_name, downsample_rate=1, height_rate=1):
    loc, color = build_3dpointArray_on_SingleFolder(
        input_folder, downsample_size=downsample_rate, heightrate=height_rate)
    array_saveto_pcd(loc, color, output_name)


def set_folder_location(set_2dimg_folder, set_3dobj_folder):
    global OUTPUT_FOLDER_2DIMG
    global OUTPUT_FOLDER_3DIMG
    OUTPUT_FOLDER_2DIMG = set_2dimg_folder
    OUTPUT_FOLDER_3DIMG = set_3dobj_folder


def display_folder_location():
    print('2D image folder location:', OUTPUT_FOLDER_2DIMG)
    print('3D object folder location:', OUTPUT_FOLDER_3DIMG)


def build_circle(r, num_points):
    t = np.linspace(0, 2*np.pi, num_points)
    x = np.cos(t)*r
    y = np.sin(t)*r
    x = x.astype(int)
    y = y.astype(int)
    return x, y


def adjustFigAspect(fig, aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize, ysize = fig.get_size_inches()
    minsize = min(xsize, ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)


def unwarp_All_image_in_Folder(in_folder_path, given_name):
    #apply extract_pixel() on all images in ONE folder
    lst = os.listdir(in_folder_path)
    if '.ipynb_checkpoints' in lst:
        lst.remove('.ipynb_checkpoints')
    #lst=sorted(lst, key=lambda x : int(os.path.splitext(x)[0]))
    lst = sorted(lst)
    order = 1
    #get current time in seconds
    start_time = time.time()
    for file in lst:
        if file.endswith(".tiff") or file.endswith(".png") or file.endswith(".tif"):
            fullfile = in_folder_path+'/'+file
            #print('image loc',fullfile)
            finalfolder = OUTPUT_FOLDER_2DIMG+'/'+given_name
            isExist = os.path.exists(finalfolder)
            if not isExist:
                os.makedirs(finalfolder)
            finalFile = finalfolder+'/'+str(file)
            #print('save to',finalFile)
            img = cv2.imread(fullfile, cv2.IMREAD_GRAYSCALE)
            gray_image = img
            ret, thresh = cv2.threshold(gray_image, 90, 255, 0)
            M = cv2.moments(thresh)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 5, (130, 255, 255), -1)
            #print('center',cX,cY)
            unwarpSingleImage(fullfile, cX, cY, 200, 400,
                              int(math.pi*300), finalFile)
            usedtime = round(time.time()-start_time, 1)
            totaltime = round((time.time()-start_time)/order*len(lst), 1)
            remaintime = round(totaltime-usedtime, 1)
            print('working on layer: ', order, 'Used time:', usedtime,
                  'Reamin time:', remaintime, 'Total time', totaltime, end='\r')
            order = order+1
    print('Extract all pixel on all images!')


def detectCenter(inFile, outName):
    img = cv2.imread(inFile, cv2.IMREAD_GRAYSCALE)
    gray_image = img
    ret, thresh = cv2.threshold(gray_image, 90, 255, 0)
    M = cv2.moments(thresh)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(img, (cX, cY), 5, (130, 255, 255), -1)
    print('center', cX, cY)
    #print('for fun x y is',img.shape[1]-cX,img.shape[0]-cY)
    plt.imsave(outName, thresh, cmap=cm.gray, vmin=0, vmax=255)


def selectPointOnCircle(center, xperpoints, yperpoints):
    points_on_circle = []
    for i in range(len(xperpoints)):
        points_on_circle.append(
            [int(center[0]+xperpoints[i]), int(center[1]+yperpoints[i])])
        #print(center[0],center[1],xperpoints[i],yperpoints[i])
    return points_on_circle


def unwarpSingleImage(infile_name, centerX, centerY, lowestR, highestR, pointsNumber, outputname):
    img = imread(infile_name)
    import math

    def unwarp_one_circle_to_one_line(r, points, center, inArray):
        a, b = build_circle(r, points)

        def selectPointOnCircle(center, xperpoints, yperpoints):
            points_on_circle = []
            for i in range(len(xperpoints)):
                points_on_circle.append(
                    [int(center[0]+xperpoints[i]), int(center[1]+yperpoints[i])])
                #print(center[0],center[1],xperpoints[i],yperpoints[i])
            return points_on_circle
        Points_on_Circle = selectPointOnCircle(center, a, b)

        def findPointsOnRealImage(points_xy: list, inArray: np.ndarray):
            allPoints = []
            for i in points_xy:
                allPoints.append(inArray[i[1]][i[0]])
            return np.asarray(allPoints)

        array_circle = findPointsOnRealImage(Points_on_Circle, inArray)

        def rePlacePixels(inArray):
            return np.asarray(inArray.r.values.tolist())

        #aline_pixels=rePlacePixels(array_circle)

        return array_circle
        #print(aline_pixels)

    def batch_unwarp(lowestR, highestR, points, center, inArray):
        finalArray = unwarp_one_circle_to_one_line(
            lowestR, points, center, inArray)
        for i in range(lowestR+1, highestR):
            thisline = unwarp_one_circle_to_one_line(
                i, points, center, inArray)
            finalArray = np.vstack([thisline, finalArray])
        return finalArray

    centerPoint = [centerX, centerY]
    #arraytoImage=batch_unwarp(200,400,int(math.pi*(400-200)),centerPoint,points_xyzrgb)
    arraytoImage = batch_unwarp(
        lowestR, highestR, pointsNumber, centerPoint, img)
    #plt.imsave(outputname, arraytoImage,cmap=cm.gray, vmin=0, vmax=255)
    plt.imsave(outputname, arraytoImage, cmap=cm.gray)
    return
