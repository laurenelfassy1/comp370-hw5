#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(
        description="Count 311 complaints per borough in a given date range"
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", help="Optional output CSV file")
    return parser.parse_args()

def main():
    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    counts = defaultdict(int)

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Match EXACT column names in your CSV
                created = datetime.strptime(row["Created Date"][:10], "%Y-%m-%d")
            except Exception:
                continue
            if start <= created <= end:
                complaint = row["Complaint Type"]
                borough = row["Borough"]
                counts[(complaint, borough)] += 1

    output_lines = ["complaint type,borough,count"]
    for (complaint, borough), count in counts.items():
        output_lines.append(f"{complaint},{borough},{count}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            out.write("\n".join(output_lines))
    else:
        print("\n".join(output_lines))

if __name__ == "__main__":
    main()

