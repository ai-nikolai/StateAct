"""Analysis helpers for the benchmark result logs.

This subpackage is deliberately separate from the runner/agent code: it only
needs pandas (and only when a function is called). The ALFWorld names mirror
the helpers that used to live in ``analysis_alfworld_eval_notebook.ipynb`` so
existing notebooks keep working after a one-line import change::

    from stateact.analysis.alfworld import load_data, analyse_data_old

WebShop and TextCraft have small loaders for their ``scores.csv`` /
``results.csv`` formats.
"""

from stateact.analysis import alfworld, textcraft, webshop
from stateact.analysis.alfworld import (
    analyse_data_basic,
    analyse_data_new,
    analyse_data_old,
    convert_bool_string_to_bool_int,
    convert_string_to_bool,
    convert_string_to_bool_int,
    create_pivot,
    get_data_file_path,
    load_data,
    no_groupby_analyse_data,
)
from stateact.analysis.common import clean_model_string
from stateact.analysis.textcraft import load_results as load_textcraft_results
from stateact.analysis.webshop import load_scores as load_webshop_scores

__all__ = [
    "alfworld",
    "webshop",
    "textcraft",
    "analyse_data_basic",
    "analyse_data_new",
    "analyse_data_old",
    "convert_bool_string_to_bool_int",
    "convert_string_to_bool",
    "convert_string_to_bool_int",
    "create_pivot",
    "get_data_file_path",
    "load_data",
    "no_groupby_analyse_data",
    "clean_model_string",
    "load_textcraft_results",
    "load_webshop_scores",
]
