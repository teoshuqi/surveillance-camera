# importing the libraries
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import scripts.camera as camera
import scripts.motion as motion
import scripts.video as video

app = FastAPI()

webcam = camera.Camera(camid=0)
motion_detector = motion.Detector()
streaming = video.Streaming(camera=webcam, detector=motion_detector)


@app.get("/stream")
async def stream_video():
    return StreamingResponse(streaming.start(),
                             media_type="multipart/x-mixed-replace; \
                                boundary=frame")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
