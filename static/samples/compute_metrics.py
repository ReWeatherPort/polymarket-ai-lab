import csv
import json

def parse_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def compute_row_metrics(row):
    return {
        "date": row["date"],
        "experiment_type": row.get("experiment_type", "okc_polymarket"),
        "pnl": parse_float(row.get("pnl", "0")),
        "win_rate": parse_float(row.get("win_rate", "0")),
        "max_drawdown": parse_float(row.get("max_drawdown", "0")),
        "source_sheet_row_id": row.get("source_sheet_row_id", ""),
        "notes": row.get("notes", "")
    }

def main(input_csv_path, output_json_path):
    with open(input_csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [compute_row_metrics(r) for r in reader]
    result = rows[-1] if rows else {}
    with open(output_json_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main("input.csv", "output.json")