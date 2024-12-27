import boto3
import pandas as pd
import time
from datetime import datetime
from botocore.exceptions import ClientError
from trp import Document

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME

client = boto3.client('textract',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

def upload_to_s3(file_path):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    bucket_name = BUCKET_NAME
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_name = file_path.split('/')[-1]
    sanitized_base_name = base_name.replace(' ', '_')
    file_name = f'{sanitized_base_name}_{date_str}'
    try:
        with open(file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, file_name)
        return bucket_name, file_name
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return None, None

def extract_text_from_image(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
        response = client.detect_document_text(Document={'Bytes': file_bytes})
        lines = [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']
        return lines
    except ClientError as e:
        print(f"AWS Textract error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def extract_text_from_pdf(file_path):
    bucket_name, file_name = upload_to_s3(file_path)
    if not bucket_name or not file_name:
        return None
    
    try:
        response = client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_name
                }
            },
            FeatureTypes=['TABLES', 'FORMS']
        )
        job_id = response['JobId']

        while True:
            response = client.get_document_analysis(JobId=job_id)
            status = response['JobStatus']
            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(5)

        if status == 'FAILED':
            raise Exception("Document analysis failed")

        all_blocks = response['Blocks']
        next_token = response.get('NextToken', None)

        while next_token:
            response = client.get_document_analysis(JobId=job_id, NextToken=next_token)
            all_blocks.extend(response['Blocks'])
            next_token = response.get('NextToken', None)

        response['Blocks'] = all_blocks
        return response

    except ClientError as e:
        print(f"AWS Textract error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def process_textract_response(response):
    try:
        if 'Blocks' not in response:
            raise ValueError("Response does not contain 'Blocks'")

        doc = Document(response)
        lines = [line.text for page in doc.pages for line in page.lines if line.text]
        tables = []
        key_values = {}

        for page in doc.pages:
            for table in page.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text if cell.text else "" for cell in row.cells]
                    table_data.append(row_data)
                df = pd.DataFrame(table_data)
                tables.append(df)

            for field in page.form.fields:
                key = field.key.text if field.key and field.key.text else ""
                value = field.value.text if field.value and field.value.text else ""
                key_values[key] = value

        date = next((line for line in lines if 'Date' in line), None)

        return lines, tables, key_values, date
    except Exception as e:
        print(f"Error processing Textract response: {e}")
        return [], [], {}, None

def main():
    file_path = input("Enter the path to the file: ").strip()

    if file_path.lower().endswith(".pdf"):
        print("Extracting text from PDF...")
        response = extract_text_from_pdf(file_path)
        if response:
            lines, tables, key_values, date = process_textract_response(response)
        else:
            print("Error occurred during document analysis.")
            return
    else:
        print("Extracting text from Image...")
        lines = extract_text_from_image(file_path)
        tables = []
        key_values, date = {}, None

    print("\nExtracted Text:")
    for line in lines:
        print(line)

    if tables:
        print("\nExtracted Tables:")
        for i, table in enumerate(tables):
            print(f"Table {i+1}:")
            print(table)

    if key_values:
        print("\nExtracted Key-Value Pairs:")
        for key, value in key_values.items():
            print(f"{key}: {value}")

    if date:
        print(f"\nDate: {date}")

if __name__ == "__main__":
    main()
