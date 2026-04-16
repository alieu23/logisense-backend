import boto3
import os


region = os.getenv("AWS_DEFAULT_REGION", "us-east-2")

dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table("SentimentResults")