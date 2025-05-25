import math

def clean_vector(vector: list[float]) -> list[float]:
    """
    Replaces invalid JSON values ​​(NaN, inf, -inf) with 0.0.
    """
    return [v if math.isfinite(v) else 0.0 for v in vector]