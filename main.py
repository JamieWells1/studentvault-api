from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/transcript/")
async def get_transcript(video_id: str):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text into a single string
        captions = " ".join([item["text"] for item in transcript])
        # Return the captions in a JSON response
        return {"captions": captions}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
