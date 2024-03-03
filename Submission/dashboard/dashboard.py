import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

def define_month(data_2011, data_2012, month_names):
    data_2011['month'] = pd.Categorical(data_2011['month'], categories=month_names, ordered=True)
    data_2012['month'] = pd.Categorical(data_2012['month'], categories=month_names, ordered=True)
    data_2011 = data_2011.sort_values(by='month')
    data_2012 = data_2012.sort_values(by='month')
    monthly_counts_2011 = data_2011.groupby('month')['count'].sum()
    monthly_counts_2012 = data_2012.groupby('month')['count'].sum()

    #Visualize the chart
    plt.plot(monthly_counts_2011.index, monthly_counts_2011.values, marker='o', linestyle='-', label='2011')
    plt.plot(monthly_counts_2012.index, monthly_counts_2012.values, marker='o', linestyle='-', label='2012')
    plt.xlabel('Month')
    plt.ylabel('Total Count')
    plt.title('Total Count by Month for 2011 and 2012')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Display the plot using Streamlit
    st.pyplot()

def mean_visual(hourly_mean_count):
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_mean_count.index, hourly_mean_count.values, color='skyblue')

    # Add a line plot to visualize the trend
    plt.plot(hourly_mean_count.index, hourly_mean_count.values, color='lightsalmon', marker='o', linestyle='-', linewidth=2)

    plt.xlabel('Hour of the Day')
    plt.ylabel('Mean Rental Count')
    plt.title('Mean Rental Count and Trend for Each Hour of the Day')
    plt.xticks(range(24))
    plt.grid(axis='y')
    plt.legend()
    st.pyplot()

def highest_mean_visual(hourly_mean_count):
    top_three_hours = hourly_mean_count.sort_values(ascending=False).head(5)

    # Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_three_hours.index, top_three_hours.values, color='skyblue')
    other_hours = hourly_mean_count[~hourly_mean_count.index.isin(top_three_hours.index)]
    plt.bar(other_hours.index, other_hours.values, color='lightgray')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Mean Rental Count')
    plt.title('Mean Rental Count')
    plt.xticks(range(24))
    plt.grid(axis='y')
    st.pyplot()

def weather_visual(hour_df):
    weather_counts_total = hour_df.groupby('weather')['count'].sum()
    max_total_count = weather_counts_total.max()
    colors_total = ['lightgray'] * len(weather_counts_total)
    max_total_index = weather_counts_total[weather_counts_total == max_total_count].index[0]
    colors_total[weather_counts_total.index.get_loc(max_total_index)] = 'skyblue'

    weather_counts_avg = hour_df.groupby('weather')['count'].mean()
    max_avg_count = weather_counts_avg.max()
    colors_avg = ['lightgray'] * len(weather_counts_avg)
    max_avg_index = weather_counts_avg[weather_counts_avg == max_avg_count].index[0]
    colors_avg[weather_counts_avg.index.get_loc(max_avg_index)] = 'skyblue'

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Plot total count chart
    axes[0].bar(weather_counts_total.index, weather_counts_total, color=colors_total)
    axes[0].set_xlabel('Weather Situation')
    axes[0].set_ylabel('Total Count of Bike Rentals')
    axes[0].set_title('Impact of Weather on Total Bike Rental Demand')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y')
    axes[0].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # Plot average count chart
    axes[1].bar(weather_counts_avg.index, weather_counts_avg, color=colors_avg)
    axes[1].set_xlabel('Weather Condition')
    axes[1].set_ylabel('Average Rental Count')
    axes[1].set_title('Average Rental Count by Weather Condition')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y')

    # Adjust layout
    plt.tight_layout()
    st.pyplot()


def rfm_visual(hour_data_df):
    rfm_df = hour_data_df.groupby('id').agg({
    'datetime': lambda x: (pd.Timestamp.now() - x.max()).days,  # Recency: Number of days since last rental
    'id': 'count',  # Frequency: Number of rentals
    'count': 'max'  # Monetary: Total count of rental bikes
    }).rename(columns={
        'datetime': 'recency',
        'id': 'frequency',
        'count': 'monetary'
    })

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    sns.barplot(y="recency", x="id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=15)
    
    sns.barplot(y="frequency", x="id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)
    
    sns.barplot(y="monetary", x="id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)
    
    plt.suptitle("Best Customer Based on RFM Parameters (id)", fontsize=20)
    st.pyplot()

def cohor_analysis_visual(hour_data_df):
    # Group data by registration month and calculate metrics for each cohort
    cohort_data = hour_data_df.groupby('registration_month').agg({
        'id': 'nunique',  # Number of unique customers
        'count': 'sum'  # Total count of rentals
    })

    # Calculate retention rate for each cohort
    cohort_data['retention_rate'] = cohort_data['id'] / cohort_data['id'].iloc[0]

    # Calculate average rental count for each cohort
    cohort_data['average_rental_count'] = cohort_data['count'] / cohort_data['id']

    # Convert index to string representation of the date
    x_values = cohort_data.index.astype(str)

    # Plot retention rate over time
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, cohort_data['retention_rate'], marker='o', linestyle='-')
    plt.xlabel('Registration Month')
    plt.ylabel('Retention Rate')
    plt.title('Retention Rate Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot()

hour_data_df = pd.read_csv("https://raw.githubusercontent.com/wahyudhiasatwika/Dicoding_dataset/main/Bike/hour_data.csv")

datetime_columns = ["datetime"]
hour_data_df.sort_values(by="datetime", inplace=True)
hour_data_df.reset_index(inplace=True)

for column in datetime_columns:
    hour_data_df[column] = pd.to_datetime(hour_data_df[column])

min_date = hour_data_df["datetime"].min()
max_date = hour_data_df["datetime"].max()

with st.sidebar:
    st.image("https://github.com/wahyudhiasatwika/Dicoding_dataset/blob/main/Bike/bike.jpg?raw=true")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_data_df[(hour_data_df["datetime"] >= str(start_date)) & 
                (hour_data_df["datetime"] <= str(end_date))]

st.header('Bike Sharing :sparkles:')
st.subheader('Bike Rental')

col1, col2 = st.columns(2)

with col1:
    total_transaction = hour_data_df['count'].count()
    st.metric("Total Transaction", value=total_transaction)

with col2:
    total_rent = hour_data_df['count'].sum() 
    st.metric("Total Rent Bikes", value=total_rent)

st.subheader('What are the bicycle rental trends each month for the years 2011 and 2012?')

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
data_2011 = hour_data_df[hour_data_df['year'] == 2011]
data_2012 = hour_data_df[hour_data_df['year'] == 2012]

define_month(data_2011, data_2012, month_names)
st.text("From two year, April until September have the highest usage of bike rental with an increasing demand on year 2012.")

st.subheader("What is the average duration on using bike rental?")
hourly_mean_count = hour_data_df.groupby('hour')['count'].mean()

mean_visual(hourly_mean_count)
st.text("From the chart we see the average of people using bike rental and the tren of bike rental. To make it easier, let's make the five highest average to skyblue color and light gray for the rest.")

highest_mean_visual(hourly_mean_count)
st.text("Based on the chart, We can see people often use bike rental with the duration 8 hours or 16 until 19 hours")

st.subheader("Which season has the greatest impact on bicycle rental usage?")
weather_visual(hour_data_df)

st.subheader("RFM Analysis")
rfm_visual(hour_data_df)
st.text("I sorted the five highest bike rent that people did. We can see the recency that means the last time they use bike rents is on 4177 untul 4192 days. The frequency is 1 because the dataset don't have customer id, so we can't calculate how many they have already used bike rent. The last one, monetary should be a frequency of total count but since the dataset doesn't have customer so i used highest count of rental bikes for monetary and there are around 967 until 977. ")

st.subheader("Retention Rate Analysis")
cohor_analysis_visual(hour_data_df)
st.text("For the retention, it should be calculating the period of people using bike rent. Since there are no customer id, so the chart only showing a tren that are around 1 which mean the frequency of people using bike rents are 1. ")

st.caption("Copyright@Wahyu Dhia Satwika")