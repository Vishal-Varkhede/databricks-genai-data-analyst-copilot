# Architecture

## Databricks GenAI Data Analyst Copilot

The project combines:

- Databricks
- Unity Catalog
- Delta Lake
- PySpark
- Spark SQL
- Natural-language-to-SQL
- LLMs
- RAG
- Data quality
- GenAI evaluation
- MLflow
- Databricks Apps
- GitHub

## High-Level Flow

User
↓
Databricks App
↓
Question Router
↓
Schema Intelligence / RAG
↓
LLM
↓
SQL Generation
↓
SQL Validation
↓
Query Execution
↓
Gold Delta Tables
↓
Result Validation
↓
Answer + Visualization
