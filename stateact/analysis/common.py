"""Small helpers shared by the benchmark analyses."""

import string

__all__ = ["clean_model_string", "require_pandas"]


def require_pandas():
    """Import pandas lazily so the rest of stateact stays dependency-free."""
    import pandas as pd

    return pd


def clean_model_string(model):
    """Normalise a model name for use in a CSV/JSON file name.

    Kept identical to ``clean_model_string`` in the WebShop/TextCraft scripts.
    """
    model = str(model).lower().replace("/", "_")
    punctuation = str.maketrans(
        {char: "-" for char in string.punctuation if char != "_"}
    )
    return model.translate(punctuation)
