"""CSV with a header row -> labeled row text -> text for chunking."""

import csv


def load_csv(file_path):
    """Read UTF-8, comma-separated records; the first row contains column names."""
    # Keep column labels with values so an embedding sees 'service: api', not just 'api'.
    # You should understand ----------------------------------------------------->
    rows = []
    with file_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            fields = []
            for column, value in row.items():
                if column is None or value is None:
                    raise ValueError(f"{file_path.name}: row does not match the CSV header.")
                fields.append(f"{column}: {value}")
            rows.append(" | ".join(fields))
    return "\n\n".join(rows)
    # -------------------------------------------------------------------------->
