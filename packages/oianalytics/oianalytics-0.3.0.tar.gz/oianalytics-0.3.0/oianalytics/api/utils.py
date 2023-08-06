from typing import Union, Optional, List, Callable
import dateutil
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd


def get_zulu_isoformat(date: Union[str, datetime]):
    # Parse date if it is a string
    if isinstance(date, str):
        date = dateutil.parser.parse(date)

    # Serialize date
    return date.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def expand_dataframe_column(
    df: pd.DataFrame,
    col: str,
    add_prefix: bool = True,
    expected_keys: Optional[List[str]] = None,
):
    col_loc = df.columns.get_loc(col)

    # Expand the target column
    if df.shape[0] == 0:
        if expected_keys is None:
            expanded_col = df[col].to_frame()
        else:
            expanded_col = pd.DataFrame(index=df.index, columns=expected_keys)
    else:
        expanded_col = df[col].apply(pd.Series)

    if expanded_col.shape[1] == 0:
        expanded_col[col] = np.NaN

    # Rename generated column using prefix
    if add_prefix is True:
        expanded_col = expanded_col.add_prefix(f"{col}_")

    # Concatenate parts of dataframe
    expanded_df = pd.concat(
        [df[df.columns[:col_loc]], expanded_col, df[df.columns[col_loc + 1 :]]], axis=1
    )

    return expanded_df


def concat_pages_to_dataframe(
    getter: Callable,
    parser: Callable,
    page: int = 0,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
):
    # Init
    def get_and_parse_page(page_num: int):
        page_response = getter(page_num)
        return parser(page_response)

    # Get first page
    response = getter(page_num=page)
    df = parser(response)

    total_pages = response["totalPages"]
    if get_all_pages is True and total_pages > 1:
        pages_to_get = range(1, total_pages)

        if multithread_pages is True:
            with ThreadPoolExecutor() as pool:
                page_dfs = list(pool.map(get_and_parse_page, pages_to_get))
        else:
            page_dfs = []
            for i in pages_to_get:
                page_dfs.append(get_and_parse_page(page_num=i))

        # Concatenate additional pages with the first one
        df = pd.concat([df] + page_dfs)

    # Concat dataframes
    return df
