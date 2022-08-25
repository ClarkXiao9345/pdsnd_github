import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would like to see data for Chicago, New York City or Washington? ").lower()
    while city not in ('new york city', 'chicago', 'washington'):
        print('Sorry, input error.Pleas enter valid city.')
        city = input("Please choose Chicago, New York City or Washinton?\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month - all,January, February, March, April, May, or June?").lower()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        print('Sorry, input error.Pleas enter a valid month.')
        month = input("Please pick from all,January, February, March, April, May, or June\n").lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day you want? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?").lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        print('Sorry, input error.Pleas enter a valid day.')
        day = input("Please enter a valid day - sun, mon, tue,wed,thu,fri,sat or all\n").lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv("{}.csv".format(city.replace(" ", "_")))

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day, :]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df['month'].mode()[0]
    print("The most common month is: ", month_mode)

    # display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print("The most common day of week is: ", day_mode)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_mode = df['hour'].mode()[0]
    print("The most common hour is: ", hour_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used start station is:', end_station)

    # display most frequent combination of start station and end station trip
    df['common_route'] = df['Start Station'] + " " + df['End Station']
    print('Most commonly used combination of start and end station is:', df['common_route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time / (60 * 60), "hours")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time / 60, "mins")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Tyeps:\n", user_types)

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print("User_gender:\n", user_gender)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print("The earliest year of birth is:", earliest_birth)
        print("The most recent year of birth is: ", most_recent_birth)
        print("The most common year of birth is ", most_common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    end_loc = 5
    while view_data == "yes":
        print(df.iloc[start_loc:end_loc, :])
        start_loc += 5
        end_loc += 5
        view_display = input("Do you want to see more data?: Enter yes or no ").lower()
        if view_display == "no":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart the program? Please Enter "yes or no"\n').lower()

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()