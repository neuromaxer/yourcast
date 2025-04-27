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

1. **Clone the repository:**


2. **Install dependencies:**
    ```sh
    npm install 
    ```

3. **Start the development server:**
    ```sh
    npm run dev
    ```

### Backend Setup

1. **Install Python dependencies:**
    ```sh
    uv sync  # install uv
    ```

2. **Run the FastAPI server:**
    ```sh
    python -m yourcast.api.api     
    ```

### Data Assets

- **Podcast Metadata:** `yourcast/assets/podcast_urls.json`  
  Contains podcast names, URLs, and transcript counts.
- **Episode Metadata:** `yourcast/assets/episode_urls.json`  
  Contains episode titles, podcast names, publication dates, and URLs.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*This project is not affiliated with ReadablePod or any of the podcasts listed. All data is aggregated for educational and research purposes only.*