from typing import List
from config import YOUTUBE_CHANNELS
from scrapers.youtube_scraper import YouTubeScraper, ChannelVideo
from scrapers.openai_scraper import OpenAIScraper, OpenAIArticle
from scrapers.anthropic_scraper import AnthropicScraper, AnthropicArticle


def run_scapers(hours: int = 24) -> dict:
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    
    youtube_videos = []
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
        youtube_videos.extend(videos)
        
    openai_articles = openai_scraper.get_articles(hours=hours)
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    
    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles,
    }
    

if __name__ == "__main__":
    results = run_scapers(hours=24)
    print(f"YouTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")