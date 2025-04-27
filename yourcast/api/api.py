import os
import tempfile
import uuid
from typing import List, Optional

import openai
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from gtts import gTTS
from pydantic import BaseModel

from yourcast.parser.episode_parser import BulletPoint, BulletPointMetadata, initialise_pinecone_index
from yourcast.tools.helpers import load_json, make_id
from yourcast.tools.llm_helpers import OpenaiModelNames, get_llm_completion

MODEL = OpenaiModelNames.gpt4o_mini

app = FastAPI(title="YourCast API", description="API for querying podcast bulletpoints")

# Allow CORS for http://localhost:8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone index
index_name = os.environ.get("PINECONE_INDEX_NAME", "yourpod")
pinecone_index = initialise_pinecone_index(index_name)
episode_summaries = load_json("yourcast/assets/episode_summaries")


class PodcastData(BaseModel):
    id: int
    title: str
    host: str
    hostId: str
    image: str
    summary: str
    date: str
    keyTakeaways: List[str]


class PodcastRequest(BaseModel):
    data_sample: List[PodcastData]
    length: str
    tone: str
    style: str


class Episode(BaseModel):
    id: str
    title: str
    host: str
    hostId: str
    image: str
    summary: str
    date: str
    keyTakeaways: List[BulletPoint]


class SearchResponse(BaseModel):
    results: List[Episode]


@app.get("/", response_model=dict)
async def root():
    return {"message": "Welcome to YourCast API. Use /search endpoint to query bulletpoints."}


@app.get("/search", response_model=SearchResponse)
async def search_bulletpoints(
    query: str = Query(..., description="Natural language query to search for relevant bulletpoints"),
    limit: int = Query(10, description="Maximum number of results to return", ge=1, le=100),
):
    try:
        # Generate embedding for the query
        response = openai.embeddings.create(input=query, model="text-embedding-3-small")
        query_embedding = response.data[0].embedding

        # Query Pinecone
        query_results = pinecone_index.query(vector=query_embedding, top_k=limit, include_metadata=True)

        episodes = {}
        for match in query_results.matches:
            metadata = BulletPointMetadata(**match.metadata)
            bulletpoint = BulletPoint(text=metadata.text, timestamp=metadata.timestamp)

            if metadata.episode_name not in episodes:
                episodes[metadata.episode_name] = Episode(
                    id=make_id(metadata.episode_name),
                    title=metadata.episode_name,
                    host=metadata.source_podcast_name,
                    hostId=make_id(metadata.source_podcast_name),
                    summary=episode_summaries[metadata.episode_name],
                    date=metadata.published_date,
                    image=metadata.image,
                    keyTakeaways=[bulletpoint],
                )
            else:
                episodes[metadata.episode_name].keyTakeaways.append(bulletpoint)

        return SearchResponse(results=episodes.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing search: {str(e)}")


@app.post(
    "/summary_audio",
    summary="Generate an MP3 audio summary from given podcast keyTakeaways",
    response_class=FileResponse,
    responses={200: {"content": {"audio/mpeg": {}}}},
)
async def generate_summary_audio(request: PodcastRequest):
    """
    1. Flattens all keyTakeaways from the payload into one prompt.
    2. Uses OpenAI ChatCompletion to produce a cohesive summary.
    3. Converts the summary to speech (MP3) via gTTS.
    4. Returns the MP3 as a FileResponse.
    """
    # 1. Flatten the bullet-points
    all_bullets = []
    for pd in request.data_sample:
        # pd.keyTakeaways is List[str]
        all_bullets.extend(pd.keyTakeaways)

    bullet_list = "\n".join(f"- {b}" for b in all_bullets)
    system_prompt = (
        f"You are a creative podcast scriptwriter. "
        f"Given a list of key takeaways from a podcast episode, your task is to write a natural, engaging dialogue between two hosts. "
        f"The conversation should cover all the key points, flow smoothly, and sound like a real discussion. "
        f"Make sure the dialogue is {request.length}, has a {request.tone} tone, and is written in a {request.style} style. "
        "Feel free to add questions, reactions, and transitions to make the dialogue lively and authentic."
    )

    user_prompt = (
        f"Here are the key takeaways from the episode:\n{bullet_list}\n\n"
        "Please write a dialogue between Host 1 and Host 2 that covers all these points."
        "Don't add asterisks or host 1 or host 2"
    )

    # 2. Call OpenAI to get the text summary
    chat_resp = get_llm_completion(system_prompt, user_prompt, MODEL)

    # 3. Convert text summary to an MP3 file
    tts = gTTS(text=chat_resp.content, lang="en")
    # Use a temp file so we don't collide in concurrent requests
    tmp = tempfile.NamedTemporaryFile(prefix="yourcast_summary_", suffix=".mp3", delete=False)
    tmp_path = tmp.name
    tmp.close()
    tts.save(tmp_path)

    # 4. Return the MP3 file
    return FileResponse(path=tmp_path, media_type="audio/mpeg", filename=f"podcast_summary_{uuid.uuid4().hex}.mp3")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
