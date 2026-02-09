# TESTING THE SCRAPER AND DATABASE CONNECTIONS

from app.runner import run_scrapers

def main(hours: int = 24):
    results = run_scrapers(hours=hours)
    
    print(f"\n=== Scraping Results (last {hours} hours) ===")
    print(f"YouTube Videos: {len(results['youtube'])}")
    print(f"OpenAI Articles: {len(results['openai'])}")
    print(f"Anthropic Articles: {len(results['anthropic'])}")
    
    return results


if __name__ == "__main__":
    main(hours=150)