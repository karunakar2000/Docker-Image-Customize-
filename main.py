from fastapi import FastAPI
import boto3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI AWS API is running!"}

@app.get("/s3")
def list_buckets():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()
    return {"buckets": [b["Name"] for b in buckets["Buckets"]]}
