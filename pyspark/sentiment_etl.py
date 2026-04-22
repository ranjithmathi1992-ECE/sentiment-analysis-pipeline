import os
os.environ['PATH'] = '/opt/hd/bin:/opt/hd/sbin:' + os.environ['PATH']
from sqlalchemy import create_engine
import pandas as pd
import subprocess

engine = create_engine('mysql+pymysql://root:root@localhost/sentiment_db')

posts_df = pd.read_sql("SELECT * FROM social_posts", engine)

print(f"Extracted {len(posts_df)} social media posts from MySQL!")
print(posts_df.head())

posts_df.to_csv('/tmp/social_posts.csv', index=False)
print("Saved to temporary CSV!")

subprocess.run(["hdfs", "dfs", "-mkdir", "-p", "/sentiment/raw_posts"])
subprocess.run(["hdfs", "dfs", "-put", "-f", "/tmp/social_posts.csv", "/sentiment/raw_posts/"])

print("Data loaded to HDFS successfully!")

result = subprocess.run(
    ["hdfs", "dfs", "-ls", "/sentiment/raw_posts/"],
    capture_output=True,
    text=True
)
print("HDFS Contents:")
print(result.stdout)
