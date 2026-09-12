from ddgs import DDGS
from ollama import chat


# =========================================================
# SEARCH AGRICULTURAL INFORMATION
# =========================================================

def search_web(disease, max_results=6):

    queries = [
        f"{disease} tomato disease symptoms treatment",
        f"{disease} tomato management prevention",
        f"{disease} tomato disease extension fungicide",
    ]

    results = []

    with DDGS() as ddgs:

        for query in queries:

            try:
                search_results = ddgs.text(
                    query,
                    region="in-en",
                    safesearch="moderate",
                    max_results=max_results
                )

                for item in search_results:

                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "content": item.get("body", "")
                    })

            except Exception as e:

                print("Search error:", e)

    # Remove duplicate URLs
    unique = {}

    for result in results:

        url = result["url"]

        if url and url not in unique:
            unique[url] = result

    return list(unique.values())


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(results):

    context = ""

    for i, result in enumerate(results[:12], start=1):

        context += f"""
SOURCE {i}

Title:
{result['title']}

URL:
{result['url']}

Information:
{result['content']}

--------------------------------
"""

    return context


# =========================================================
# AI AGENT
# =========================================================

def generate_agent_response(
    disease,
    confidence,
    crop="Tomato",
    location="India"
):

    print("Searching agricultural information...")

    sources = search_web(disease)

    if not sources:

        return {
            "answer": (
                "I could not retrieve current agricultural information. "
                "Please try again."
            ),
            "sources": []
        }

    context = build_context(sources)

    prompt = f"""
You are an agricultural AI assistant.

You are analyzing a tomato leaf disease prediction.

MODEL PREDICTION:
Disease: {disease}
Confidence: {confidence}%
Crop: {crop}
Location: {location}

Use the retrieved agricultural sources below.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not claim the model diagnosis is 100% certain.
3. Clearly distinguish model prediction from confirmed diagnosis.
4. Give practical agricultural guidance.
5. For pesticide/fungicide recommendations, do not invent dosage.
6. Recommend following the locally approved product label.
7. If the sources disagree, explain the uncertainty.
8. Prefer information supported by agricultural universities,
   government agriculture departments, extension services,
   research institutions, or other authoritative sources.
9. Mention the sources used.

Provide the response using this structure:

1. Prediction
2. Confidence
3. What this disease is
4. Why this prediction may be consistent with the image
5. Cause
6. Common symptoms
7. Severity
8. What to do immediately
9. Treatment / management
10. Prevention
11. When to seek expert confirmation
12. Sources

Retrieved information:

{context}
"""

    try:

        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False
        )

        answer = response.message.content

    except Exception as e:

        print("Ollama error:", e)

        answer = (
            "The disease was detected, but the AI explanation "
            "could not be generated."
        )

    return {
        "answer": answer,
        "sources": sources[:10]
    }