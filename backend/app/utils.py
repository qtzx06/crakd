
def parse_query(query: str) -> dict:
    """
    A simple parser to extract language and role from a search query.
    This is a placeholder for a more sophisticated NLP solution.
    """
    parsed = {
        "language": None,
        "role": None,
        "keywords": []
    }

    # Simple language detection
    languages = ["rust", "python", "go", "typescript", "javascript", "java", "c++"]
    for lang in languages:
        if lang in query.lower():
            parsed["language"] = lang
            break # Take the first one found

    # Simple role detection
    roles = ["engineer", "developer", "researcher", "architect", "lead", "manager"]
    for role in roles:
        if role in query.lower():
            parsed["role"] = role
            break
    
    # Stop words to ignore
    stop_words = ["find", "me", "a", "an", "the", "is", "are", "in", "on", "at", "for", "with", "of", "and", "or", "but", "cracked"]

    # Treat the rest as keywords, filtering out stop words
    parsed["keywords"] = [word for word in query.split() if word.lower() not in languages and word.lower() not in roles and word.lower() not in stop_words]

    return parsed
