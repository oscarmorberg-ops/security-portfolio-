#!/usr/bin/env python3
"""
AWS Config Scanner - Multiverse Cloud Security Portfolio
"""
import boto3

def scan_users():
    iam = boto3.client('iam')
    print("AWS IAM Security Scan")
    print("-" * 30)
    
    users = [u for u in iam.list_users()['Users'] if u['UserName'] != 'root']
    print(f"Total IAM users (exkl root): {len(users)}")
    
    no_mfa_users = []
    key_users = []
    
    for user in users:
        mfa = iam.list_mfa_devices(UserName=user['UserName'])
        if len(mfa['MFADevices']) == 0:
            no_mfa_users.append(user['UserName'])
        
        keys = iam.list_access_keys(UserName=user['UserName'])
        if len(keys['AccessKeyMetadata']) > 0:
            key_users.append(user['UserName'])
    
    print(f"Users utan MFA: {len(no_mfa_users)}")
    for user in no_mfa_users:
        print(f"  MISSING MFA: {user}")
    
    print(f"Users med access keys: {len(key_users)}")
    for user in key_users:
        print(f"  HAS KEYS: {user}")

if __name__ == "__main__":
    scan_users()
