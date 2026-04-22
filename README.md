# 🌐 Social Media Sentiment Analysis Pipeline

## 📌 Project Overview
An end-to-end Big Data NLP pipeline that automatically 
analyzes sentiment of social media posts about brands 
using PySpark and TextBlob. Classifies posts as 
POSITIVE, NEGATIVE or NEUTRAL and generates brand 
reputation reports using Apache Hive.

## 🎯 Business Problem Solved
- Companies receive thousands of social media mentions daily
- Manual sentiment analysis is impossible at scale
- No automated system to track brand reputation
- Cannot identify negative trends before they go viral

## ✅ Solution Built
- Simulates real social media posts for multiple brands
- Stores posts in MySQL database
- Loads data to Hadoop HDFS for big data processing
- Uses PySpark + TextBlob for NLP sentiment analysis
- Classifies each post as POSITIVE NEGATIVE NEUTRAL
- Stores results in Hive Data Warehouse
- Runs automatically daily via Airflow

## 🛠️ Technologies Used
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 | ETL + NLP scripting |
| MySQL | 8.0 | Source database |
| Apache Hadoop | 3.3.6 | Distributed storage |
| Apache Hive | 3.1.3 | Data Warehouse |
| Apache Spark PySpark | 3.2.4 | Sentiment processing |
| TextBlob | Latest | NLP sentiment analysis |
| Apache Airflow | 2.9.0 | Pipeline automation |

## 🏗️ Architecture
MySQL → Python ETL → HDFS → PySpark + TextBlob → Hive → Airflow DAG

## 📊 Key Results
- 20 social media posts analyzed daily
- POSITIVE posts identified per brand
- NEGATIVE posts flagged for action
- Brand reputation score calculated
- Platform wise sentiment breakdown
- Location wise sentiment analysis

## 📁 Project Structure
sentiment_analysis/
├── README.md
├── .gitignore
├── pyspark/
│   ├── sentiment_etl.py
│   └── analyze_sentiment.py
└── airflow/
    └── sentiment_dag.py

## 🚀 How to Run
Step 1 - Start Hadoop:
start-dfs.sh and start-yarn.sh

Step 2 - Create HDFS folders:
hdfs dfs -mkdir -p /sentiment/raw_posts
hdfs dfs -mkdir -p /sentiment/results

Step 3 - Install TextBlob:
pip3 install textblob --break-system-packages
python3 -m textblob.download_corpora

Step 4 - Run ETL:
python3 pyspark/sentiment_etl.py

Step 5 - Run Spark Sentiment Analysis:
spark-submit pyspark/analyze_sentiment.py

Step 6 - Start Airflow:
airflow standalone

Step 7 - Access UI:
http://localhost:8080

## 🎯 Skills Demonstrated
- Natural Language Processing (NLP)
- Sentiment Analysis
- PySpark Big Data Processing
- TextBlob Python Library
- Apache Hive Data Warehouse
- Apache Airflow Automation
- Big Data ETL Pipeline
- Python Programming
- MySQL Database Design
- Hadoop HDFS Storage
- Brand Analytics
- Social Media Analytics
