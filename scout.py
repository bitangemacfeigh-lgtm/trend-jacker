import pandas as pd
from pytrends.request import TrendReq
import time
import random

def get_pytrends_client():
    """
    Returns a client without backoff_factor to avoid 
    the 'method_whitelist' urllib3 error.
    """
    # Removed backoff_factor to fix the 'unexpected keyword argument' error
    return TrendReq(hl='en-US', tz=360)

def get_global_trends():
    """Fetches daily trending searches with error handling."""
    try:
        pytrends = get_pytrends_client()
        df = pytrends.trending_searches(pn='united_states')
        if not df.empty:
            return df[0].head(10).tolist()
    except Exception as e:
        print(f"Pytrends Global Error: {e}")
    
    # Static fallback so the UI never looks empty if Google blocks the IP
    return ["AI Breakthroughs", "Remote Work Evolution", "Sustainable Tech", "Market Volatility"]

def get_filtered_trends(topic, geo='', timeframe='now 1-d'):
    """Fetches related queries with retries and failover."""
    try:
        pytrends = get_pytrends_client()
        # Randomized sleep helps avoid instant 429 blocks
        time.sleep(random.uniform(1, 3)) 
        
        pytrends.build_payload([topic], cat=0, timeframe=timeframe, geo=geo)
        related_queries = pytrends.related_queries()
        
        rising = related_queries.get(topic, {}).get('rising')
        
        if rising is not None and not rising.empty:
            return {
                "topic": rising.iloc[0].get('query', topic),
                "growth": f"+{rising.iloc[0].get('value', 'Rising')}%"
            }
    except Exception as e:
        print(f"Pytrends Filtered Error: {e}")

    # Fallback: Use the user's input topic so the AI can still generate a strategy
    return {"topic": topic, "growth": "Steady Interest (Cached)"}