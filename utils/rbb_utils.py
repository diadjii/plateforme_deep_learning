#Common functions to work with rotationnal bounding boxes.

import os
import cv2
import math
import itertools
import numpy as np
import skimage.draw
from mrcnn.utils import extract_bboxes

##############################
# Rotations anchors proposals
##############################
#
# def get_rbb_propositions(mask,bbox):
#     y = (bbox[0]+bbox[2])/2
#     x = (bbox[1]+bbox[3])/2
#     h = bbox[2]-bbox[0]
#     w = bbox[3]-bbox[1]
#     angles = np.linspace(0,(np.pi), 10)
#     v = [[(math.cos(i),math.sin(i)),(-math.sin(i),math.cos(i))] for i in angles]
#     d = [w/2,h/2]
#     rbb_propositions = []
#     for i in range(10):
#         d1 = [d[0]*a for a in v[i][0]]
#         d2 = [d[1]*a for a in v[i][1]]
#         p1=(int(x+d1[0]+d2[0]),int(y+d1[1]+d2[1]))
#         p2 = (int(x-d1[0]+d2[0]), int(y-d1[1]+d2[1]))
#         p3 = (int(x-d1[0]-d2[0]), int(y-d1[1]-d2[1]))
#         p4 = (int(x+d1[0]-d2[0]), int(y+d1[1]-d2[1]))
#         rbb_propositions.append([p1,p2,p3,p4])
#     return [int(x),int(y)],rbb_propositions

############################
# Other utils
###########################
def extract_points(bbox):
    #horizontal bboxes is a vector of 4 integers
    # let's find the corresponding points of its angles
    pts=[]
    pts.append((bbox[1],bbox[0]))
    pts.append((bbox[1],bbox[2]))
    pts.append((bbox[3],bbox[2]))
    pts.append((bbox[3],bbox[0]))
    return(pts)
############################
# Display RBB
###########################
def display_rbbs(rbb,image,DISPLAY=False):
    for i,elem in enumerate(rbb):
        pts = rbb[i]
        display_rbb(pts,image)
    if DISPLAY==True:
        cv2.imshow("Output",image)
        cv2.waitKey()

def display_rbb(rbb,image):
    cv2.line(image,rbb[0],rbb[1],(255,0,0),2)
    cv2.line(image,rbb[1],rbb[2],(255,0,0),2)
    cv2.line(image,rbb[2],rbb[3],(255,0,0),2)
    cv2.line(image,rbb[3],rbb[0],(255,0,0),2)

##############################
# Get RBB
##############################

def get_rbb(center,size,angle):
    x,y=center
    w,h=size
    v = [(math.cos(angle),math.sin(angle)),(-math.sin(angle),math.cos(angle))]
    d = [w/2,h/2]
    d1 = [d[0]*a for a in v[0]]
    d2 = [d[1]*a for a in v[1]]
    p1=(int(x+d1[0]+d2[0]),int(y+d1[1]+d2[1]))
    p2 = (int(x-d1[0]+d2[0]), int(y-d1[1]+d2[1]))
    p3 = (int(x-d1[0]-d2[0]), int(y-d1[1]-d2[1]))
    p4 = (int(x+d1[0]-d2[0]), int(y+d1[1]-d2[1]))
    rbb_propositions =[p1,p2,p3,p4]
    return rbb_propositions

def get_min_area_rect(mask):
    non_zeros = cv2.findNonZero(mask)
    center,size,angle = cv2.minAreaRect(non_zeros)
    rbb_pts=get_rbb(center,size,angle/180*math.pi)
    return rbb_pts,tuple(int(a) for a in center)

##############################
# Compare RBB
##############################
def get_useful_info(mask,bbox):
    #Let's first build the max corresponding to the bounding box
    bbox_mask = np.zeros([mask.shape[0],mask.shape[1]],dtype=np.uint8)
    bbox = np.array(bbox)
    x,y = skimage.draw.polygon(bbox[:,1],bbox[:,0])
    out_indices = [i for i,a in enumerate(x) if (a>=mask.shape[0] or a<0 or y[i]>=mask.shape[1] or y[i]<0 )]
    for i in range(0,len(x)):
        if i not in out_indices:
            bbox_mask[x[i],y[i]]=1
    # As all the points from the original mask are contained in the bbox mask, all we have left to do is
    # to compare them in terms of size
    mask_count = len(np.where(mask==1)[0])
    bbox_mask_count = len(np.where(bbox_mask==1)[0])+len(out_indices) #we need to count the indices out of the image
    useful_info = mask_count/bbox_mask_count
    # print('[DEBUG]         mask size : {}'.format(mask_count))
    # print('[DEBUG]    bbox mask size : {}'.format(bbox_mask_count))
    # print('[DEBUG]             len x : {}'.format(len(x)))

    return(useful_info)

def get_intersection_info(bboxes,width,height):
    map = np.zeros([width,height,len(bboxes)],dtype=np.uint8)
    mask_size = np.zeros([len(bboxes)],dtype=np.uint32)
    for j,bbox in enumerate(bboxes):
        mask_size_tmp=0
        bbox = np.array(bbox)
        x,y = skimage.draw.polygon(bbox[:,1],bbox[:,0])
        out_indices = [i for i,a in enumerate(x) if (a>=width or a < 0 or y[i]>=height or y[i] <0)]
        for i in range(0,len(x)):
            if i not in out_indices:
                map[x[i],y[i],j]=1
        mask_size[j]=len(x)
    # this variable will hold how many indices get caught in intersection for each bboxes
    double_count = np.zeros([len(bboxes)],dtype=np.uint32)
    for row in map:
        for elem in row :
            if (np.sum(elem)>1):
                # # We have an intersection between two boundng boxes.
                intersection_indices = np.where(elem==1)[0] #get the indices of the intersecting bboxes
                for indice in intersection_indices:
                    double_count[indice]+=1
    # print('[DEBUG]       bbox mask size : {}'.format(mask_size))
    # print('[DEBUG]       bbox double count : {}\n'.format(double_count))
    intersection_percentage = [a/b for a,b in itertools.zip_longest(double_count,mask_size)]
    return(intersection_percentage)

def get_bbox_rbbox_values(image,masks,bboxes):
    rbbs=[]
    hbbox_UIs=[]
    rbbox_UIs=[]
    for i in range(masks.shape[2]):
        mask = masks[:,:,i]
        # for RBB
        rbb,center = get_min_area_rect(mask)
        rbbs.append(rbb)
        #get percentage of useful information for horizontal bboxes
        hbbox_UIs.append(get_useful_info(mask,extract_points(bboxes[i])))
        # get percentage of useful information for rotated bboxes
        rbbox_UIs.append(get_useful_info(mask,rbb))
    #Get average percentage of useful information for all the bboxes of an image
    hbbox_UI=np.mean(hbbox_UIs)
    rbbox_UI=np.mean(rbbox_UIs)
    # Get average percentage of intersection between bounding boxes
    inter_percentages_hbbox = get_intersection_info([extract_points(bbox) for bbox in bboxes],masks.shape[0],masks.shape[1])
    inter_percentages_rbbox = get_intersection_info([rbb for rbb in rbbs],masks.shape[0],masks.shape[1])
    mean_inter_hbbox = np.mean(inter_percentages_hbbox)
    mean_inter_rbbox = np.mean(inter_percentages_rbbox)

    return(hbbox_UI,rbbox_UI,mean_inter_hbbox,mean_inter_rbbox)

# center,rbb=get_rbb_propositions([],[100,100,300,400])
# print(center)
# ROOT_DIR = os.path.join("D:\\","workspace","object-detection","rcnn_test")
# image = os.path.join(ROOT_DIR,'images','8433365521_9252889f9a_z.jpg')
# image=cv2.imread(image)
# display_rbb(rbb,image)
# get_min_area_rect([[1],[4]])
