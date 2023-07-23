# importing the libraries
from app.camera import Camera
from app.motion import Detector
from app.video import Streaming
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

webcam = Camera(camid=0)
motion_detector = Detector()
streaming = Streaming(camera=webcam, detector=motion_detector)


@app.get("/stream")
async def stream_video():
    return StreamingResponse(
        streaming.start(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
