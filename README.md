# Divvy Bike Share Data Analysis

**Google Data Analytics Professional Certificate - Capstone Project**

Analysis of over 5.4 million bike-sharing trips from the Divvy system, providing insights into usage patterns, user behavior, and operational efficiency.

## Overview

This project examines the Divvy bike-sharing system through comprehensive data analysis, delivering actionable insights for business decision-making. The analysis covers temporal patterns, user segmentation, station utilization, and strategic recommendations.

## Project Structure

```
data-projects/
├── data/
│   └── processed/
│       └── divvy_combined_data.csv    # Cleaned dataset
├── src/
│   ├── divvy_bike_share_report.Rmd    # R Markdown analysis
│   ├── divvy_bike_share_analysis.py   # Python analysis
│   └── divvy_bike_export_analysis.py  # Python export script
├── outputs/
│   ├── kpi_dashboard/                 # Key performance indicators
│   ├── temporal_analysis/             # Time-based patterns
│   ├── user_analysis/                 # User behavior insights
│   ├── station_analysis/              # Station utilization
│   └── additional_insights/           # Additional findings
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

## Quick Start

### Prerequisites

- **R**: R with tidyverse, ggplot2, dplyr, lubridate packages
- **Python**: Python 3.13+ with pandas, matplotlib, seaborn

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/gsmkev/data-projects.git
   cd data-projects
   git checkout google-data-analytics
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install R packages** (if using R):
   ```r
   install.packages(c("tidyverse", "ggplot2", "dplyr", "lubridate",
                     "scales", "gridExtra", "viridis", "ggthemes", "DT",
                     "knitr", "kableExtra"))
   ```

### Execution

#### R Markdown Analysis

```r
# In R/RStudio
rmarkdown::render("src/divvy_bike_share_report.Rmd")
```

#### Python Analysis

```bash
python src/divvy_bike_share_analysis.py
```

#### Export Data to Excel

```bash
python src/divvy_bike_export_analysis.py
```

This script exports all analysis data to an Excel file (`divvy_analysis_data.xlsx`) with separate sheets for each visualization, allowing manual chart creation in Excel. The file includes 13 sheets with clean, formatted data ready for charting.

## Analysis Components

### Key Performance Indicators

- **Daily Trip Efficiency**: Average trips completed per day
- **Member User Distribution**: Percentage of member users
- **Station Utilization**: Average trips per active station
- **User Satisfaction Rate**: Percentage of optimal duration trips (5-60 minutes)

### Temporal Analysis

- **Hourly Patterns**: Intraday usage distribution
- **Daily Patterns**: Weekly usage cycles
- **Monthly Trends**: Seasonal usage patterns
- **User Type Behavior**: Member vs casual user temporal differences

### User Analysis

- **User Type Distribution**: Member vs casual user breakdown
- **Trip Duration Analysis**: Duration patterns by user segment
- **Member Proportion**: Hourly member engagement patterns
- **Behavioral Patterns**: Usage habit identification

### Station Analysis

- **Top Utilization Stations**: Most frequent start and end stations
- **Station Type Classification**: Real vs unknown station analysis
- **Geographic Distribution**: Spatial usage patterns

### Additional Insights

- **Temporal Heatmap**: Hour-day usage intensity visualization
- **Duration Distribution**: Trip length frequency analysis

## Key Findings

### Executive Summary

1. **Peak Usage Patterns**: Clear work commute patterns (7-9 AM, 5-7 PM)
2. **Member Dominance**: Members represent the majority of system usage
3. **Weekend Patterns**: Increased recreational usage on weekends
4. **Station Concentration**: Downtown stations show highest utilization
5. **Duration Patterns**: Members exhibit shorter, more regular trips

### Strategic Recommendations

1. **Fleet Expansion**: Increase bike availability at high-demand stations during peak hours
2. **Membership Conversion**: Target casual users for membership conversion
3. **Distribution Optimization**: Optimize bike placement based on usage patterns
4. **Station Development**: Develop new stations in growth opportunity areas
5. **Dynamic Pricing**: Consider peak-hour pricing strategies

## Generated Visualizations

### KPI Dashboard

- `kpi_strategic.png` - Strategic KPIs dashboard

### Temporal Analysis

- `hourly_analysis.png` - Hourly usage patterns
- `daily_pattern.png` - Weekly usage patterns
- `monthly_analysis.png` - Monthly seasonal patterns

### User Analysis

- `user_distribution.png` - User type distribution
- `duration_comparison.png` - Duration by user type
- `hourly_by_user.png` - Hourly patterns by user type
- `member_proportion.png` - Member engagement patterns

### Station Analysis

- `start_stations.png` - Top start stations
- `end_stations.png` - Top destination stations
- `station_types.png` - Station type distribution

### Additional Insights

- `heatmap.png` - Temporal usage heatmap
- `duration_distribution.png` - Duration frequency

## Data Description

### Dataset Information

- **Source**: Divvy bike-sharing system operational data
- **Records**: Over 5.4 million trip records
- **Coverage**: Multi-year comprehensive dataset
- **Variables**: Trip details, user segmentation, station utilization

### Key Variables

- `ride_id`: Unique trip identifier
- `started_at`/`ended_at`: Trip timestamps
- `trip_duration_minutes`: Trip duration in minutes
- `member_casual`: User type classification
- `start_station_name`/`end_station_name`: Station locations
- `membership_indicator`: Binary membership status

## Technical Implementation

### R Analysis Framework

- **Tidyverse**: Data manipulation and analysis
- **ggplot2**: Statistical plotting
- **R Markdown**: Reproducible reporting

### Python Analysis Framework

- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Statistical visualization
- **NumPy**: Numerical computation

### Output Formats

- **HTML Reports**: Interactive web-based reports
- **PDF Reports**: Print-ready documents
- **PNG Images**: High-resolution chart outputs
- **Excel Data**: Raw data for manual chart creation

## Key Metrics

- **Total Trips**: 5,590,798
- **Member Percentage**: 63.3%
- **Average Duration**: 14.8 minutes
- **Active Stations**: 1,868
- **Daily Efficiency**: 15,293 trips/day

## Support

For technical questions, review the code comments for implementation details and examine the generated visualizations for business insights.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Google Data Analytics Professional Certificate - Capstone Project**  
**Divvy Bike Share Analysis**
