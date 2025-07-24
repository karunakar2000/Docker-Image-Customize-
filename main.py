from fastapi import FastAPI
from fastapi.responses import FileResponse
import boto3

app = FastAPI()

# Serve index.html at root URL
@app.get("/")
def read_index():
    return FileResponse("index.html")

# EC2 endpoint
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

# S3 endpoint
@app.get("/s3")
def list_s3_buckets():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()
    return {"buckets": [b["Name"] for b in buckets.get("Buckets", [])]}

# VPCs endpoint
@app.get("/vpcs")
def list_vpcs():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    response = ec2.describe_vpcs()
    vpcs = response.get("Vpcs", [])
    return {"vpcs": [{"VpcId": vpc["VpcId"], "CidrBlock": vpc["CidrBlock"]} for vpc in vpcs]}

# ACM Certificates endpoint
@app.get("/certs")
def list_certificates():
    acm = boto3.client("acm", region_name="us-east-1")
    certs = acm.list_certificates().get("CertificateSummaryList", [])
    return {
        "certificates": [
            {
                "DomainName": c["DomainName"],
                "CertificateArn": c["CertificateArn"]
            }
            for c in certs
        ]
    }
