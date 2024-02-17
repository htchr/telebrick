from fastapi import FastAPI, File, UploadFile
import shutil
from groundlight import Groundlight
import cv2
import cv2.aruco as aruco
import numpy as np


app = FastAPI()

LIGHT = False
FULL = False
PER_FULL = -1

def find_aruco(im_path):
    img = cv2.imread(im_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict_types = [
        aruco.DICT_4X4_50, aruco.DICT_4X4_100, aruco.DICT_4X4_250, aruco.DICT_4X4_1000,
        aruco.DICT_5X5_50, aruco.DICT_5X5_100, aruco.DICT_5X5_250, aruco.DICT_5X5_1000,
        aruco.DICT_6X6_50, aruco.DICT_6X6_100, aruco.DICT_6X6_250, aruco.DICT_6X6_1000,
        aruco.DICT_7X7_50, aruco.DICT_7X7_100, aruco.DICT_7X7_250, aruco.DICT_7X7_1000,
        aruco.DICT_ARUCO_ORIGINAL]
    for dict_type in aruco_dict_types:
        aruco_dict = aruco.Dictionary_get(dict_type)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if ids is not None:
            return True
    return False

def print_largest_aruco_id(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    aruco_params = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    if ids is not None:
        ids = ids.flatten()
        largest_id = np.max(ids)
        # print(f"Largest Aruco ID: {largest_id}")
        return int(largest_id)
    else:
        return -1

"""
def find_aruco(im_path):
    img = cv2.imread(im_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4x4_1000)
    parameters = aruco.DetectorParameters(aruco_dict)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return ids is not None
"""

# find_aruco("/home/jack/telebrick/images/202401312126test.jpg")

@app.post("/upload")
async def upload_img(file: UploadFile = File(...)):
    global LIGHT
    global FULL
    global PER_FULL
    path = "images/"
    im_path = path + file.filename
    # save image from upload
    with open(im_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # find aruco
    FULL = find_aruco(im_path)
    PER_FULL = print_largest_aruco_id(im_path)
    """
    # analyze image
    gl = Groundlight()
    det = gl.get_or_create_detector(name="hand", query="Is there a hand?")
    qry = gl.submit_image_query(detector=det, image=img_path)
    LIGHT = qry.result.label == "YES"
    """
    return {file.filename: LIGHT}

@app.get("/light")
def light():
    global LIGHT
    return {'light': LIGHT}

@app.get("/full")
def full():
    global FULL
    return {'full': FULL}

@app.get("/per_full")
def per_full():
    global PER_FULL
    return {'per_full': PER_FULL}

@app.get("/")
def root():
    return {"Hello": "world"}

