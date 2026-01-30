#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta
import json

# COMMIT #68: CloudTrail boto3 client + lookup_events
def scan_cloudtrail_basic():
    """68: Bas CloudTrail lookup_events API"""
    cloudtrail = boto3.client('cloudtrail', region_name='eu-north-1')
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    response = cloudtrail.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'AccountId', 
                'AttributeValue': '695210052267'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50
    )
    
    events = response['Events']
    print(f"🔍 Found {len(events)} CloudTrail events (7 days)")
    
    for event in events[:5]:  # Visa första 5
        print(f"  📅 {event['EventTime'][:19]} | {event['EventName']}")
    
    return events

if __name__ == "__main__":
    events = scan_cloudtrail_basic()

python3 cloudtrail_analyzer.py
git add cloudtrail_analyzer.py
git commit -m "feat: cloudtrail boto3 client + lookup_events"


