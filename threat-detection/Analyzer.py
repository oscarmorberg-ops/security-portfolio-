#!/usr/bin/env python3
"""
🐳 Docker Trivy Vulnerability Analyzer v1.0
Cloud Security Engineer portfolio project
"""
import subprocess
import sys
from datetime import datetime
import json
import os


class DockerTrivyAnalyzer:
    def __init__(self):
        self.results_file = "trivy-results.json"

    def scan_image(self, image_name):
        """Scan Docker image med Trivy"""
        print(f"🔍 Scanning {image_name}...")
        cmd = ["docker", "run", "--rm", "aquasec/trivy:latest", "image", image_name]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("DEBUG: Trivy return code:", result.returncode)
            print("DEBUG: Trivy output:", result.stdout[:500])
            if result.stderr:
                print("DEBUG: Trivy error:", result.stderr)
            return self.parse_trivy_output(result.stdout)
        except subprocess.TimeoutExpired:
            print("⏰ Scan timeout!")
            return None

    def parse_trivy_output(self, output):
        """Parse Trivy JSON output"""
        lines = output.split('\n')
        vulnerabilities = []

        for line in lines:
            if 'CRITICAL' in line or 'HIGH' in line:
                vulns = line.split('|')
                if len(vulns) >= 6:
                    vulnerabilities.append({
                        'severity': vulns[1].strip(),
                        'package': vulns[3].strip(),
                        'version': vulns[4].strip(),
                        'vulnerability': vulns[2].strip()
                    })

        return vulnerabilities

    def save_results(self, image_name, vulns):
        """Spara results till JSON"""
        result = {
            'scan_date': datetime.now().isoformat(),
            'image': image_name,
            'critical_count': len([v for v in vulns if v['severity'] == 'CRITICAL']),
            'high_count': len([v for v in vulns if v['severity'] == 'HIGH']),
            'vulnerabilities': vulns
        }

        with open(self.results_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Results saved: {self.results_file}")

    def print_summary(self, vulns):
        """Skriv ut executive summary"""
        critical = len([v for v in vulns if v['severity'] == 'CRITICAL'])
        high = len([v for v in vulns if v['severity'] == 'HIGH'])

        print("\n" + "=" * 60)
        print("🚨 SECURITY ASSESSMENT SUMMARY")
        print("=" * 60)
        print(f"🔴 CRITICAL: {critical}")
        print(f"🟡 HIGH:     {high}")
        print(f"🟢 LOW:      N/A")
        print("=" * 60)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyzer.py <docker-image>")
        print("Example: python3 analyzer.py nginx:alpine")
        sys.exit(1)

    image = sys.argv[1]
    analyzer = DockerTrivyAnalyzer()

    vulns = analyzer.scan_image(image)
    if vulns:
        analyzer.print_summary(vulns)
        analyzer.save_results(image, vulns)
    else:
        print("❌ No vulnerabilities found or scan failed")
        analyzer.save_results(image, vulns)


if __name__ == "__main__":
    main()
