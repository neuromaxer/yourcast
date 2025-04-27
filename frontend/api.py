from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os
import openai
from yourcast.parser.episode_parser import initialise_pinecone_index

app = FastAPI(title="YourCast API", description="API for querying podcast bulletpoints")

# Initialize Pinecone index
index_name = os.environ.get("PINECONE_INDEX_NAME", "yourpod")
pinecone_index = initialise_pinecone_index(index_name)

class BulletpointResponse(BaseModel):
    text: str
    timestamp: int
    source_podcast_name: str
    episode_name: str
    published_date: str
    listen_link: Optional[str] = ""
    score: float

class SearchResponse(BaseModel):
    results: List[BulletpointResponse]
    query: str

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
        
        # Format results
        results = []
        for match in query_results.matches:
            metadata = match.metadata
            results.append(
                BulletpointResponse(
                    text=metadata["text"],
                    timestamp=metadata["timestamp"],
                    source_podcast_name=metadata["source_podcast_name"],
                    episode_name=metadata["episode_name"],
                    published_date=metadata["published_date"],
                    listen_link=metadata.get("listen_link", ""),
                    score=match.score
                )
            )
        
        return SearchResponse(results=results, query=query)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing search: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
