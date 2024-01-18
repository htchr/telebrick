from groundlight import Groundlight

gl = Groundlight()
det = gl.get_or_create_detector(name="hand", query="Is there a hand?")
img1 = "ground/hand.jpg"
img2 = "ground/nothand.jpg"
query1 = gl.submit_image_query(detector=det, image=img1)
query2 = gl.submit_image_query(detector=det, image=img2)
print(f"q1: {query1.result.label}")
print(f"q2: {query2.result.label}")
