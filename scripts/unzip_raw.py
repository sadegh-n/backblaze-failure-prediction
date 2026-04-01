import boto3
import zipfile
import io

s3 = boto3.client('s3')
bucket = 'backblaze-afr' 
raw_prefix = 'raw/'
unzipped_prefix = 'raw-unzipped/'

response = s3.list_objects_v2(Bucket=bucket, Prefix=raw_prefix)
zip_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.zip')]

for zip_key in zip_files:
    print(f"Processing {zip_key}...")
    
    zip_obj = s3.get_object(Bucket=bucket, Key=zip_key)
    buffer = io.BytesIO(zip_obj["Body"].read())
    
    with zipfile.ZipFile(buffer) as z:
        for file_info in z.infolist():
            if file_info.filename.endswith('.csv'):
                print(f"  Extracting {file_info.filename}...")
                
                csv_data = z.read(file_info.filename)
                
                new_key = f"{unzipped_prefix}{file_info.filename}"
                s3.put_object(Bucket=bucket, Key=new_key, Body=csv_data)

print("All files unzipped successfully!")
