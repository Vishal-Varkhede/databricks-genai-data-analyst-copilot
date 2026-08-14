# Databricks GenAI Data Analyst Copilot

Production-oriented GenAI Data Analyst Copilot built on Databricks using PySpark, Delta Lake, LLMs, RAG and natural-language-to-SQL.

## Project Status

🚧 Under development

## Overview

The Databricks GenAI Data Analyst Copilot is a portfolio project demonstrating modern Data Engineering, GenAI and MLOps practices.

The system transforms raw sales data through a Delta Lake Medallion Architecture and allows users to ask analytical questions using natural language.

Example:

> Which region generated the highest revenue?

The system determines the user's intent, retrieves relevant schema metadata, generates read-only SQL, validates the SQL, executes it against governed analytical tables, and generates a grounded explanation.

## Architecture

```text
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
Databricks SQL
 ↓
Gold Delta Tables
 ↓
Result Validation
 ↓
Answer + Visualization
