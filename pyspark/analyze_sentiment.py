import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
os.environ['SPARK_HOME'] = '/opt/spark'

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import pandas as pd
from textblob import TextBlob
import subprocess

spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark Session Created!")

posts_pd = pd.read_csv('/tmp/social_posts.csv')
print(f"Loaded {len(posts_pd)} posts!")

def get_sentiment(text):
    if pd.isna(text):
        return 'NEUTRAL', 0.0
    score = TextBlob(str(text)).sentiment.polarity
    if score > 0.1:
        return 'POSITIVE', round(score, 2)
    elif score < -0.1:
        return 'NEGATIVE', round(score, 2)
    else:
        return 'NEUTRAL', round(score, 2)

posts_pd['sentiment'] = posts_pd['post_text'].apply(
    lambda x: get_sentiment(x)[0]
)
posts_pd['sentiment_score'] = posts_pd['post_text'].apply(
    lambda x: get_sentiment(x)[1]
)
print("\n=== SENTIMENT DISTRIBUTION ===")
print(posts_pd['sentiment'].value_counts())

print("\n=== SENTIMENT BY BRAND ===")
print(posts_pd.groupby(['brand','sentiment']).size())

posts_pd.to_csv('/tmp/sentiment_results.csv', index=False)

print("\n=== FULL RESULTS ===")
print(posts_pd[['username','brand','platform','sentiment','sentiment_score']].to_string())

print("\n=== POSITIVE POSTS ===")
positive = posts_pd[posts_pd['sentiment']=='POSITIVE']
print(positive[['username','brand','sentiment_score','post_text']].to_string())

print("\n=== NEGATIVE POSTS ===")
negative = posts_pd[posts_pd['sentiment']=='NEGATIVE']
print(negative[['username','brand','sentiment_score','post_text']].to_string())

print("\nSaving to HDFS...")
subprocess.run([
    "hdfs", "dfs", "-put", "-f",
    "/tmp/sentiment_results.csv",
    "/sentiment/results/"
])

print("Results saved to HDFS!")
print("Sentiment Analysis Complete!")
spark.stop()
