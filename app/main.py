from fastapi import FastAPI, File, UploadFile, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import itertools
import shutil
from groundlight import Groundlight
import cv2
import cv2.aruco as aruco
import numpy as np
import os


app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")

NEW_NAME = ""
PER_FULL = -1
FULL = False
MIXD = False


def largest_aruco_id(im_path):
    """identify the largest aruco code present in a image"""
    image = cv2.imread(im_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    aruco_params = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    if ids is not None:
        ids = ids.flatten()
        largest_id = np.max(ids)
        return int(largest_id)
    else:
        return -1


def ground(im_path, det_name, det_qry):
    """query groudlight AI for image analysis"""
    gl = Groundlight()
    det = gl.get_or_create_detector(name=det_name, query=det_qry)
    qry = gl.submit_image_query(detector=det, image=im_path)
    return qry.result.label == "YES"


@app.post("/upload")
async def upload_img(file: UploadFile = File(...)):
    """raspberry pi uploads photos"""
    global NEW_NAME, PER_FULL, FULL, MIXD
    path = "images/"
    im_path = path + file.filename
    with open(im_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    NEW_NAME = file.filename
    PER_FULL = largest_aruco_id(im_path)
    FULL = ground(im_path, "hand", "Is there a hand?")
    # MIXD = ground(im_path, "mixed_waste1", "Is concrete the only thing in the bin?")
    return {}


@app.get("/latest")
async def get_latest_info():
    """frontend updates info"""
    global NEW_NAME, PER_FULL, FULL, MIXD
    return JSONResponse({
        "im_path": f"/images/{NEW_NAME}",
        "per_full": PER_FULL,
        "full": FULL,
        "mixd": MIXD,
    })


@app.get("/")
async def get_home(request: Request):
    """serve homepage"""
    return templates.TemplateResponse("index.html", {"request": request})

