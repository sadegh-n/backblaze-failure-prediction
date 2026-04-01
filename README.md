# Predicting Hard Drive Failure at Scale (AWS & Polars)

An end-to-end cloud data engineering and machine learning pipeline predicting hard drive failures using the 50+ GB Backblaze dataset.

## Project Overview
Predicting hard drive failure is a classic binary classification problem with an extreme twist: **massive class imbalance**. Over 99% of hard drives function perfectly, while less than 1% fail. 

This project bypasses local compute limitations by building a cloud-native pipeline in AWS. It ingests a decade of daily hard drive telemetry (SMART stats), processes the 50 GB dataset out-of-core using Polars, and trains an XGBoost model to predict impending drive deaths.

## Cloud Architecture & Data Flow
To handle the scale of the data efficiently and cost-effectively, this project relies on serverless data transfers and out-of-core memory execution.

1. **Source:** Backblaze B2 Cloud Storage (Apache Iceberg Parquet format).
2. **Transfer:** AWS CloudShell utilizing `rclone` for a direct cloud-to-cloud gigabit transfer (0 local bandwidth used).
3. **Storage:** Amazon S3 (Silver Data Layer).
4. **Compute:** Amazon SageMaker Notebook instance (`ml.t3.medium`).
5. **Processing:** Polars (Lazy API) streaming Parquet files directly from S3, managing schema drift, and handling data filtering without Out-of-Memory (OOM) crashes.

```text
[Backblaze B2] --(rclone / CloudShell)--> [Amazon S3] --(Polars Lazy API)--> [Amazon SageMaker] -> [XGBoost Model]
