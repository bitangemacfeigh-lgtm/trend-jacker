import pandas as pd
from pytrends.request import TrendReq

def get_global_trends():
    """Fetches daily trending searches globally."""
    pytrends = TrendReq(hl='en-US', tz=360)
    # Get trending searches for a major region (e.g., US or Global)
    try:
        df = pytrends.trending_searches(pn='united_states') # 'pn' is the country name
        return df[0].head(10).tolist() # Returns top 10 trends
    except:
        return ["AI breakthroughs", "Tech layoffs", "Global Economic Shift"]

def get_filtered_trends(topic, geo='', timeframe='now 1-d'):
    """Advanced search based on user filters."""
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # geo is the 2-letter country code (e.g., 'KE' for Kenya, 'US' for USA)
    pytrends.build_payload([topic], cat=0, timeframe=timeframe, geo=geo)
    
    related_queries = pytrends.related_queries()
    rising = related_queries.get(topic, {}).get('rising')
    
    if rising is not None and not rising.empty:
        return {
            "topic": rising.iloc[0]['query'],
            "growth": rising.iloc[0]['value']
        }
    return {"topic": topic, "growth": "Steady Interest"}