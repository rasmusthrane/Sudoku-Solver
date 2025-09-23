from typing import List

def cross(A: str, B: str) -> List[str]:
    "Cross product of strings in A and strings in B."
    return [a + b for a in A for b in B]
