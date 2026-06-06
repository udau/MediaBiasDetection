import boto3
import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

def verify_dynamodb():
    print("=== DynamoDB Connectivity Diagnostic ===")
    
    # 1. Check Environment Variables
    table_name = os.getenv('NEWS_HISTORY_TABLE', 'NewsClickHistory')
    region = os.getenv('AWS_REGION', 'eu-north-1')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    print(f"Target Table: {table_name}")
    print(f"Region: {region}")
    
    missing_creds = []
    if not access_key: missing_creds.append("AWS_ACCESS_KEY_ID")
    if not secret_key: missing_creds.append("AWS_SECRET_ACCESS_KEY")
    
    if missing_creds:
        print(f"\n[!] WARNING: Missing credentials: {', '.join(missing_creds)}")
        print("Please set these variables in your terminal using:")
        print(f"  set AWS_ACCESS_KEY_ID=your_access_key")
        print(f"  set AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("\nNote: You can find these in the AWS IAM Console under 'Security credentials'.")
    else:
        print("[+] Credentials found in environment.")

    # 2. Attempt Connection
    try:
        print("\nConnecting to DynamoDB...")
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        # 3. Check Table Status
        print(f"Checking table status for '{table_name}'...")
        status = table.table_status
        print(f"[+] SUCCESS: Table status is '{status}'.")
        
        # 4. Try a simple scan (limited to 1 item) to check read permissions
        print("Testing read permissions (Scan)...")
        response = table.scan(Limit=1)
        item_count = len(response.get('Items', []))
        print(f"[+] SUCCESS: Read check passed. Found {item_count} items (limit 1).")
        
        print("\n结论: Your DynamoDB configuration is WORKING correctly!")
        
    except Exception as e:
        print(f"\n[!] ERROR: Could not connect to DynamoDB.")
        print(f"Details: {str(e)}")
        if "AccessDeniedException" in str(e):
            print("\nTip: Check if your IAM user has 'AmazonDynamoDBFullAccess' or similar permissions.")
        elif "ResourceNotFoundException" in str(e):
            print(f"\nTip: The table '{table_name}' does not exist in region '{region}'. Check for typos or verify the region.")

if __name__ == "__main__":
    verify_dynamodb()
