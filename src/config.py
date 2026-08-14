import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    """
    Central configuration for the Databricks GenAI Data Analyst Copilot.

    Environment-specific values should be supplied through environment
    variables or Databricks configuration rather than hard-coded secrets.
    """

    catalog: str = os.getenv(
        "GENAI_COPILOT_CATALOG",
        "main"
    )

    bronze_schema: str = "bronze"
    silver_schema: str = "silver"
    gold_schema: str = "gold"

    sales_table: str = "sales"

    max_sql_length: int = 10_000
    max_result_rows: int = 1_000


config = ProjectConfig()
