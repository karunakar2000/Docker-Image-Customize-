from fastapi import FastAPI
import boto3

app = FastAPI()
from fastapi.responses import FileResponse

# Serve index.html at root URL
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/")
def root():
    return {"message": "AWS Docker Dashboard API is running!!!"}

@app.get("/s3")
def list_s3_buckets():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()
    return {"buckets": [b["Name"] for b in buckets.get("Buckets", [])]}

@app.get("/vpcs")
def list_vpcs():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    response = ec2.describe_vpcs()
    vpcs = response.get("Vpcs", [])
    return {"vpcs": [{"VpcId": vpc["VpcId"], "CidrBlock": vpc["CidrBlock"]} for vpc in vpcs]}

@app.get("/ec2")
def list_ec2_instances():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2.describe_instances().get("Reservations", [])
    instances = [
        {
            "InstanceId": i["InstanceId"],
            "State": i["State"]["Name"],
            "InstanceType": i["InstanceType"],
            "PublicIpAddress": i.get("PublicIpAddress")
        }
        for r in reservations for i in r["Instances"]
    ]
    return {"instances": instances}

@app.get("/certs")
def list_certificates():
    acm = boto3.client("acm", region_name="us-east-1")
    certs = acm.list_certificates().get("CertificateSummaryList", [])
    return {"certificates": [{"DomainName": c["DomainName"], "CertificateArn": c["CertificateArn"]} for c in certs]}
