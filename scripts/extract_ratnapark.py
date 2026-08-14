from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "excel"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "ratnapark"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FILES = {
    2024: RAW_DIR / "aqms_2024.xlsx",
    2025: RAW_DIR / "aqms_2025.xlsx",
}


def extract_ratnapark(year: int, file_path: Path) -> None:
    print(f"\nProcessing {year}...")
    print(f"File: {file_path}")

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    excel = pd.ExcelFile(file_path)

    ratnapark_sheet = next(
        (sheet for sheet in excel.sheet_names if "ratnapark" in sheet.lower()),
        None,
    )

    if ratnapark_sheet is None:
        print("Ratnapark sheet not found.")
        print("Available sheets:")
        for sheet in excel.sheet_names:
            print(f"  - {sheet}")
        return

    print(f"Found sheet: {ratnapark_sheet}")

    df = pd.read_excel(
        file_path,
        sheet_name=ratnapark_sheet,
    )

    print(f"Rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    output_file = OUTPUT_DIR / f"ratnapark_{year}_raw.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    print(f"Saved: {output_file}")


def main() -> None:
    for year, file_path in FILES.items():
        extract_ratnapark(year, file_path)


if __name__ == "__main__":
    main()
