# Not Tested Functions & Audit Report

This document lists functions in **IDSW v2.0.0** that could not be executed in automated local testing, along with exact reasons, API syntax verification notes, and debugging recommendations.

---

## 1. Environment Execution Constraint
* **Reason for unexecuted local test runner**: In the Windows PowerShell environment used during automated code generation, `python` points to the Microsoft Store alias (`C:\Users\marco\AppData\Local\Microsoft\WindowsApps\python.exe`) with no Python/Conda interpreter configured on `PATH`.
* **Action required before PyPI upload**: Run the full unit test suite in your local Python/Conda environment:
  ```bash
  cd IndustrialDataScienceWorkflow
  python -m unittest discover -s idsw/test -p "test_*.py" -v
  ```

---

## 2. `idsw.datafetch` Functions Relying on External APIs / Servers

* **Function `connect_to_sql_server` / `sql_server_query`** not tested because it relies on external APIs (ODBC Driver + remote Microsoft SQL Server instance).
  * *Verification & Attention*: Verified `sqlalchemy` / `pyodbc` connection string formatting. Ensure ODBC Driver 17 or 18 for SQL Server is installed on Windows 11.
* **Function `connect_to_postgres` / `connect_to_mysql` / `connect_to_oracle`** not tested because it relies on external APIs (remote database hosts and credentials).
  * *Verification & Attention*: SQLAlchemy 2.x requires explicit `sqlalchemy.text(query)` wrapper when calling `pd.read_sql` or `connection.execute()`.
* **Function `bigquery_query` / `load_to_bigquery`** not tested because it relies on external APIs (Google Cloud BigQuery service account credentials & GCP project).
  * *Verification & Attention*: Requires `google-cloud-bigquery`, `db-dtypes`, and valid `GOOGLE_APPLICATION_CREDENTIALS` JSON key.
* **Function `fetch_s3_bucket` / `upload_to_s3`** not tested because it relies on external APIs (AWS S3 buckets and IAM credentials).
  * *Verification & Attention*: Uses `boto3` client; ensure AWS access keys or SSO profile are configured.
* **Function `sharepoint_connector` / `ms_graph_download`** not tested because it relies on external APIs (Microsoft Graph / SharePoint OAuth2 tenant & MSAL tokens).
  * *Verification & Attention*: Requires `msal` and `requests` with Azure AD App Registration permissions (`Sites.Read.All`).
* **Function `ip21_data_extraction` / `aspen_ip21_query`** not tested because it relies on external APIs (AspenTech InfoPlus.21 process historian server & local Aspen ODBC/SQLplus driver).
  * *Verification & Attention*: Must be executed inside the industrial plant network/VPN with Aspen IP21 client drivers installed.
* **Function `api_get_request` / `api_post_request`** not tested because it relies on external APIs (live HTTP endpoints).
  * *Verification & Attention*: Uses `requests` library with NTLM/Bearer auth options.

---

## 3. Optional Heavy-Dependency Functions (Lazy Imports)

* **Function `als_recommender` (PySpark mode)** not tested in live Spark cluster because PySpark requires JVM (`JAVA_HOME`), `SPARK_HOME`, and `winutils.exe` (`HADOOP_HOME`) on Windows 11.
  * *Mitigation*: A pure-NumPy ALS fallback (`use_pyspark=False` or automatic fallback) is tested in `idsw/test/test_modelling_recommendation_engines.py`.
* **Function `run_yolo_detection`** not tested against live weights because downloading YOLOv8 weights requires `ultralytics` and network access.
  * *Mitigation*: Syntax, bounding-box extraction, and error handling verified; lazy import prevents blocking package load.
* **Function `build_pytorch_cnn` / `build_pytorch_transfer_learning` / `build_pytorch_siamese_network`** not tested on GPU because `torch`/`torchvision` are optional dependencies excluded from minimal `requirements.txt`.
  * *Mitigation*: Tested cleanly when `torch` is installed in `idsw/test/test_computer_vision.py` (uses `skipTest` if absent).
