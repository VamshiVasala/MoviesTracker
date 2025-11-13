import requests


import urllib.request
import urllib.parse
import json
import ssl
import ssl
import urllib.request
import urllib.parse
import json

import os, requests

API_KEY= os.getenv('BACKEND_API_KEY')

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"



def generate_text(prompt, title_or_genre):
    
    full_prompt = f"{prompt}\nContext: {title_or_genre}"


    data = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
            
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }


    response = requests.post(GEMINI_URL, headers=headers, json=data)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"


    result = response.json()
    generated_text = (
        result.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    )

    return generated_text



def fetch_wikipedia_image(title):
    ctx = ssl._create_unverified_context()
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MyMovieApp/1.0; +https://example.com)"}


    search_url = (
        f"https://en.wikipedia.org/w/api.php?action=query&list=search"
        f"&srsearch={urllib.parse.quote(title + ' film')}&format=json"
    )
    search_req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(search_req, context=ctx) as sresp:
        search_data = json.load(sresp)
        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            return None
        best_title = search_results[0]["title"]


    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(best_title)}"
    summary_req = urllib.request.Request(summary_url, headers=headers)
    with urllib.request.urlopen(summary_req, context=ctx) as sresp:
        summary_data = json.load(sresp)
        image_url = summary_data.get("originalimage", {}).get("source") or summary_data.get("thumbnail", {}).get("source")

    return image_url


Genreprompt = """
You are a knowledgeable movie assistant.
From the following movie description, identify all the genres that apply.
Return the result as a valid JSON list of strings.
Do not include explanations or extra text — only the JSON list.

Example output:
["Action", "Adventure", "Drama"]

Movie description:
{paragraph}

Output:
"""

import urllib.request
import urllib.parse
import json
import ssl

def fetch_Genres(title, word_limit=500):
    """
    Fetch movie info (first 500 words + image URL) from Wikipedia.
    Returns: {'title': best_title, 'text': first_500_words, 'image_url': image_link}
    """
    try:
        ctx = ssl._create_unverified_context()
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MyMovieApp/1.0; +https://example.com)"}

        
        search_url = (
            f"https://en.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={urllib.parse.quote(title + ' movie')}&format=json"
        )
        search_req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(search_req, context=ctx) as sresp:
            search_data = json.load(sresp)
            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
               
                return {"title": title, "text": None, "image_url": None}

            best_title = search_results[0]["title"]

      
        extract_url = (
            f"https://en.wikipedia.org/w/api.php?action=query&format=json"
            f"&titles={urllib.parse.quote(best_title)}&prop=extracts&explaintext=true&redirects=1"
        )
        extract_req = urllib.request.Request(extract_url, headers=headers)
        with urllib.request.urlopen(extract_req, context=ctx) as resp:
            data = json.load(resp)
            pages = data["query"]["pages"]
            page = next(iter(pages.values()))
            text = page.get("extract", "")

        
        words = text.split()
        first_part = " ".join(words[:word_limit])

        return {"text": first_part}

    except Exception as e:
       
        return {"title": title, "text": None, "image_url": None}





Movieprompt = """
You are a helpful movie recommendation assistant.

Given a list of movie genres and main cast members, suggest 10 movies or web series that are *most related* to the given genres and cast. 
Focus on thematic, stylistic, and performance-based similarities — not just popularity.

For each recommended title, include the following fields:
- "title": the name of the movie or web series
- "year_of_release": the release year
- "language": the original language
- "short_synopsis": a 1–2 sentence description of the plot or theme
- "main_cast": top actors or actresses
- "poster_url": an official or Wikipedia image link (if available)
- "type": "movie" or "webseries"
- "genre": the relevant genres
- "relation_reason": a brief line explaining why it fits the given genres and cast (e.g., "same genre and lead actor known for similar roles")

Input details:
Genres and Cast:
{genres_and_cast}

Return the result as valid JSON — a list of movie or webseries objects with double quotes.
"""

def format_list(items):
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]

def newData(genres,cast):
    genresInput = format_list(genres)
    castInput = format_list(cast)
    genandcast = f"Genres: {genresInput}\nCast: {castInput}"
    finalRes = []
    
    recommended_result = generate_text(Movieprompt, genandcast)
 
    import json
    import re


    match = re.search(r"\[.*\]", recommended_result, re.DOTALL)
    if match:
        try:
            recommended_json = json.loads(match.group())
        except json.JSONDecodeError:
            recommended_json = []
    else:
        recommended_json = []

    for movie in recommended_json:
        movie["poster_url"] = fetch_wikipedia_image(movie["title"])
    finalRes.append(recommended_json)
 
    return finalRes 



