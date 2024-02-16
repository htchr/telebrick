from fastapi import FastAPI, File, UploadFile
import shutil
from groundlight import Groundlight
import cv2
import cv2.aruco as aruco
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os

app = FastAPI()

LIGHT = False
FULL = False

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
    path = "images/"
    im_path = path + file.filename
    # save image from upload
    with open(im_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # find aruco
    FULL = find_aruco(im_path)
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

@app.get("/")
def root():
    return {"Hello": "world"}



# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the directory containing the images to serve them statically
app.mount("/images", StaticFiles(directory="images"), name="images")

# Define the path to the directory containing the images
IMAGES_DIR = "images"

@app.get("/latest")
async def serve():
    global LIGHT
    global FULL
    # Sample data for 'full' and 'light' attributes
    sample_data = {"light": LIGHT, "full": FULL}

    #!!! substitute with name of most recent image!!!
    image_filename = "test.png"
    image_path = os.path.join(IMAGES_DIR, image_filename)

    # Construct the full URL to the image
    image_url = f"http://localhost:8000/images/{image_filename}"

    # Construct the response object
    response_data = {"light": sample_data["light"], "full": sample_data["full"], "image": image_url}

    return response_data
