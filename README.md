# YourCast

YourCast is a modern podcast discovery and AI-powered episode generation platform. It allows users to explore, summarize, and even generate custom podcast episodes based on their preferences.

## Features
- **Podcast Directory:** Browse a large collection of podcasts, each with metadata and key points for each episode
- **Podcast Generation** Generate your own podcasts in audio based on key ideas from other podcasts
- **Transcript Access:** Access and analyze key points for each episode.
- **Modern Frontend:** Built with Vite, React, TypeScript, shadcn-ui, and Tailwind CSS for a fast and responsive user experience.
- **API Backend:** Powered by FastAPI for robust and scalable API endpoints.
- **Data Aggregation:** Uses Playwright for web scraping and DuckDuckGo for search integration.
- **AI & Embeddings:** Integrates with OpenAI and Pinecone for advanced search and analysis features.



## Screenshots

### Search and Select View
![Podcast Directory](screenshots/Screenshot%202025-04-27%20at%2009.47.06.png)

### Podcast Generation Interface
![Episode Details](screenshots/Screenshot%202025-04-27%20at%2009.47.16.png)

### Episode Detail View
![Podcast Generation](screenshots/Screenshot%202025-04-27%20at%2009.47.44.png)

## Pitch Deck 
[YourCast.pdf](YourCast.pdf)

## Technologies Used

- **Frontend:** Vite, React, TypeScript, shadcn-ui, Tailwind CSS
- **Backend:** FastAPI, Pydantic, Python 3.12+
- **Data & AI:** OpenAI, Pinecone, fastembed, gTTS, markdownify
- **Utilities:** Playwright, Requests, python-dotenv, python-slugify, Tenacity, coloredlogs

## Getting Started

### Prerequisites

- [Node.js & npm](https://github.com/nvm-sh/nvm#installing-and-updating) (for frontend)
- Python 3.12+ (for backend)

### Setup

1. **Clone the repository and add .env file**
Add .env file to root with following keys
OPENAI_API_KEY=...  (your OAI key)
PINECONE_API_KEY= [upon request via link](https://docs.google.com/document/d/1h3L_HQt3saVTsN7fgFhNfcFsNe_Zr5cVWdAbTPhYUQk/edit?usp=sharing)


2. **Install dependencies:**
    ```sh
    cd frontend
    npm install
    ```

3. **Start the development server:**
    ```sh
    npm run dev
    ```

### Backend Setup

1. **Install Python dependencies:**
You need to run those commands **from repo root**
    ```sh
    uv venv .venv
    source .venv/bin/activate
    uv sync  # install uv
    ```

2. **Run the FastAPI server:**
    ```sh
    python -m yourcast.api.api
    ```
3. **End enjoy the best ideas of the world**
by visiting `http://localhost:8080/`

* Note that you need to enter the query and press `Enter` key to get relevant podcasts and relevant key points within them.
* To generate a personal podcast from bits of other podcasts, click `Select` and select episodes that you're interested, then click `Confirm`
* To download the audio version of your own personally-generated podcast click `Generate Audio`, wait and then click `Download Audio`

### Data Assets

- **Podcast Metadata:** `yourcast/assets/podcast_urls.json`
  Contains podcast names, URLs, and transcript counts.
- **Episode Metadata:** `yourcast/assets/episode_urls.json`
  Contains episode titles, podcast names, publication dates, and URLs.

## Authors
* Lovis
* Nico
* Max
* Karthik

---
*This project is not affiliated with ReadablePod or any of the podcasts listed. All data is aggregated for educational and research purposes only.*