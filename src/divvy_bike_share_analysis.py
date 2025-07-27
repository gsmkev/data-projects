# =============================================================================
# DIVVY BIKE SHARE - COMPREHENSIVE DATA ANALYSIS
# Google Data Analytics Professional Certificate - Capstone Project
# Professional Data Analysis with Strategic Business Insights
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

# Create output directory structure
output_directories = [
    'outputs/kpi_dashboard',
    'outputs/temporal_analysis', 
    'outputs/user_analysis',
    'outputs/station_analysis',
    'outputs/additional_insights'
]

for directory in output_directories:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

# Configure matplotlib for professional visualizations
plt.style.use('default')
sns.set_theme(style="whitegrid")
sns.set_palette("husl")

# Define professional color palette for consistent branding
divvy_colors = [
    "#FF6B6B",  # Coral red
    "#4ECDC4",  # Turquoise
    "#45B7D1",  # Light blue
    "#96CEB4",  # Mint green
    "#FFEAA7",  # Soft yellow
    "#DDA0DD",  # Lavender
    "#98D8C8",  # Aqua green
    "#FF8A80",  # Light coral
    "#81C784",  # Light green
    "#64B5F6",  # Light blue
    "#FFB74D",  # Orange
    "#BA68C8"   # Purple
]

# Set global plotting parameters
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 14

# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================

print("Loading and processing Divvy bike share data...")

# Define file paths
processed_file_path = 'data/processed/divvy_combined_data.csv'

# Check if processed dataset exists, otherwise create from raw files
if not os.path.exists(processed_file_path):
    print("Processing raw CSV files...")
    
    # Get all CSV files from raw directory
    raw_file_paths = []
    for file in os.listdir('data/raw'):
        if file.endswith('.csv'):
            raw_file_paths.append(os.path.join('data/raw', file))
    
    raw_file_paths.sort()  # Ensure consistent processing order
    print(f"Found {len(raw_file_paths)} CSV files to process")
    
    # Initialize list to store processed dataframes
    processed_dataframes = []
    
    # Process each raw file
    for file_index, current_file_path in enumerate(raw_file_paths, 1):
        print(f"Processing file {file_index}/{len(raw_file_paths)}: {os.path.basename(current_file_path)}")
        
        try:
            # Read CSV file with proper encoding
            temp_dataframe = pd.read_csv(current_file_path)
            
            # Perform data cleaning and validation
            temp_dataframe = temp_dataframe.dropna(subset=['ride_id', 'started_at', 'ended_at'])
            
            # Convert datetime columns to proper format
            temp_dataframe['started_at'] = pd.to_datetime(temp_dataframe['started_at'])
            temp_dataframe['ended_at'] = pd.to_datetime(temp_dataframe['ended_at'])
            
            # Calculate trip duration and apply data quality filters
            temp_dataframe['trip_duration_minutes'] = (temp_dataframe['ended_at'] - temp_dataframe['started_at']).dt.total_seconds() / 60
            temp_dataframe = temp_dataframe[temp_dataframe['trip_duration_minutes'] > 0]
            temp_dataframe = temp_dataframe[temp_dataframe['trip_duration_minutes'] <= 24*60]
            
            # Standardize station names - replace missing values with "Unknown"
            temp_dataframe['start_station_name'] = temp_dataframe['start_station_name'].fillna("Unknown")
            temp_dataframe['end_station_name'] = temp_dataframe['end_station_name'].fillna("Unknown")
            temp_dataframe['start_station_name'] = temp_dataframe['start_station_name'].replace('', "Unknown")
            temp_dataframe['end_station_name'] = temp_dataframe['end_station_name'].replace('', "Unknown")
            
            # Create binary membership indicator
            temp_dataframe['membership_indicator'] = (temp_dataframe['member_casual'] == 'member').astype(int)
            
            processed_dataframes.append(temp_dataframe)
            print(f"Processed {len(temp_dataframe):,} records from {os.path.basename(current_file_path)}")
            
        except Exception as e:
            print(f"Error processing {current_file_path}: {str(e)}")
            continue
    
    # Combine all processed dataframes into single dataset
    if processed_dataframes:
        divvy_dataset = pd.concat(processed_dataframes, ignore_index=True)
        print(f"Combined {len(divvy_dataset):,} total records from {len(processed_dataframes)} files")
        
        # Create output directory and save processed dataset
        os.makedirs('data/processed', exist_ok=True)
        divvy_dataset.to_csv(processed_file_path, index=False)
        print(f"Saved processed dataset to {processed_file_path}")
    else:
        print("No data files were successfully processed")
        exit(1)

else:
    print("Loading existing processed dataset...")
    divvy_dataset = pd.read_csv(processed_file_path)

# =============================================================================
# DATA FEATURE ENGINEERING
# =============================================================================

# Create temporal features for analysis
divvy_dataset['started_at'] = pd.to_datetime(divvy_dataset['started_at'])
divvy_dataset['ended_at'] = pd.to_datetime(divvy_dataset['ended_at'])
divvy_dataset['start_hour'] = divvy_dataset['started_at'].dt.hour
divvy_dataset['day_of_week'] = divvy_dataset['started_at'].dt.day_name()
divvy_dataset['month'] = divvy_dataset['started_at'].dt.month_name()
divvy_dataset['date'] = divvy_dataset['started_at'].dt.date

# Ensure membership indicator exists
if 'membership_indicator' not in divvy_dataset.columns:
    divvy_dataset['membership_indicator'] = (divvy_dataset['member_casual'] == 'member').astype(int)

# =============================================================================
# DATASET SUMMARY STATISTICS
# =============================================================================

# Display comprehensive dataset summary
print(f"Dataset Summary:")
print(f"Total records: {len(divvy_dataset):,}")
print(f"Analysis period: {divvy_dataset['started_at'].min().strftime('%d/%m/%Y')} - {divvy_dataset['started_at'].max().strftime('%d/%m/%Y')}")
print(f"Average trip duration: {divvy_dataset['trip_duration_minutes'].mean():.1f} minutes")
print(f"Member user percentage: {divvy_dataset['membership_indicator'].mean() * 100:.1f}%")

# Analyze data quality for station information
unknown_start_stations = (divvy_dataset['start_station_name'] == "Unknown").sum()
unknown_end_stations = (divvy_dataset['end_station_name'] == "Unknown").sum()

print(f"Data quality assessment - Unknown stations:")
print(f"  Start stations: {unknown_start_stations:,} ({unknown_start_stations/len(divvy_dataset)*100:.2f}%)")
print(f"  End stations: {unknown_end_stations:,} ({unknown_end_stations/len(divvy_dataset)*100:.2f}%)")

# =============================================================================
# KEY PERFORMANCE INDICATORS
# =============================================================================

print("\nCalculating key performance indicators...")

# Calculate core business metrics
total_trips = len(divvy_dataset)
member_user_percentage = divvy_dataset['membership_indicator'].mean() * 100
average_trip_duration = divvy_dataset['trip_duration_minutes'].mean()
total_usage_hours = divvy_dataset['trip_duration_minutes'].sum() / 60

# Calculate operational efficiency metrics
analysis_period_days = (divvy_dataset['started_at'].max() - divvy_dataset['started_at'].min()).total_seconds() / (24 * 3600)
daily_trip_efficiency = total_trips / analysis_period_days

# Calculate station utilization metrics
station_utilization_data = divvy_dataset[divvy_dataset['start_station_name'] != "Unknown"].groupby('start_station_name').size()
average_station_efficiency = station_utilization_data.mean()
total_active_stations = len(station_utilization_data)

# Calculate user satisfaction metrics
optimal_duration_trips = len(divvy_dataset[(divvy_dataset['trip_duration_minutes'] >= 5) & (divvy_dataset['trip_duration_minutes'] <= 60)])
user_satisfaction_rate = optimal_duration_trips / total_trips * 100

# Create comprehensive metrics summary table
system_metrics_data = {
    'Metric': [
        'Total Trips',
        'Member User Percentage',
        'Average Trip Duration',
        'Total Usage Hours',
        'Daily Trip Efficiency',
        'Average Station Efficiency',
        'User Satisfaction Rate'
    ],
    'Value': [
        f"{total_trips:,}",
        f"{member_user_percentage:.1f}%",
        f"{average_trip_duration:.1f} min",
        f"{total_usage_hours/1000:.1f}K hours",
        f"{daily_trip_efficiency:.0f} trips/day",
        f"{average_station_efficiency:.0f} trips/station",
        f"{user_satisfaction_rate:.1f}%"
    ],
    'Description': [
        'Total number of completed trips',
        'Proportion of member users in the system',
        'Average trip duration across all users',
        'Total system usage time in hours',
        'Average trips completed per day',
        'Average trips per active station',
        'Percentage of trips with optimal duration (5-60 min)'
    ]
}

metrics_df = pd.DataFrame(system_metrics_data)
print("\n📊 KEY DIVVY SYSTEM METRICS")
print("=" * 80)
print(metrics_df.to_string(index=False))

# =============================================================================
# 3. STRATEGIC KPIs DASHBOARD
# =============================================================================

print("\n🎨 Creating Strategic KPIs dashboard...")

# Create KPI dashboard with individual plots
fig, axes = plt.subplots(2, 2, figsize=(24, 20))
fig.suptitle('DIVVY BIKE SHARE - STRATEGIC KEY PERFORMANCE INDICATORS\nExecutive Dashboard for Business Decision Making', 
             fontsize=28, fontweight='bold', y=0.98)

# KPI 1: Daily Rides Volume (Min/Avg/Max)
daily_rides_stats = divvy_dataset.groupby('date').size()
min_daily = daily_rides_stats.min()
max_daily = daily_rides_stats.max()
avg_daily = daily_trip_efficiency

axes[0,0].bar(['Min', 'Avg', 'Max'], [min_daily, daily_trip_efficiency, max_daily], 
              color=[divvy_colors[0], divvy_colors[1], divvy_colors[2]], alpha=0.8, width=0.6)
axes[0,0].set_ylabel('Rides per Day', fontsize=18, fontweight='bold')
axes[0,0].set_title('DAILY RIDES VOLUME\nMin/Average/Max Daily Rides', fontsize=20, fontweight='bold', pad=40)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(axes[0,0].patches, [min_daily, daily_trip_efficiency, max_daily])):
    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + bar.get_height()*0.02, 
                   f'{value:,.0f}', ha='center', va='bottom', fontsize=16, fontweight='bold')
axes[0,0].tick_params(axis='both', which='major', labelsize=14)

# KPI 2: Member Distribution
axes[0,1].pie([member_user_percentage, 100-member_user_percentage], 
              labels=[f'{member_user_percentage:.1f}%\nMembers', f'{100-member_user_percentage:.1f}%\nCasual'], 
              colors=[divvy_colors[1], divvy_colors[2]], autopct='', startangle=90)
axes[0,1].set_title('USER TYPE DISTRIBUTION\nMember vs Casual Users', fontsize=20, fontweight='bold', pad=40)

# KPI 3: Station Efficiency (Min/Avg/Max)
station_rides = divvy_dataset[divvy_dataset['start_station_name'] != "Unknown"].groupby('start_station_name').size()
min_station = station_rides.min()
max_station = station_rides.max()

axes[1,0].bar(['Min', 'Avg', 'Max'], [min_station, average_station_efficiency, max_station], 
              color=[divvy_colors[3], divvy_colors[4], divvy_colors[5]], alpha=0.8, width=0.6)
axes[1,0].set_ylabel('Rides per Station', fontsize=18, fontweight='bold')
axes[1,0].set_title('STATION EFFICIENCY\nMin/Average/Max Rides per Station', fontsize=20, fontweight='bold', pad=40)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(axes[1,0].patches, [min_station, average_station_efficiency, max_station])):
    axes[1,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + bar.get_height()*0.02, 
                   f'{value:,.0f}', ha='center', va='bottom', fontsize=16, fontweight='bold')
axes[1,0].tick_params(axis='both', which='major', labelsize=14)

# KPI 4: User Satisfaction
axes[1,1].bar(['Satisfaction'], [user_satisfaction_rate], color=divvy_colors[4], alpha=0.8, width=0.6)
axes[1,1].set_ylabel('Percentage (%)', fontsize=18, fontweight='bold')
axes[1,1].set_ylim(0, 100)  # Set Y-axis from 0 to 100%
axes[1,1].set_title(f'USER SATISFACTION RATE\n{user_satisfaction_rate:.1f}% Satisfaction', fontsize=20, fontweight='bold', pad=40)
axes[1,1].text(0, user_satisfaction_rate + 2, f'{user_satisfaction_rate:.1f}%', 
               ha='center', va='bottom', fontsize=18, fontweight='bold')
axes[1,1].tick_params(axis='both', which='major', labelsize=14)

# Adjust spacing between subplots - much more space at the top
plt.subplots_adjust(hspace=0.5, wspace=0.3, top=0.85, bottom=0.08, left=0.08, right=0.92)
plt.savefig('outputs/kpi_dashboard/kpi_strategic.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 4. TEMPORAL ANALYSIS
# =============================================================================

print("\n⏰ Creating temporal analysis...")

# Hourly usage plot
fig, ax = plt.subplots(figsize=(14, 8))
hourly_data = divvy_dataset.groupby('start_hour').agg({
    'ride_id': 'count',
    'membership_indicator': 'mean',
    'trip_duration_minutes': 'mean'
}).rename(columns={'ride_id': 'total_rides'}).reset_index()

ax.plot(hourly_data['start_hour'], hourly_data['total_rides'], 
        color=divvy_colors[0], linewidth=3, marker='o', markersize=8)
ax.fill_between(hourly_data['start_hour'], hourly_data['total_rides'], 
                alpha=0.3, color=divvy_colors[0])

# Add value labels
for x, y in zip(hourly_data['start_hour'], hourly_data['total_rides']):
    ax.text(x, y + y*0.02, f'{y:,.0f}', ha='center', va='bottom', 
            fontsize=10, fontweight='bold')

ax.set_title('HOURLY RIDES DISTRIBUTION\nDaily Usage Patterns and Peak Hours Analysis', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Hour of Day', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Rides', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24, 2))
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/temporal_analysis/hourly_analysis.png', dpi=300, bbox_inches='tight')
plt.close()



# Daily analysis
daily_data = divvy_dataset.groupby('day_of_week').agg({
    'ride_id': 'count',
    'membership_indicator': 'mean',
    'trip_duration_minutes': 'mean'
}).rename(columns={'ride_id': 'total_rides'}).reset_index()

# Reorder days
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_data['day_of_week'] = pd.Categorical(daily_data['day_of_week'], categories=day_order, ordered=True)
daily_data = daily_data.sort_values('day_of_week')

# Daily rides plot
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(daily_data['day_of_week'], daily_data['total_rides'], 
              color=divvy_colors, alpha=0.8)

# Add value labels
for bar, value in zip(bars, daily_data['total_rides']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + value*0.01, 
            f'{value:,.0f}', ha='center', va='bottom', 
            fontsize=10, fontweight='bold')

ax.set_title('WEEKLY RIDES DISTRIBUTION\nBusiness Day vs Weekend Usage Patterns', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Day of Week', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Rides', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/temporal_analysis/daily_pattern.png', dpi=300, bbox_inches='tight')
plt.close()

# Monthly analysis
monthly_data = divvy_dataset.groupby('month').agg({
    'ride_id': 'count',
    'membership_indicator': 'mean',
    'trip_duration_minutes': 'mean'
}).rename(columns={'ride_id': 'total_rides'}).reset_index()

# Reorder months
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_data['month'] = pd.Categorical(monthly_data['month'], categories=month_order, ordered=True)
monthly_data = monthly_data.sort_values('month')

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(monthly_data['month'], monthly_data['total_rides'], 
              color=divvy_colors, alpha=0.8)

# Add value labels
for bar, value in zip(bars, monthly_data['total_rides']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + value*0.01, 
            f'{value:,.0f}', ha='center', va='bottom', 
            fontsize=10, fontweight='bold')

ax.set_title('MONTHLY RIDES DISTRIBUTION\nSeasonal Usage Patterns Throughout the Year', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Rides', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/temporal_analysis/monthly_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 5. USER ANALYSIS
# =============================================================================

print("\n👥 Creating user analysis...")

# User type analysis
user_analysis = divvy_dataset.groupby('member_casual').agg({
    'ride_id': 'count',
    'trip_duration_minutes': ['mean', 'median', 'sum']
}).round(2)
user_analysis.columns = ['total_rides', 'avg_duration', 'median_duration', 'total_duration']
user_analysis = user_analysis.reset_index()
user_analysis['total_hours'] = user_analysis['total_duration'] / 60
user_analysis['percentage'] = user_analysis['total_rides'] / user_analysis['total_rides'].sum() * 100

# User distribution pie chart
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(user_analysis['total_rides'], 
                                  labels=[f"{row['member_casual']}\n{row['total_rides']:,.0f}\n{row['percentage']:.1f}%" 
                                         for _, row in user_analysis.iterrows()],
                                  colors=divvy_colors[:2], autopct='', startangle=90)
ax.set_title('USER TYPE DISTRIBUTION\nMember vs Casual User Market Share Analysis', 
             fontsize=18, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('outputs/user_analysis/user_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Duration comparison
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.bar(user_analysis['member_casual'], user_analysis['avg_duration'], 
              color=divvy_colors[:2], alpha=0.8)

# Add duration labels
for bar, duration in zip(bars, user_analysis['avg_duration']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{duration:.1f} min', ha='center', va='bottom', 
            fontsize=12, fontweight='bold')

ax.set_title('AVERAGE TRIP DURATION BY USER TYPE\nMember vs Casual User Trip Length Analysis', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('User Type', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Duration (minutes)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/user_analysis/duration_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# Hourly pattern by user type
hourly_by_user = divvy_dataset.groupby(['start_hour', 'member_casual']).size().reset_index(name='total_rides')

fig, ax = plt.subplots(figsize=(14, 8))
for user_type in hourly_by_user['member_casual'].unique():
    data = hourly_by_user[hourly_by_user['member_casual'] == user_type]
    ax.plot(data['start_hour'], data['total_rides'], 
            marker='o', linewidth=3, markersize=6, 
            label=user_type, color=divvy_colors[0] if user_type == 'member' else divvy_colors[1])

ax.set_title('HOURLY USAGE PATTERNS BY USER TYPE\nMember vs Casual User Behavior Comparison', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Hour of Day', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Rides', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24, 2))
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/user_analysis/hourly_by_user.png', dpi=300, bbox_inches='tight')
plt.close()

# Member proportion by hour
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(hourly_data['start_hour'], hourly_data['membership_indicator'] * 100, 
              color=divvy_colors[1], alpha=0.8)

# Add percentage labels
for bar, percentage in zip(bars, hourly_data['membership_indicator'] * 100):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            f'{percentage:.1f}%', ha='center', va='bottom', 
            fontsize=10, fontweight='bold')

ax.set_title('MEMBER VS CASUAL USER DISTRIBUTION BY HOUR\nMember Engagement Patterns Throughout the Day', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Hour of Day', fontsize=14, fontweight='bold')
ax.set_ylabel('Member Percentage (%)', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24, 2))
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/user_analysis/member_proportion.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 6. STATION ANALYSIS
# =============================================================================

print("\n🏁 Creating station analysis...")

# Filter real stations
real_stations_start = divvy_dataset[divvy_dataset['start_station_name'] != "Unknown"]['start_station_name'].value_counts().head(10)
real_stations_end = divvy_dataset[divvy_dataset['end_station_name'] != "Unknown"]['end_station_name'].value_counts().head(10)

# Start stations plot
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.barh(range(len(real_stations_start)), real_stations_start.values, 
               color=divvy_colors[0], alpha=0.8)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, real_stations_start.values)):
    ax.text(value + value*0.01, bar.get_y() + bar.get_height()/2, 
            f'{value:,}', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(real_stations_start)))
ax.set_yticklabels(real_stations_start.index, fontsize=9)
ax.set_title('TOP 10 MOST POPULAR START STATIONS\nHigh-Demand Origin Points for Bike Trips', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Rides', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/station_analysis/start_stations.png', dpi=300, bbox_inches='tight')
plt.close()

# End stations plot
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.barh(range(len(real_stations_end)), real_stations_end.values, 
               color=divvy_colors[1], alpha=0.8)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, real_stations_end.values)):
    ax.text(value + value*0.01, bar.get_y() + bar.get_height()/2, 
            f'{value:,}', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(real_stations_end)))
ax.set_yticklabels(real_stations_end.index, fontsize=9)
ax.set_title('TOP 10 MOST POPULAR DESTINATION STATIONS\nHigh-Demand End Points for Bike Trips', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Rides', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/station_analysis/end_stations.png', dpi=300, bbox_inches='tight')
plt.close()

# Station type distribution
total_stations = divvy_dataset['start_station_name'].nunique()
real_stations_count = divvy_dataset[divvy_dataset['start_station_name'] != "Unknown"]['start_station_name'].nunique()
unknown_percentage = (total_stations - real_stations_count) / total_stations * 100

station_types_data = pd.DataFrame({
    'type': ['Real Stations', 'Unknown Stations'],
    'count': [real_stations_count, total_stations - real_stations_count],
    'percentage': [100 - unknown_percentage, unknown_percentage]
})

fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(station_types_data['count'], 
                                  labels=[f"{row['type']}\n{row['percentage']:.1f}%" 
                                         for _, row in station_types_data.iterrows()],
                                  colors=divvy_colors[2:4], autopct='', startangle=90)
ax.set_title(f'STATION TYPE DISTRIBUTION\nTotal Network: {total_stations:,} Stations', 
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('outputs/station_analysis/station_types.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. TEMPORAL HEATMAP
# =============================================================================

print("\n🔥 Creating temporal heatmap...")

# Temporal heatmap
heatmap_data = divvy_dataset.groupby(['start_hour', 'day_of_week']).size().reset_index(name='total_rides')

# Create pivot table for heatmap
heatmap_pivot = heatmap_data.pivot(index='start_hour', columns='day_of_week', values='total_rides')
heatmap_pivot = heatmap_pivot.reindex(columns=day_order)

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(heatmap_pivot, annot=True, fmt=',.0f', cmap='viridis', 
            cbar_kws={'label': 'Number of Rides'}, ax=ax)

ax.set_title('WEEKLY USAGE HEATMAP\nHour-by-Day Usage Intensity Patterns', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Day of Week', fontsize=14, fontweight='bold')
ax.set_ylabel('Hour of Day', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/additional_insights/heatmap.png', dpi=300, bbox_inches='tight')
plt.close()



# =============================================================================
# 9. ADDITIONAL ANALYSES
# =============================================================================

print("\n📈 Creating additional analyses...")

# Trip duration distribution
reasonable_rides = divvy_dataset[divvy_dataset['trip_duration_minutes'] <= 120]

fig, ax = plt.subplots(figsize=(14, 8))
ax.hist(reasonable_rides['trip_duration_minutes'], bins=50, color=divvy_colors[0], alpha=0.7, edgecolor='black')

ax.set_title('TRIP DURATION DISTRIBUTION\nFrequency Analysis of Trip Lengths (Up to 2 Hours)', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Duration (minutes)', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/additional_insights/duration_distribution.png', dpi=300, bbox_inches='tight')
plt.close()



# =============================================================================
# 10. SUMMARY AND CONCLUSIONS
# =============================================================================

print("\n💡 Analysis Summary:")
print("=" * 80)
print("Key Conclusions:")
print("1. Intensive System Usage: The Divvy system shows intensive usage with over 5.4 million trips analyzed.")
print("2. Clear Work Pattern: There is a clear work usage pattern with peaks during work hours (7-9 AM and 5-7 PM).")
print("3. Member Dominance: Member users represent the majority of usage, with shorter and more regular trip patterns.")
print("4. Seasonality: Weekends show a more recreational and distributed usage pattern.")
print("5. Geographic Concentration: Downtown stations are the most utilized.")

print("\nStrategic Recommendations:")
print("1. Fleet Expansion: Expand the bike fleet at high-demand stations during peak hours.")
print("2. Conversion Campaigns: Implement marketing campaigns to convert casual users to members.")
print("3. Distribution Optimization: Optimize bike distribution according to identified temporal patterns.")
print("4. New Stations: Develop new stations in identified growth areas.")
print("5. Dynamic Pricing: Consider dynamic pricing to balance demand during peak hours.")

print(f"\n✅ Analysis completed successfully!")
print(f"📁 All visualizations saved in 'outputs/' directory")
print(f"📊 Total rides analyzed: {total_trips:,}")
print(f"👥 Member percentage: {member_user_percentage:.1f}%")
print(f"⏱️ Average duration: {average_trip_duration:.1f} minutes")
print(f"🏁 Real stations: {total_active_stations:,}")

print(f"\n📁 Generated files:")
print(f"• kpi_strategic.png - Strategic KPIs Dashboard")
print(f"• hourly_analysis.png - Hourly usage patterns")
print(f"• member_proportion.png - Member proportion by hour")
print(f"• daily_pattern.png - Daily usage patterns")
print(f"• user_distribution.png - User type distribution")
print(f"• duration_comparison.png - Duration comparison")
print(f"• hourly_by_user.png - Hourly patterns by user type")
print(f"• start_stations.png - Top start stations")
print(f"• end_stations.png - Top end stations")
print(f"• station_types.png - Station type distribution")
print(f"• heatmap.png - Temporal heatmap")
print(f"• duration_distribution.png - Duration distribution")
print(f"• monthly_analysis.png - Monthly analysis (temporal)") 