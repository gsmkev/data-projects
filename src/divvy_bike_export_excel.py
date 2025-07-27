import pandas as pd
import os

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('data/processed/divvy_combined_data.csv')

# Create datetime columns for analysis
df['started_at'] = pd.to_datetime(df['started_at'])
df['start_hour'] = df['started_at'].dt.hour
df['day_of_week'] = df['started_at'].dt.day_name()
df['month'] = df['started_at'].dt.month_name()

# Create Excel writer
if not os.path.exists("outputs"):
    os.makedirs("outputs", exist_ok=True)
excel_file = 'outputs/divvy_analysis_data.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    
    print("Creating Excel file with all chart data...")
    
    # =============================================================================
    # 1. KPI DASHBOARD DATA
    # =============================================================================
    print("Creating KPI Dashboard data...")
    
    # Calculate KPIs
    total_trips = len(df)
    member_trips = len(df[df['member_casual'] == 'member'])
    casual_trips = len(df[df['member_casual'] == 'casual'])
    member_percentage = (member_trips / total_trips) * 100
    avg_duration = df['trip_duration_minutes'].mean()
    total_hours = df['trip_duration_minutes'].sum() / 60
    
    # Calculate daily efficiency
    date_range = (df['started_at'].max() - df['started_at'].min()).days
    daily_efficiency = total_trips / date_range
    
    # Calculate station efficiency
    real_stations = df[df['start_station_name'] != "Unknown"]['start_station_name'].nunique()
    station_efficiency = total_trips / real_stations
    
    # Calculate satisfaction rate
    optimal_trips = len(df[(df['trip_duration_minutes'] >= 5) & (df['trip_duration_minutes'] <= 60)])
    satisfaction_rate = (optimal_trips / total_trips) * 100
    
    # Create KPI data - numbers without commas
    kpi_data = pd.DataFrame({
        'Metric': ['Total Trips', 'Member Percentage', 'Average Duration', 'Total Hours', 'Daily Efficiency', 'Station Efficiency', 'Satisfaction Rate'],
        'Value_Numeric': [total_trips, member_percentage, avg_duration, total_hours, daily_efficiency, station_efficiency, satisfaction_rate],
        'Value_Formatted': [f"{total_trips}", f"{member_percentage:.1f}%", f"{avg_duration:.1f} min", f"{total_hours/1000:.1f}K hours", f"{daily_efficiency:.0f} trips/day", f"{station_efficiency:.0f} trips/station", f"{satisfaction_rate:.1f}%"],
        'Description': ['Total number of completed trips', 'Proportion of member users', 'Average trip duration', 'Total system usage time', 'Average trips per day', 'Average trips per station', 'Percentage of optimal trips']
    })
    
    kpi_data.to_excel(writer, sheet_name='KPI_Dashboard', index=False)
    
    # =============================================================================
    # 2. HOURLY ANALYSIS DATA
    # =============================================================================
    print("Creating Hourly Analysis data...")
    
    hourly_data = df.groupby('start_hour').agg({
        'ride_id': 'count',
        'membership_indicator': 'mean',
        'trip_duration_minutes': 'mean'
    }).rename(columns={'ride_id': 'total_trips'}).reset_index()
    
    hourly_data['member_percentage'] = hourly_data['membership_indicator'] * 100
    hourly_data['casual_percentage'] = 100 - hourly_data['member_percentage']
    
    hourly_data.to_excel(writer, sheet_name='Hourly_Analysis', index=False)
    
    # =============================================================================
    # 3. DAILY ANALYSIS DATA
    # =============================================================================
    print("Creating Daily Analysis data...")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_data = df.groupby('day_of_week').agg({
        'ride_id': 'count',
        'membership_indicator': 'mean',
        'trip_duration_minutes': 'mean'
    }).rename(columns={'ride_id': 'total_trips'}).reset_index()
    
    daily_data['day_of_week'] = pd.Categorical(daily_data['day_of_week'], categories=day_order, ordered=True)
    daily_data = daily_data.sort_values('day_of_week')
    daily_data['member_percentage'] = daily_data['membership_indicator'] * 100
    
    daily_data.to_excel(writer, sheet_name='Daily_Analysis', index=False)
    
    # =============================================================================
    # 4. MONTHLY ANALYSIS DATA
    # =============================================================================
    print("Creating Monthly Analysis data...")
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_data = df.groupby('month').agg({
        'ride_id': 'count',
        'membership_indicator': 'mean',
        'trip_duration_minutes': 'mean'
    }).rename(columns={'ride_id': 'total_trips'}).reset_index()
    
    monthly_data['month'] = pd.Categorical(monthly_data['month'], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values('month')
    monthly_data['member_percentage'] = monthly_data['membership_indicator'] * 100
    
    monthly_data.to_excel(writer, sheet_name='Monthly_Analysis', index=False)
    
    # =============================================================================
    # 5. USER ANALYSIS DATA
    # =============================================================================
    print("Creating User Analysis data...")
    
    user_analysis = df.groupby('member_casual').agg({
        'ride_id': 'count',
        'trip_duration_minutes': ['mean', 'median', 'sum']
    }).round(2)
    
    user_analysis.columns = ['total_trips', 'avg_duration', 'median_duration', 'total_duration']
    user_analysis = user_analysis.reset_index()
    user_analysis['total_hours'] = user_analysis['total_duration'] / 60
    user_analysis['percentage'] = user_analysis['total_trips'] / user_analysis['total_trips'].sum() * 100
    
    user_analysis.to_excel(writer, sheet_name='User_Analysis', index=False)
    
    # =============================================================================
    # 6. HOURLY BY USER TYPE DATA
    # =============================================================================
    print("Creating Hourly by User Type data...")
    
    hourly_by_user = df.groupby(['start_hour', 'member_casual']).size().reset_index(name='total_trips')
    
    hourly_by_user.to_excel(writer, sheet_name='Hourly_by_User', index=False)
    
    # =============================================================================
    # 7. MEMBER PROPORTION BY HOUR DATA
    # =============================================================================
    print("Creating Member Proportion by Hour data...")
    
    member_proportion_data = hourly_data[['start_hour', 'member_percentage']].copy()
    member_proportion_data['casual_percentage'] = 100 - member_proportion_data['member_percentage']
    
    member_proportion_data.to_excel(writer, sheet_name='Member_Proportion', index=False)
    
    # =============================================================================
    # 8. TOP START STATIONS DATA
    # =============================================================================
    print("Creating Top Start Stations data...")
    
    start_stations = df['start_station_name'].value_counts().head(20).reset_index()
    start_stations.columns = ['station_name', 'total_trips']
    start_stations['percentage'] = (start_stations['total_trips'] / total_trips) * 100
    
    start_stations.to_excel(writer, sheet_name='Top_Start_Stations', index=False)
    
    # =============================================================================
    # 9. TOP END STATIONS DATA
    # =============================================================================
    print("Creating Top End Stations data...")
    
    end_stations = df['end_station_name'].value_counts().head(20).reset_index()
    end_stations.columns = ['station_name', 'total_trips']
    end_stations['percentage'] = (end_stations['total_trips'] / total_trips) * 100
    
    end_stations.to_excel(writer, sheet_name='Top_End_Stations', index=False)
    
    # =============================================================================
    # 10. STATION TYPES DATA
    # =============================================================================
    print("Creating Station Types data...")
    
    total_start_stations = df['start_station_name'].nunique()
    real_start_stations = df[df['start_station_name'] != "Unknown"]['start_station_name'].nunique()
    unknown_start_stations = total_start_stations - real_start_stations
    
    station_types_data = pd.DataFrame({
        'type': ['Real Stations', 'Unknown Stations'],
        'count': [real_start_stations, unknown_start_stations],
        'percentage': [(real_start_stations/total_start_stations)*100, (unknown_start_stations/total_start_stations)*100]
    })
    
    station_types_data.to_excel(writer, sheet_name='Station_Types', index=False)
    
    # =============================================================================
    # 11. TEMPORAL HEATMAP DATA
    # =============================================================================
    print("Creating Temporal Heatmap data...")
    
    heatmap_data = df.groupby(['start_hour', 'day_of_week']).size().reset_index(name='total_trips')
    
    # Create pivot table for heatmap
    heatmap_pivot = heatmap_data.pivot(index='start_hour', columns='day_of_week', values='total_trips')
    heatmap_pivot = heatmap_pivot.reindex(columns=day_order)
    
    heatmap_pivot.to_excel(writer, sheet_name='Temporal_Heatmap')
    
    # =============================================================================
    # 12. DURATION DISTRIBUTION DATA
    # =============================================================================
    print("Creating Duration Distribution data...")
    
    # Filter reasonable rides (up to 2 hours)
    reasonable_rides = df[df['trip_duration_minutes'] <= 120]
    
    # Create duration bins
    duration_bins = pd.cut(reasonable_rides['trip_duration_minutes'], bins=50)
    duration_dist = duration_bins.value_counts().sort_index().reset_index()
    duration_dist.columns = ['duration_range', 'frequency']
    duration_dist['duration_midpoint'] = duration_dist['duration_range'].apply(lambda x: x.mid)
    
    duration_dist.to_excel(writer, sheet_name='Duration_Distribution', index=False)
    
    # =============================================================================
    # 13. SUMMARY STATISTICS
    # =============================================================================
    print("Creating Summary Statistics...")
    
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Trips',
            'Member Trips',
            'Casual Trips',
            'Member Percentage',
            'Casual Percentage',
            'Average Duration (minutes)',
            'Median Duration (minutes)',
            'Total Hours',
            'Daily Efficiency (trips/day)',
            'Real Start Stations',
            'Real End Stations',
            'Average Trips per Start Station',
            'Average Trips per End Station',
            'Optimal Duration Trips (5-60 min)',
            'Satisfaction Rate (%)',
            'Analysis Period (days)',
            'Peak Hour (8 AM) Trips',
            'Peak Hour (6 PM) Trips',
            'Weekday Average Trips',
            'Weekend Average Trips'
        ],
        'Value_Numeric': [
            total_trips,
            member_trips,
            casual_trips,
            member_percentage,
            100-member_percentage,
            avg_duration,
            df['trip_duration_minutes'].median(),
            total_hours,
            daily_efficiency,
            real_stations,
            df[df['end_station_name'] != 'Unknown']['end_station_name'].nunique(),
            total_trips/real_stations,
            total_trips/df[df['end_station_name'] != 'Unknown']['end_station_name'].nunique(),
            optimal_trips,
            satisfaction_rate,
            date_range,
            hourly_data[hourly_data['start_hour'] == 8]['total_trips'].iloc[0],
            hourly_data[hourly_data['start_hour'] == 18]['total_trips'].iloc[0],
            daily_data[daily_data['day_of_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]['total_trips'].mean(),
            daily_data[daily_data['day_of_week'].isin(['Saturday', 'Sunday'])]['total_trips'].mean()
        ],
        'Value_Formatted': [
            f"{total_trips}",
            f"{member_trips}",
            f"{casual_trips}",
            f"{member_percentage:.1f}%",
            f"{100-member_percentage:.1f}%",
            f"{avg_duration:.1f}",
            f"{df['trip_duration_minutes'].median():.1f}",
            f"{total_hours:.1f}",
            f"{daily_efficiency:.0f}",
            f"{real_stations}",
            f"{df[df['end_station_name'] != 'Unknown']['end_station_name'].nunique()}",
            f"{total_trips/real_stations:.0f}",
            f"{total_trips/df[df['end_station_name'] != 'Unknown']['end_station_name'].nunique():.0f}",
            f"{optimal_trips}",
            f"{satisfaction_rate:.1f}",
            f"{date_range}",
            f"{hourly_data[hourly_data['start_hour'] == 8]['total_trips'].iloc[0]}",
            f"{hourly_data[hourly_data['start_hour'] == 18]['total_trips'].iloc[0]}",
            f"{daily_data[daily_data['day_of_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]['total_trips'].mean():.0f}",
            f"{daily_data[daily_data['day_of_week'].isin(['Saturday', 'Sunday'])]['total_trips'].mean():.0f}"
        ]
    })
    
    summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)

print(f"✅ Excel file '{excel_file}' created successfully!")
print("\n📊 Sheets included:")
print("1. KPI_Dashboard - Key performance indicators")
print("2. Hourly_Analysis - Hourly usage patterns")
print("3. Daily_Analysis - Daily usage patterns")
print("4. Monthly_Analysis - Monthly trends")
print("5. User_Analysis - User type breakdown")
print("6. Hourly_by_User - Hourly patterns by user type")
print("7. Member_Proportion - Member percentage by hour")
print("8. Top_Start_Stations - Most popular start stations")
print("9. Top_End_Stations - Most popular end stations")
print("10. Station_Types - Station type distribution")
print("11. Temporal_Heatmap - Hour-day usage heatmap")
print("12. Duration_Distribution - Trip duration frequency")
print("13. Summary_Statistics - Complete dataset summary")