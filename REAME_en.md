# Portfolio Visualizer for Securities Assets  
証券資産の抽出・整形・可視化ツール

This project extracts, cleans, and visualizes investment data from SBI Securities CSV files, focusing on mutual funds and stocks. It analyzes asset transitions by account type and visualizes fund performance over time.

## Features

- Handles "dirty" CSV structures with multiple sections, blank lines, and inconsistent columns
- Extracts and aggregates assets by account type (Taxable / NISA: Accumulation / Growth)
- Visualizes mutual fund value transitions using stacked bar charts
- Supports multiple CSV files across different dates for time-series analysis

## Data Structure

```text
data/
├── portfolio_20230925.csv
├── portfolio_20231025.csv
└── portfolio_20231125.csv
```

## Technologies Used
- Python 3.x
- pandas: for CSV loading, cleaning, and aggregation
- plotly: for interactive visualization (stacked bar chart)

## How to Run
1. Place multiple CSV files into the data/ folder
(e.g., portfolio_20230925.csv, portfolio_20231025.csv, etc.)
2. Run the script:

```bash
python main.py
```

## Output Example
- graphs/fund_distribution_over_time.png
- graphs/fund_distribution_over_time.html


## Differentiators
- Robust handling of messy CSV formats with multiple sections and inconsistent layouts
- Automatic filtering and classification by account type and asset category
- Aggregates mutual fund data by fund name and date
- Time-series visualization of portfolio changes
- Practical structure aligned with real-world asset management workflows

## Author
GitHub Username: @nori-tty
This project was created for portfolio publication on CrowdWorks, with support from Microsoft Copilot. Copilot was used for technical guidance and structural refinement during development.

## License
This project is released under the MIT License.
Copyright (c) 2025 nori-tty


## Disclaimer
- This project uses dummy data and does not contain any actual account information
- The sample CSV files are anonymized and only replicate the structural format of SBI Securities exports
