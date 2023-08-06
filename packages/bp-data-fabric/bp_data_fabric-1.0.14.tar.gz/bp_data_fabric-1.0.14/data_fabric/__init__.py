from typing import List
from data_fabric.components import main

def data_fabric(
    query: str = "",
    query_tool_title: str = "",
    data_grid_title: str = "",
    data_visualization_title: str = "",
    databases: List[str] = [],
    tables: List[dict] = [],
    columns: List[dict] = [],
    error: str = "",
    show_execute=True,
    on_database_change=None,
    on_table_change=None,
    on_generate_query=None,
    on_copy_query=None,
    on_execute_query=None,
    data={},
    show_data_grid=True,
    show_charts=True,
):
    
    main(
        query=query,
        query_tool_title=query_tool_title,
        data_grid_title=data_grid_title,
        data_visualization_title=data_visualization_title,
        databases=databases,
        tables=tables,
        columns=columns,
        data=data,
        error=error,
        show_execute=show_execute,
        on_database_change=on_database_change,
        on_table_change=on_table_change,
        on_generate_query=on_generate_query,
        on_copy_query=on_copy_query,
        on_execute_query=on_execute_query,
        show_data_grid=show_data_grid,
        show_charts=show_charts,
    )