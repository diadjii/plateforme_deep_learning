###Comon functions to work with annotations extracted with the VIA tool.

import os
import sys
import cv2
import json
import numpy as np
import skimage.draw
from mrcnn import visualize
ROOT_DIR = os.path.join("D:\\","workspace","object-detection","rcnn_test","mrcnn")
# sys.path.append(ROOT_DIR)
# ROOT_DIR = os.path.dirpath(os.path.abspath('__file__'))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rbb_utils

from mrcnn.utils import extract_bboxes

def concatenate_two(ann1, ann2):
    for elem in ann2 :
        if elem in ann1 :
            regions2 = ann2[elem]['regions']
            regions = ann1[elem]['regions']
            regions.extend(regions2)
        else :
            ann1[elem] = ann2[elem]
    return ann1

def concatenate(list):
    tmp = list[0].copy()
    for annotations in list[1::]:
        tmp = concatenate_two(tmp,annotations)
    return tmp

def write_annotation(annotation,path):
    with open(path,'w') as json_file:
        json.dump(annotation,json_file)

def load_masks_from_annotation(annotation, width=800, height=1024):
    ## This should be the annotatinon for a whole file.

    # Extract polygons information
    assert annotation['filename']
    assert annotation['regions']
    if type(annotation['regions']) is dict :
        polygons = [r['shape_attributes'] for r in annotation['regions'].values()]
    else:
        polygons = [r['shape_attributes'] for r in annotation['regions']]

    # Build mask
    # We will need to add classID in case of multiple labels
    masks = np.zeros([width,height,len(polygons)],dtype=np.uint8)
    for i,elem in enumerate(polygons):
        # print("all points x : {}".format(elem['all_points_x']))
        # print("all points y : {}".format(elem['all_points_y']))
        x,y = skimage.draw.polygon(elem['all_points_y'],elem['all_points_x'])
        masks[x,y,i] = 1
    return masks

def display(image,annotations, MASK=True, RBB=False, BB=True,resize = None):
    width,height=image.shape[:2]
    masks = load_masks_from_annotation(annotations,width=width,height=height)
    bboxes = extract_bboxes(masks)
    for i in range(masks.shape[2]):
        mask = masks[:,:,i]
        if MASK:
            #display mask
            image=visualize.apply_mask(image,mask,(0,255,0),alpha=0.5)
        if BB :
            #display bounding boxes
            bbox=bboxes[i]
            cv2.rectangle(image,(bbox[1],bbox[0]),(bbox[3],bbox[2]),(0,0,255),2)
        if RBB :
            # for RBB
            rbb,center = rbb_utils.get_min_area_rect(mask)
            rbb_utils.display_rbb(rbb,image)

    if resize is not None :
        image = cv2.resize(image,(resize[0],resize[1]))
    cv2.imshow("image with annotations",image)
    cv2.waitKey()

def display_from_annotation(annotation,images_dir=os.path.join(ROOT_DIR,'images'),resize=None,ext='jpg'):
    for elem in annotation:
        if '.' in elem:
            img_ext=elem.split('.')[-1]
            img_name = elem.replace(img_ext,ext)
        else:
            #image names are not well constructed so correct it here
            img_name=elem[23:]
            img_name = img_name[:-2]+'_'+img_name[-2:]
            img_name = img_name+'.'+ext
        # print(img_name)
        image=cv2.imread(os.path.join(images_dir,img_name))
        try :
            display(image,annotation[elem],resize=resize)
        except AssertionError:
            continue

def compare_bbox_rbbox_from_annotations(annotation,image_dir):
    for elem in annotation:
        img_ext = elem.split('.')[-1]
        img_name = elem.replace(img_ext,'jpg')
        image=cv2.imread(os.path.join(image_dir,img_name))
        width,height = image.shape[:2]
        # print('[INFO]   working on {}'.format(img_name))
        bbox_ABI = []
        bbox_AUI = []
        rbbox_ABI = []
        rbbox_AUI = []
        try :
            masks = load_masks_from_annotation(annotation[elem],width=width,height=height)
            bboxes = extract_bboxes(masks)
            # print('[DEBUG]      Number of objects : {}'.format(len(bboxes)))
            (a,b,c,d)=rbb_utils.get_bbox_rbbox_values(image,masks,bboxes)
            # print('[INFO]   Average useful information on image :                         - hbbox : {}  |  rbbox : {}'.format(a,b))
            # print('[INFO]   Average percentage of intersection between boxes on image :   - hbbox : {}  |  rbbox : {}'.format(c,d))
            # print('')
            bbox_ABI.append(a)
            rbbox_ABI.append(b)
            bbox_AUI.append(c)
            rbbox_AUI.append(d)
        except AssertionError:
            continue
    return (np.mean(bbox_ABI),np.mean(rbbox_ABI),np.mean(bbox_AUI),np.mean(rbbox_AUI))

def test(annotation,images_dir=os.path.join(ROOT_DIR,'images')):
    for elem in annotation:
        img_name=elem.split('.')[0]+'.jpg'
        image=cv2.imread(os.path.join(images_dir,img_name))
        w,h=image.shape[:2]
        masks  = load_masks_from_annotation(annotation[elem],w,h)
        test_MAR(masks[:,:,0])

def test_MAR(mask):
    rbb_utils.get_min_area_rect(mask)


# annotation0 = json.load(open(os.path.join(ROOT_DIR,'images','via_export_json.json')))
# annotation1 = json.load(open(os.path.join(ROOT_DIR,'images','via_test.json')))
# annotation2 = json.load(open(os.path.join(ROOT_DIR,'images','via_test_2.json')))
# image = os.path.join(ROOT_DIR,'images','8433365521_9252889f9a_z.jpg')
# image=cv2.imread(image)
# # ann=concatenate_two(annotation1,annotation2)
# ann = concatenate([annotation0,annotation1,annotation2])
# write_annotation(ann,os.path.join(ROOT_DIR,'annotation_test_3.json'))
# for elem in annotation2:
#     masks = load_masks_from_annotation(annotation2[elem])
#     print(extract_bboxes(masks))
#
# for elem in annotation2:
#     print(elem)
#     display(image,annotation2[elem])
# test(annotation0)
# display_from_annotation(ann)
# display_from_annotation(annotation1)
# annotation = json.load(open("D:\\datas\\Emile_Remote_Mango\\Sliced_Dataset\\val\\via_region_data.json"))
# display_from_annotation(annotation,"D:\\datas\\Emile_Remote_Mango\\Sliced_Dataset\\val\\")
