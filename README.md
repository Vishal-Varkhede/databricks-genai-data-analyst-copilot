# GenAI Data Analyst Copilot

An end-to-end **GenAI Data Analyst Copilot** built on Databricks that converts natural-language business questions into actionable data insights using **SQL, RAG, and Hybrid SQL + RAG reasoning**.

The project combines modern data engineering, analytics, retrieval-augmented generation, LLM-based answer generation, pipeline orchestration, monitoring, and production validation into a single analytics copilot.

---

## 🚀 Project Overview

The GenAI Data Analyst Copilot allows users to ask questions such as:

> Which region generated the highest revenue?

> What is the discount policy?

> Which region generated the highest revenue and what discount policy applies there?

The system automatically determines how the question should be processed.

### Supported Routes

| Route       | Purpose                                                |
| ----------- | ------------------------------------------------------ |
| SQL         | Structured analytical questions                        |
| RAG         | Questions requiring business documents/policies        |
| Hybrid      | Questions requiring both structured data and documents |
| Unsupported | Questions outside the supported capabilities           |

---

# 🏗️ Architecture

```text
                         USER QUESTION
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Question Classifier │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
             SQL              RAG             HYBRID
              │                │                │
              ▼                ▼                ▼
        SQL Generator     Embedding        Decomposition
              │                │             /       \
              ▼                ▼            /         \
        SQL Validator     Retrieval       SQL         RAG
              │                │            │           │
              ▼                ▼            ▼           ▼
        SQL Executor      RAG Context   SQL Result   RAG Answer
              │                │            │           │
              └────────────────┴────────────┴───────────┘
                               │
                               ▼
                     Final Answer Assembly
                               │
                               ▼
                     Production API Response
```

---

# 📊 Data Engineering Architecture

The data platform follows a layered architecture:

```text
Source Data
    │
    ▼
Bronze
    │
    ▼
Silver
    │
    ▼
Gold
    │
    ▼
GenAI Analytics Layer
```

### Medallion Architecture

```text
Bronze
genai_copilot.bronze.sales
        │
        ▼
Silver
genai_copilot.silver.sales
        │
        ▼
Gold
genai_copilot.gold.region_sales
```

The Gold layer provides analytical data used by the SQL generation and execution pipeline.

---

# 🤖 GenAI Architecture

The GenAI layer contains multiple components.

### Question Classification

The classifier determines whether a question requires:

* SQL
* RAG
* Hybrid processing
* Unsupported handling

### Natural Language → SQL

Business questions are converted into SQL queries using an LLM-based SQL generation pipeline.

Example:

```text
User:
Which region generated the highest revenue?

        ↓

Generated SQL:

SELECT
    region,
    SUM(total_revenue) AS total_revenue
FROM genai_copilot.gold.region_sales
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 10
```

### SQL Validation

Generated SQL is validated before execution to prevent unsafe or unsupported queries.

### SQL Execution

Validated SQL is executed against the Databricks analytical tables.

---

# 📚 RAG Pipeline

The RAG pipeline handles questions requiring business knowledge stored in documents.

The pipeline performs:

```text
Question
   ↓
Embedding Generation
   ↓
Document Retrieval
   ↓
Similarity Ranking
   ↓
Context Construction
   ↓
LLM Answer Generation
   ↓
Grounded Answer + Sources
```

Example document sources include:

```text
discount_policy.txt
product_policy.txt
regional_sales_guidelines.txt
return_policy.txt
```

The generated response includes the relevant document sources to improve traceability.

---

# 🔀 Hybrid SQL + RAG

The Hybrid route combines structured analytics with unstructured business knowledge.

Example:

> Which region generated the highest revenue and what discount policy applies there?

The system decomposes the question into:

```text
SQL Question
Which region generated the highest revenue?

RAG Question
What discount policy applies to that region?
```

The two pipelines execute independently and the results are combined into a final response.

Example result:

```text
Highest revenue region: Middle East
Highest revenue: 1,939,021.50

Discount policy:
The global discount policy applies to that region.
```

---

# ⚙️ Production Pipeline

The production pipeline is orchestrated through Databricks Jobs using Serverless compute.

```text
Databricks Serverless Job
          │
          ▼
02_data_pipeline.py
          │
          ▼
03_rag_pipeline.py
          │
          ▼
04_copilot_pipeline.py
```

The tasks are dependency-aware:

```text
data_pipeline
      ↓
rag_pipeline
      ↓
copilot_pipeline
```

This ensures downstream processing occurs only after the required upstream pipeline succeeds.

---

# 📈 Pipeline Monitoring

The project includes pipeline monitoring and observability capabilities.

Monitoring covers:

* Pipeline execution
* Task status
* Execution failures
* Pipeline dependencies
* End-to-end validation
* Production test results

---

# 🧪 Testing & Validation

The project includes dedicated validation for:

### SQL

```text
PASS - SQL
```

### RAG

```text
PASS - RAG
```

### Hybrid

```text
PASS - HYBRID
```

### Production API

```text
PASS - API
```

### End-to-End

```text
PHASE 22 STATUS: PASS ✓
```

The actual Databricks production Job has successfully executed:

```text
data_pipeline       ✅
      ↓
rag_pipeline        ✅
      ↓
copilot_pipeline    ✅
```

---

# 📁 Project Structure

```text
databricks-genai-data-analyst-copilot/
│
├── 01_setup/
│
├── 02_ingestion/
│
├── 03_transformation/
│
├── 04_gold/
│
├── 05_data_quality/
│
├── 06_genai/
│   ├── 02_question_classifier.py
│   ├── 03_sql_generator.py
│   ├── 04_sql_validator.py
│   └── 05_sql_executor.py
│
├── 07_rag/
│   ├── 04_rag_retrieval.py
│   └── 05_rag_answer_generation.py
│
├── 08_integration/
│   ├── 01_copilot_orchestrator.py
│   ├── 02_evaluation.py
│   ├── 03_production_response.py
│   └── 04_production_hardening.py
│
├── 09_pipeline/
│   ├── 02_data_pipeline.py
│   ├── 03_rag_pipeline.py
│   ├── 04_copilot_pipeline.py
│   ├── 05_pipeline_monitoring.py
│   ├── 06_pipeline_scheduling.py
│   ├── 07_end_to_end_validation.py
│   └── 08_databricks_job_setup.py
│
└── README.md
```

---

# 🛠️ Technology Stack

### Data Engineering

* Databricks
* Apache Spark
* PySpark
* SQL
* Medallion Architecture

### GenAI

* Databricks AI / Foundation Models
* LLM-based SQL generation
* Retrieval-Augmented Generation
* Embeddings
* Hybrid SQL + RAG reasoning

### Data Platform

* Delta tables
* Databricks Serverless
* Databricks Jobs
* Pipeline orchestration

### Development

* Python
* Git
* GitHub
* Jupyter/Databricks notebooks

---

# 🔐 Production Considerations

The project includes several production-oriented controls:

* SQL validation before execution
* Structured pipeline responses
* Error handling
* Execution-time tracking
* Source attribution for RAG responses
* Route validation
* Pipeline dependency management
* End-to-end production validation
* Serverless Job orchestration

---

# 📊 Example Queries

### SQL Question

```text
Which region generated the highest revenue?
```

Result:

```text
Middle East
1,939,021.50
```

### RAG Question

```text
What is the discount policy?
```

The system retrieves the relevant policy documents and generates a grounded answer with source attribution.

### Hybrid Question

```text
Which region generated the highest revenue
and what discount policy applies there?
```

The system combines:

```text
SQL Analytics
      +
RAG Knowledge
      ↓
Final Answer
```

---

# 🎯 Key Engineering Highlights

This project demonstrates practical experience with:

1. End-to-end data engineering
2. Medallion architecture
3. PySpark and Spark SQL
4. Natural-language analytics
5. LLM-powered SQL generation
6. SQL validation and controlled execution
7. Retrieval-Augmented Generation
8. Document embeddings and retrieval
9. Hybrid SQL + RAG workflows
10. Production pipeline orchestration
11. Serverless Databricks Jobs
12. Monitoring and validation
13. API response standardization
14. GitHub-based project management
15. End-to-end production testing

---

# 🚧 Future Improvements

Potential future enhancements include:

* Databricks App / web UI
* Interactive charts and visualizations
* Streaming data support
* Advanced evaluation metrics
* Conversation memory
* Multi-turn analytical conversations
* Improved hybrid question decomposition
* Automated CI/CD
* Automated regression testing
* Role-based access control
* Advanced observability dashboards

---

# 👨‍💻 Author

**Vishal Varkhede**

Data Analyst / Data Engineer focused on:

* Python
* PySpark
* SQL
* Databricks
* Azure
* GenAI
* RAG
* Data Analytics

---

# ⭐ Project Goal

The goal of this project is to demonstrate how modern data engineering and Generative AI can be combined to create a production-oriented **AI Data Analyst Copilot** capable of answering business questions using both structured enterprise data and unstructured business knowledge.
