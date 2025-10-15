#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Define directories for input data and output graphs
DATA_DIR: Path = Path("data")
GRAPH_DIR: Path = Path("graphs")

def list_csv_files() -> List[Path]:
    """
    Scan the data directory and return a sorted list of CSV files.
    Each file is expected to follow the naming pattern: portfolio_YYYYMMDD.csv
    """
    return sorted(list(DATA_DIR.glob("*.csv")))

def parse_csv(filepath: Path) -> List[List[str]]:
    """
    Read a CSV file and split it into logical sections.
    Sections are separated by blank lines and contain grouped asset data.
    Returns a list of sections, each as a list of strings.
    """
    with filepath.open(encoding="utf-8") as f:
        lines = f.readlines()

    sections: List[List[str]] = []
    current_section: List[str] = []

    for line in lines:
        if line.strip() == "":
            # Blank line indicates end of a section
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            current_section.append(line.strip())

    # Append the last section if not already added
    if current_section:
        sections.append(current_section)

    return sections

def extract_fund_data(sections: List[List[str]], date_str: str) -> List[Dict[str, object]]:
    """
    Extract mutual fund data from parsed sections.
    Filters out summary sections ending with '合計'.
    Returns a list of dictionaries with date, fund name, and evaluation amount.
    """
    fund_rows: List[Dict[str, object]] = []

    for section in sections:
        # Target only mutual fund sections, excluding totals
        if section[0].startswith("投資信託（金額/") and not section[0].endswith("合計"):
            for row in section[2:]:  # Skip header rows
                values = row.split(",")
                try:
                    fund_name = values[0]
                    eval_amount = int(values[6])  # Evaluation amount column
                    fund_rows.append({
                        "date": date_str,
                        "fund": fund_name,
                        "eval_amount": eval_amount
                    })
                except (IndexError, ValueError):
                    # Skip malformed or incomplete rows
                    continue

    return fund_rows

def aggregate_fund_data() -> pd.DataFrame:
    """
    Aggregate mutual fund data across all CSV files.
    Converts date strings to 'YYYY/MM/DD' format for readability.
    Returns a pandas DataFrame with columns: date, fund, eval_amount.
    """
    all_data: List[Dict[str, object]] = []

    for filename in list_csv_files():
        # Extract date from filename and format it
        date_str = filename.stem.replace("portfolio_", "")
        date_str = datetime.strptime(date_str, "%Y%m%d").strftime("%Y/%m/%d")

        # Parse and extract fund data
        sections = parse_csv(filename)
        fund_data = extract_fund_data(sections, date_str)
        all_data.extend(fund_data)

    return pd.DataFrame(all_data)

def plot_fund_distribution(df: pd.DataFrame) -> None:
    """
    Create a stacked bar chart showing fund evaluation amounts over time.
    Uses plotly for interactive visualization.
    """
    # Group by date and fund, then reshape for plotting
    pivot = (
        df.groupby(["date", "fund"])["eval_amount"]
        .sum()
        .unstack(fill_value=0)
    )

    fig = go.Figure()

    # Add each fund as a stacked bar trace
    for fund in pivot.columns:
        fig.add_trace(go.Bar(
            name=fund,
            x=pivot.index,
            y=pivot[fund]
        ))

    # Configure layout and axis labels
    fig.update_layout(
        barmode='stack',
        title="Trend of Fund Valuation",
        xaxis_title="Date",
        yaxis_title="Fund Valuation (JPY)",
        template="plotly_white"
    )

    fig.show()  # Display in JupyterLab

    # Optional: export to image or HTML
    # fig.write_image(GRAPH_DIR / "fund_distribution_over_time.png")
    # fig.write_html(GRAPH_DIR / "fund_distribution_over_time.html")

if __name__ == "__main__":
    # Load and visualize aggregated fund data
    df = aggregate_fund_data()
    plot_fund_distribution(df)


