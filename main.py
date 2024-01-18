from fastapi import FastAPI, File, UploadFile
import shutil
from groundlight import Groundlight

app = FastAPI()

light = False

@app.post("/upload")
async def upload_img(file: UploadFile = File(...)):
    global light
    path = "images/"
    img_path = path + file.filename
    # save image from upload
    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # analyze image
    gl = Groundlight()
    det = gl.get_or_create_detector(name="hand", query="Is there a hand?")
    qry = gl.submit_image_query(detector=det, image=img_path)
    light = qry.result.label == "YES"
    return {file.filename: light}

@app.get("/light")
def light():
    global light
    return {'light': light}

@app.get("/")
def root():
    return {"Hello": "world"}

