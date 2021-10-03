import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Function to figure out the filtering requirements of the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #I am now creating an empty city variable
    city = ''
    
    #Implementing a WHILE LOOP for error handling
    while city not in CITY_DATA.keys():
        print("\nWelcome to this program. Please input a city name:")
        print("\n1. Chicago 2. New York City 3. Washington")
        
        #I am now converting the user's input into lower case so that the input is acceptable
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease re-check your input. It is not among the 3 cities: Chicago, New york city or Washington.")
            print("\nrestarting....")

    print(f"\nYou have chosen {city.title()} as your city.")

    #Creating a dictionary that maps keys and values for the months
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter a month name between January and June or enter 'all' to view data for all the months:")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nIncorrect input. Please input the month again.")
            print("\nrestarting....")

    print(f"\nYou have chosen {month.title()} as your month.")

    #Creating a dictionary that maps keys and values for the days
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter the day of the week or enter 'all' to view data for all the days:")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nIncorrect input. Please input the day of the week again.")
            print("\nRestarting....")

    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for City: {city.upper()}, Month/s: {month.upper()} and Day/s of the week: {day.upper()}.")
    print('-'*80)
    
    
    #Returning the city, month and day selections
    return city, month, day

#Function to load data from .csv files
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #Load data for city
    print("\nLoading the requested data....")
    df = pd.read_csv(CITY_DATA[city])

    #Converting the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel....\n')
    start_time = time.time()

    #Here, i used the mode function
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = January, 2 = February,...,6 = June) is: {popular_month}")

    #Uses mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day of the Week is: {popular_day}")

    #Extract hour from the Start Time column
    df['hour'] = df['Start Time'].dt.hour

    #I use the mode function here too
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour is: {popular_hour}")

    #Time taken to complete the computation
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating the most popular stations and trips....\n')
    start_time = time.time()

    #I use the mode function to find the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station is: {common_start_station}")

    #I use the mode function again to find the most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station is: {common_end_station}")

    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating Trip Duration....\n')
    start_time = time.time()

    #Here, I use the sum function
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #Calculating the average trip duration
    average_duration = round(df['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating User Stats....\n')
    start_time = time.time()

    #Calculate total users and their summary by type
    user_type = df['User Type'].value_counts()

    print(f"The count of users by type is:\n\n{user_type}")

    #Calculate number of users by gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe count of users by gender is:\n\n{gender}")
    except:
        print("\nThere is no gender column in this dataset.")

    #Computing earliest birth year, most recent birth year and most common birth year from the dataset
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth is: {earliest}\n\nThe most recent year of birth is: {recent}\n\nThe most common year of birth is: {common_year}")
    except:
        print("There are no birth year details in the Dataset.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to display the data as specified in Rubric
def df_display(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    MY_RESPONSES = ['yes', 'no']
    resonse_df = ''
    #I introduce a counter variable
    counter = 0
    while resonse_df not in MY_RESPONSES:
        print("\nDo you wish to view the raw data?")
        resonse_df = input().lower()
        #the raw data from the df is displayed depending on what the user specifies
        if resonse_df == "yes":
            print(df.head())
        elif resonse_df not in MY_RESPONSES:
            print("\nPlease re-check your input.")
            print("\nrestarting....\n")

    #I add an extra while loop to give user more options when it comes to viewing data
    while resonse_df == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        resonse_df = input().lower()
        #If user opts for it, then I display the next 5 lines
        if resonse_df == "yes":
             print(df[counter:counter+5])
        elif resonse_df != "yes":
             break

    print('-'*80)


#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        df_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()