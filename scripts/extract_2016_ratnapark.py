from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "excel"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "ratnapark"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


OLD_FILE = RAW_DIR / "aqms_2016_2020.xlsx"

NEW_FILES = {
    2024: RAW_DIR / "aqms_2024.xlsx",
    2025: RAW_DIR / "aqms_2025.xlsx",
}


def extract_old_ratnapark() -> None:
    """
    Extract Ratnapark data from the 2016–2020 workbook.

    The workbook stores each pollutant in a separate section.
    Each section contains 2016–2020 data side-by-side.

    No missing-value handling is performed.
    """

    print("\nProcessing 2016–2020...")

    if not OLD_FILE.exists():
        print(f"File not found: {OLD_FILE}")
        return

    df = pd.read_excel(
        OLD_FILE,
        sheet_name="Ratnapark",
        header=None,
    )

    print(f"Original shape: {df.shape}")

    # Starting row of each pollutant section.
    sections = {
        "pm1": 0,
        "pm2_5": 370,
        "pm10": 740,
        "tsp": 1111,
    }

    years = [2016, 2017, 2018, 2019, 2020]

    pollutant_data = {}

    for pollutant, start_row in sections.items():
        print(f"Extracting {pollutant}...")

        section = df.iloc[start_row:]

        year_data = []

        for year_index, year in enumerate(years):
            date_column = year_index * 2
            value_column = date_column + 1

            dates = section.iloc[:, date_column]
            values = section.iloc[:, value_column]

            temp = pd.DataFrame(
                {
                    "date": dates,
                    pollutant: values,
                }
            )

            # Remove only rows that are outside the actual
            # data section/header. We are NOT removing
            # missing measurements.
            temp = temp[
                pd.to_datetime(
                    temp["date"],
                    errors="coerce",
                ).notna()
            ].copy()

            temp["date"] = pd.to_datetime(
                temp["date"],
                errors="coerce",
            )

            temp["year"] = year

            year_data.append(temp)

        pollutant_df = pd.concat(
            year_data,
            ignore_index=True,
        )

        pollutant_data[pollutant] = pollutant_df

        print(f"  {pollutant}: {len(pollutant_df)} rows")

    # Start with PM1 dates and merge the other pollutants.
    result = pollutant_data["pm1"]

    for pollutant in ["pm2_5", "pm10", "tsp"]:
        result = result.merge(
            pollutant_data[pollutant][["date", pollutant]],
            on="date",
            how="outer",
        )

    result = result.sort_values("date").reset_index(drop=True)

    # Keep year explicitly.
    result["year"] = result["date"].dt.year

    output_file = OUTPUT_DIR / "ratnapark_2016_2020_raw.csv"

    result.to_csv(
        output_file,
        index=False,
    )

    print(f"Final shape: {result.shape}")
    print(f"Columns: {result.columns.tolist()}")
    print(f"Saved: {output_file}")


def extract_new_ratnapark(
    year: int,
    file_path: Path,
) -> None:
    """
    Extract Ratnapark from the 2024/2025 workbook.

    No missing-value handling is performed.
    """

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
    extract_old_ratnapark()

    for year, file_path in NEW_FILES.items():
        extract_new_ratnapark(
            year,
            file_path,
        )


if __name__ == "__main__":
    main()
