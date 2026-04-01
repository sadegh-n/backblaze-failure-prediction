import boto3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BUCKET_NAME = 'backblaze-afr' 
S3_PREFIX = 'raw/'               

s3_client = boto3.client('s3')

print("Fetching download links from Backblaze...")
url = "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")
zip_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.zip')]

print(f"Found {len(zip_links)} files to transfer. Starting stream to S3...")

for href in zip_links:
    full_url = urljoin(url, href)
    filename = href.split('/')[-1]
    s3_key = f"{S3_PREFIX}{filename}"
    
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"Skipping {filename} - already exists in S3.")
        continue
    except s3_client.exceptions.ClientError:
        pass
        
    print(f"Streaming {filename} to s3://{BUCKET_NAME}/{s3_key} ...")
    
    with requests.get(full_url, stream=True) as r:
        r.raise_for_status()
        
        s3_client.upload_fileobj(
            Fileobj=r.raw, 
            Bucket=BUCKET_NAME, 
            Key=s3_key
        )

print("All raw files successfully streamed to S3!")
