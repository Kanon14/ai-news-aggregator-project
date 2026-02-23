# AI News Aggregator
An intelligent news aggregation system that scrapes AI-related content from multiple sources (RSS feeds, YouTube videos), processes them with LLM-powered summarization, and sends curated personalized digests based on user preferences, and delivers daily email summaries. 

## Features
This project includes the following key features:
- **RSS Feeds**: Scrapes AI-related content from multiple RSS feeds.
- **YouTube Videos**: Scrapes AI-related content from YouTube videos.
- **LLM Summarization**: Processes the scraped content with LLM-powered summarization.
- **Personalized Digests**: Curates personalized digests based on user preferences.
- **Daily Email Summaries**: Sends daily email summaries to users.

## Project Structure
The project directory structure is as follows:
```map
app/
├── agent/                   # Agent classes
│   ├── base.py              # Base agent class
│   ├── curator_agent.py     # Curator agent class
│   ├── digest_agent.py      # Digest content generation
│   └── email_agent.py       # Email content generation
│
├── database/                # Database layer
│   ├── check_connection.py  # Connection check and environment
│   ├── connection.py        # DB connection & environment
│   ├── create_tables.py     # Database schema creation
│   ├── models.py            # SQLAlchemy models
│   └── repository.py        # Data access layer
│
├── profiles/                # User profile configuration
│   └── user_profile.py
│
├── scrapers/                # Content scrapers
│   ├── base.py              # Base scraper for RSS feeds
│   ├── anthropic_scraper.py # Anthropic RSS scraper
│   ├── openai_scraper.py    # OpenAI RSS scraper
│   └── youtube_scraper.py   # YouTube channel scraper
│
├── services/                # Processing services
│   ├── base.py              # Base process service
│   ├── process_anthropic.py
│   ├── process_youtube.py
│   ├── process_digest.py
│   ├── process_curator.py
│   ├── process_email.py
│   └── email.py             # Email sending
│
├── config.py                # Configuration (YouTube channels ID)
├── daily_runner.py          # Main pipeline orchestrator
└── runner.py                # Scraper registry & execution

```

## Setup

### Prequisites
* Python 3.11+
* PostgreSQL database
* Docker (optional, local testing)
* OpenAI API key
* Gmail account and app password (for email sending)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Kanon14/ai-news-aggregator-project.git
```

2. Navigate to the project directory:
```bash
cd ai-news-aggregator-project
```

3. Install dependencies:
```bash
uv sync # If you have uv installed
pip install -r requirements.txt
```

4. Configure `.env` environment variables:
```bash
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
MY_EMAIL="YOUR_EMAIL_ADDRESS"
APP_PASSWORD="YOUR_APP_PASSWORD"
DATABASE_URL=postgresql://user:pass@host:port/db
ENVIRONMENT=LOCAL  # Optional: auto-detected from DATABASE_URL if contains "render.com"
```

5. Configure YouTube channels ID in `./app/config.py` based on your preferences.

6. Update user profile in `./app/profiles/user_profile.py` with your desired settings.

### Running the Project
```bash
uv run main.py
```

## Deployment
This project is configured for deployment on Render.com with free tier. To deploy, follow these steps:
1. **Create Database**: Create a PostgreSQL database and configure the `DATABASE_URL` in `.env`.
2. **Cron Job**: Scheduled daily execution via `render.yaml`.
3. **Environment**: Automatically detected as PRODUCTION when `DATABASE_URL` contains "render.com".

## Docker
To run the project in a Docker container, use the following command:
```bash
docker build -t ai-news-aggregator-project .
docker run --name ai-news-aggregator-project -d -p 8000:8000 ai-news-aggregator-project
```
* Make sure the database is connected and running before running the container.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.