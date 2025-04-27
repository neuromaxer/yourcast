

Backend (yourcast/api/api.py)
Overview
The backend is built with FastAPI and provides endpoints to:
Search podcast bulletpoints using semantic search (via OpenAI embeddings and Pinecone vector database).
Generate audio summaries of podcast episodes, turning key takeaways into a natural-sounding dialogue and converting it to MP3 using gTTS.
Features
Semantic Search: Query podcast episode highlights using natural language.
Audio Summaries: Generate and download MP3 summaries as engaging host dialogues.
CORS Enabled: Allows frontend (e.g., on localhost:8080) to interact with the API.
Endpoints
GET /
Welcome message and API usage hint.
GET /search?query=...&limit=...
Search for relevant podcast bulletpoints using a natural language query.
POST /summary_audio
Generate an MP3 audio summary from provided podcast key takeaways.
Technologies
FastAPI for API endpoints
OpenAI for embeddings and LLM completions
Pinecone for vector search
gTTS for text-to-speech
Pydantic for data validation
Setup
1. Install dependencies:
gtts
Set environment variables:
OPENAI_API_KEY
PINECONE_API_KEY
(Optional) PINECONE_INDEX_NAME
3. Run the server:
reload
4. API Docs:
Visit http://localhost:8000/docs for interactive documentation.
---
Frontend
Overview
The frontend (not shown in your code, but implied by CORS and typical usage) is likely a web application running on localhost:8080 that interacts with the backend API.
Features
Search Interface: Enter queries to find relevant podcast episode highlights.
Audio Summary Generator: Select episodes and generate/download audio summaries as host dialogues.
Technologies (Assumed)
Vue.js or React (common for port 8080)
Fetch/Axios for API requests
Audio Player for playing MP3 summaries
Setup
1. Install dependencies:
install
Run the development server:
serve
Access the app:
Visit http://localhost:8080
Example Usage
Search:
Enter a question like “What did the hosts say about AI in episode 5?” and view relevant bulletpoints.
Generate Audio Summary:
Select key takeaways, choose summary style/tone/length, and download or play the generated MP3.
---
What Does YourCast Do?
YourCast makes podcast content more accessible and interactive by:
Summarizing episodes into key bulletpoints.
Enabling semantic search so users can find highlights by asking questions in plain English.
Generating natural-sounding audio summaries in the form of host dialogues, making it easy to catch up on episodes or share highlights.
---
Project Structure (Inferred)
)
---
Contributing
Fork the repo and clone it.
Set up backend and frontend as above.
Submit pull requests for improvements or bug fixes.
---
License
MIT License
---
Let me know if you want a more detailed frontend README or a template for a specific framework!