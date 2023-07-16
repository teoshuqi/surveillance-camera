# importing the libraries
import camera
import motion
import uvicorn
import video
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

webcam = camera.Camera(camid=-1)
motion_detector = motion.Detector()
streaming = video.Streaming(camera=webcam, detector=motion_detector)


@app.get("/stream")
async def stream_video():
    return StreamingResponse(
        streaming.start(),
        media_type="multipart/x-mixed-replace; \
                                boundary=frame",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
