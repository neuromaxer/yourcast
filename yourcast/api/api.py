from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from yourcast.parser.episode_parser import BulletPoint, BulletPointMetadata
import os
import openai
from yourcast.parser.episode_parser import initialise_pinecone_index
from yourcast.tools.helpers import make_id, load_json
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

# export interface Episode {
#   id: number;
#   title: string;
#   host: string;
#   hostId: string;
#   image: string;
#   summary: string;
#   date: string;
#   keyTakeaways?: string[];
# }

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
    limit: int = Query(10, description="Maximum number of results to return", ge=1, le=100)
):
    try:
        # Generate embedding for the query
        response = openai.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        query_embedding = response.data[0].embedding
        
        # Query Pinecone
        query_results = pinecone_index.query(
            vector=query_embedding,
            top_k=limit,
            include_metadata=True
        )
        
        episodes = {}
        for match in query_results.matches:
            metadata = BulletPointMetadata(**match.metadata)
            bulletpoint = BulletPoint(
                text=metadata.text,
                timestamp=metadata.timestamp
            )

            if metadata.episode_name not in episodes:
                episodes[metadata.episode_name] = Episode(
                    id=make_id(metadata.episode_name),
                    title=metadata.episode_name,
                    host=metadata.source_podcast_name,
                    hostId=make_id(metadata.source_podcast_name),
                    summary=episode_summaries[metadata.episode_name],
                    date=metadata.published_date,
                    image=metadata.image,
                    keyTakeaways=[bulletpoint]
                )
            else:
                episodes[metadata.episode_name].keyTakeaways.append(bulletpoint)

        return SearchResponse(results=episodes.values())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing search: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
