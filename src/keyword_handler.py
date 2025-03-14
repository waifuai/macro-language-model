# keyword_handler.py
from typing import Dict, List, Tuple, Any, Optional
from utils import tokenize, matches

def handle_keywords(tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], used_responses: set, debug: bool) -> Optional[str]:
    """Handles general keywords."""
    if debug:
        print(f"keyword_handler.handle_keywords: Entering")
    for word in tokens:
        if debug:
            print(f"keyword_handler.handle_keywords: checking word: {word}")

        # Check for direct keyword match or synonym
        if word in keywords:
            if debug:
                print(f"keyword_handler.handle_keywords: found match (direct or synonym): {word}")
            responses = keywords[word]
            for resp_pattern, resp_text in responses:
                if matches(tokenize(resp_pattern), tokens):
                    # used_responses.add(resp_text) # Removed, not using this here
                    if debug:
                        print (f"keyword_handler.handle_keywords: Matched keyword/synonym: {word}, response: {resp_text}")
                    return resp_text
        # Check for synonym match - Removed complex logic

    if debug: # Added
        print("keyword_handler.handle_keywords: No keyword match found.") # Added
    return None