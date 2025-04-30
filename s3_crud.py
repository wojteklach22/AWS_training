import boto3

region = 'eu-central-1'
s3 = boto3.resource('s3', region_name=region)
bucket_name = 'new-test-bucket-1234-wojtek-new-one'

all_buckets = [bucket.name for bucket in s3.buckets.all()]
if bucket_name not in all_buckets:
    print(f'{bucket_name} bucket does not exist. \n Creating now...')

    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )

    print(f'{bucket_name} bucket has been created.')
else:
    print(f'{bucket_name} bucket already exists. No need to create new one.')

# UPLOAD
file_1: str = 'file_1.txt'
file_2: str = 'file_2.txt'

s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)
s3.Bucket(bucket_name).upload_file(Filename=file_2, Key=file_2)

# READ and print the file from the bucket
obj_1 = s3.Object(bucket_name, file_1)
obj_2 = s3.Object(bucket_name, file_2)

body_1 = obj_1.get()['Body'].read()
print(body_1)

body_2 = obj_2.get()['Body'].read()
print(body_2)

# UPDATE file_1 with content from file_2

s3.Object(bucket_name, file_1).put(Body=open(file_2, 'rb'))
# Check if works
obj_1 = s3.Object(bucket_name, file_1)
body_1 = obj_1.get()['Body'].read()
print(body_1)

# DELETE the file from the bucket
s3.Object(bucket_name, file_1).delete()

# DELETE the bucket ( bucket should be empty)
bucket = s3.Bucket(bucket_name)
bucket.delete()
