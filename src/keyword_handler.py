from typing import Dict, List, Tuple, Any, Optional
from utils import tokenize, matches

def handle_keywords(tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], used_responses: set, debug: bool) -> Optional[str]:
    """Handles general keywords."""
    if debug:
        print(f"keyword_handler.handle_keywords: Entering")
    for word in tokens:
        if word in keywords:
            responses = keywords[word]
            for resp_pattern, resp_text in responses:
                if matches(tokenize(resp_pattern), tokens):
                    used_responses.add(resp_text)
                    if debug:
                        print (f"keyword_handler.handle_keywords: Matched keyword: {word}, response: {resp_text}")
                    return resp_text
    return None