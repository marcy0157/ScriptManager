import boto3
from botocore.exceptions import NoCredentialsError
import os


def save_results_to_file(base_name, results):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    count = 0
    while True:
        filename = f"{base_name}{count}.txt" if count > 0 else f"{base_name}.txt"
        filepath = os.path.join(results_dir, filename)
        if not os.path.exists(filepath):
            break
        count += 1

    try:
        with open(filepath, 'a') as f:
            for result in results:
                f.write(result + '\n')
        print(f"Results saved in {filepath}")
    except Exception as e:
        print(f"Error writing file: {e}")


def cloud_bucket_scanner():
    print("Cloud Bucket Scanner Tool (AWS S3)")
    bucket_name = input("Enter the bucket name to check: ")

    try:
        s3 = boto3.client('s3')
        response = s3.get_bucket_acl(Bucket=bucket_name)
        grants = response['Grants']
        results = []

        for grant in grants:
            if 'AllUsers' in str(grant['Grantee']):
                result_str = f"Bucket {bucket_name} is publicly accessible!"
                print(result_str)
                results.append(result_str)
            else:
                print(f"Bucket {bucket_name} is not publicly accessible.")
        save_results_to_file("cloud_bucket_scan_results", results)

    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        save_results_to_file("cloud_bucket_scan_error", [result_str])


cloud_bucket_scanner()
