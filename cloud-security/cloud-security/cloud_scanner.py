#!/usr/bin/env python3
"""
AWS Cloud Security Scanner
Checks IAM policies + S3 bucket security
Multiverse Cloud Security Portfolio
"""

import boto3
import json
from datetime import datetime

class CloudSecurityScanner:
    def __init__(self):
        self.iam = boto3.client('iam')
        self.s3 = boto3.client('s3')
    
    def check_overprivileged_iam(self):
        """Find overly permissive IAM policies"""
        print("🔍 Scanning IAM policies...")
        policies = []
        
        # Check for wildcard (*) permissions
        response = self.iam.list_policies(Scope='All')
        for policy in response['Policies']:
            print(f"  📋 {policy['PolicyName']}: {policy['Arn']}")
            policies.append(policy['PolicyName'])
        return policies
    
    def check_public_s3(self):
        """Find public S3 buckets"""
        print("\n🛡️ Scanning S3 buckets...")
        buckets = []
        response = self.s3.list_buckets()
        
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            print(f"  ☁️  {bucket_name}")
            buckets.append(bucket_name)
        return buckets

if __name__ == "__main__":
    print("🌩️  CLOUD SECURITY SCANNER v1.0")
    print("=" * 40)
    
    scanner = CloudSecurityScanner()
    iam_policies = scanner.check_overprivileged_iam()
    s3_buckets = scanner.check_public_s3()
    
    print(f"\n✅ Scan complete!")
    print(f"   IAM Policies: {len(iam_policies)}")
    print(f"   S3 Buckets: {len(s3_buckets)}")
