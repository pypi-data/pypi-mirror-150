import os
from typing import Optional

import pandas as pd
from rich.table import Table

from audit_tools.core.utils.file_manager import import_file, export_file
from audit_tools.core.utils.logger import get_logger


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj. from @neelabalan on Github

    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values."""

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []

        variance_index = pandas_dataframe.columns.get_loc("Variance")
        if variance_index is not None:
            try:
                if int(value_list[4]) >= 1 or int(value_list[4]) <= -1:
                    value_list[4] = f"[bold red]{value_list[4]}"
            except ValueError:
                pass

        row += [str(x) for x in value_list]

        rich_table.add_row(*row)

    return rich_table
