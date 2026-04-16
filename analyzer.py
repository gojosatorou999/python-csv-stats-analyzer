import csv
import sys
import os
from collections import Counter
from statistics import mean, median, stdev

class CSVAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.headers = []
        self.data = []
        self.rows_count = 0
        self.cols_count = 0

    def parse(self):
        """Parse the CSV file and load data into memory."""
        if not os.path.exists(self.filename):
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames
                self.data = list(reader)
                self.rows_count = len(self.data)
                self.cols_count = len(self.headers) if self.headers else 0
        except Exception as e:
            print(f"Error reading CSV: {e}")
            sys.exit(1)

    def _infer_type(self, value):
        """Try to infer the type of a string value."""
        if not value or value.strip() == "":
            return None
        
        # Try Integer
        try:
            int(value)
            return int
        except ValueError:
            pass

        # Try Float
        try:
            float(value)
            return float
        except ValueError:
            pass

        return str

    def get_column_stats(self):
        """Analyze each column and return statistics."""
        stats = {}
        for header in self.headers:
            col_data = [row[header] for row in self.data if row[header] is not None and row[header].strip() != ""]
            
            # Infer the dominant type for the column
            types = [self._infer_type(v) for v in col_data]
            types = [t for t in types if t is not None]
            
            if not types:
                stats[header] = {"type": "empty", "count": 0}
                continue

            most_common_type = Counter(types).most_common(1)[0][0]
            
            col_stats = {
                "type": most_common_type.__name__ if hasattr(most_common_type, "__name__") else "string",
                "count": len(col_data),
                "null_count": self.rows_count - len(col_data)
            }

            if most_common_type in (int, float):
                numeric_values = []
                for v in col_data:
                    try:
                        numeric_values.append(float(v))
                    except ValueError:
                        continue
                
                if numeric_values:
                    col_stats.update({
                        "min": min(numeric_values),
                        "max": max(numeric_values),
                        "mean": round(mean(numeric_values), 2),
                        "median": median(numeric_values),
                        "sum": sum(numeric_values)
                    })
                    if len(numeric_values) > 1:
                        col_stats["std_dev"] = round(stdev(numeric_values), 2)
            else:
                # For strings, get unique counts and most common
                counts = Counter(col_data)
                unique_vals = len(counts)
                most_common = counts.most_common(3)
                col_stats.update({
                    "unique_values": unique_vals,
                    "top_3": most_common
                })

            stats[header] = col_stats
        
        return stats

    def display_report(self):
        """Print a pretty report of the CSV analysis."""
        print("="*50)
        print(f"CSV ANALYSIS REPORT: {self.filename}")
        print("="*50)
        print(f"Total Rows:    {self.rows_count}")
        print(f"Total Columns: {self.cols_count}")
        print("-" * 50)

        stats = self.get_column_stats()
        
        for col, data in stats.items():
            print(f"Column: {col}")
            print(f"  Type:  {data['type']}")
            print(f"  Count: {data['count']} (Nulls: {data['null_count']})")
            
            if data['type'] in ('int', 'float'):
                print(f"  Min/Max:  {data.get('min')} / {data.get('max')}")
                print(f"  Mean:     {data.get('mean')}")
                print(f"  Median:   {data.get('median')}")
                print(f"  Sum:      {data.get('sum')}")
            else:
                print(f"  Unique:   {data.get('unique_values')}")
                top_str = ", ".join([f"'{v}' ({c})" for v, c in data.get('top_3', [])])
                print(f"  Top 3:    {top_str}")
            print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <filename.csv>")
    else:
        analyzer = CSVAnalyzer(sys.argv[1])
        analyzer.parse()
        analyzer.display_report()
