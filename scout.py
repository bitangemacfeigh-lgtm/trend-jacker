import pandas as pd
from pytrends.request import TrendReq
import time

def get_google_trends(niche="AI in Kenya"):
    """Fetches trending related queries for a specific niche."""
    print(f"🔍 Searching Google Trends for: {niche}...")
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Build payload
    pytrends.build_payload([niche], cat=0, timeframe='now 1-d', geo='', gprop='')
    
    # Get related queries
    related_queries = pytrends.related_queries()
    
    # We look at 'rising' queries (those with % growth or 'Breakout')
    rising_trends = related_queries.get(niche, {}).get('rising')
    
    if rising_trends is not None and not rising_trends.empty:
        # Filter for 'Breakout' or high percentage
        top_trend = rising_trends.iloc[0]['query']
        value = rising_trends.iloc[0]['value']
        return {"topic": top_trend, "growth": value}
    
    return None

def scout_all_sources(niche):
    """Aggregates trends from multiple sources."""
    # Phase 2 focus: Google Trends
    g_trend = get_google_trends(niche)
    
    if g_trend:
        print(f"🔥 Found Spike: '{g_trend['topic']}' (Growth: {g_trend['growth']})")
        return g_trend
    else:
        print("Cooling down... no major spikes detected.")
        return None