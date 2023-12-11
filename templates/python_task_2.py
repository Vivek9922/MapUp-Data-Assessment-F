import pandas as pd


def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): DataFrame containing the data for which distances need to be calculated.

    Returns:
        pandas.DataFrame: Distance matrix.
    """
    # Assuming the relevant columns for calculating distances are 'latitude' and 'longitude'
    coordinates = df[['latitude', 'longitude']]

    # Calculate pairwise distances using Euclidean distance metric
    distance_matrix = pd.DataFrame(cdist(coordinates, coordinates, metric='euclidean'), index=df.index, columns=df.index)

    return distance_matrix


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Assuming the rows and columns of the distance matrix are labeled with 'id' values
    df_unrolled = df.reset_index().melt(id_vars='index', var_name='id_end', value_name='distance')

    # Rename columns to match the desired output
    df_unrolled.columns = ['id_start', 'id_end', 'distance']

    # Optionally, you can filter out rows where 'id_start' is equal to 'id_end' if needed
    df_unrolled = df_unrolled[df_unrolled['id_start'] != df_unrolled['id_end']]

    return df_unrolled


def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): DataFrame containing 'id_start', 'id_end', and 'distance' columns.
        reference_id (int): Reference ID for which to find similar IDs.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Calculate the average distance for the reference ID
    reference_avg_distance = df.loc[(df['id_start'] == reference_id) | (df['id_end'] == reference_id), 'distance'].mean()

    # Calculate the threshold for similarity (within 10% of the reference average distance)
    threshold = 0.1 * reference_avg_distance

    # Find all IDs whose average distance is within the threshold
    similar_ids = df.groupby('id_start')['distance'].mean().reset_index()
    similar_ids = similar_ids[(similar_ids['distance'] >= reference_avg_distance - threshold) &
                              (similar_ids['distance'] <= reference_avg_distance + threshold)]

    return similar_ids


def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame): Unrolled DataFrame containing columns 'id_start', 'id_end', 'distance', and 'vehicle_type'.

    Returns:
        pandas.DataFrame: DataFrame with toll rates added.
    """
    # Assuming the toll rates are based on the vehicle type
    toll_rates = {
        'car': 0.1,    # Toll rate for cars
        'truck': 0.2,  # Toll rate for trucks
        # Add more vehicle types and their corresponding toll rates as needed
    }

    # Calculate toll rates based on the 'vehicle_type' column
    df['toll_rate'] = df['vehicle_type'].map(toll_rates)

    # Calculate toll charges based on distance and toll rate
    df['toll_charge'] = df['distance'] * df['toll_rate']

    return df


def calculate_time_based_toll_rates(df):
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): DataFrame containing columns 'id_start', 'id_end', 'distance', 'timestamp', and 'vehicle_type'.

    Returns:
        pandas.DataFrame: DataFrame with time-based toll rates added.
    """
    # Define time intervals and corresponding toll rates
    time_intervals = [(0, 6), (6, 12), (12, 18), (18, 24)]
    toll_rates = {
        'car': [0.1, 0.2, 0.15, 0.25],    # Toll rates for cars for each time interval
        'truck': [0.2, 0.3, 0.25, 0.35],  # Toll rates for trucks for each time interval
        # Add more vehicle types and their corresponding toll rates as needed
    }

    # Convert 'timestamp' to datetime if it's not already in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Define a custom function to assign toll rates based on the time of the day
    def get_time_interval_rate(row):
        for start, end in time_intervals:
            if start <= row['timestamp'].hour < end:
                return toll_rates[row['vehicle_type']][time_intervals.index((start, end))]
        return 0.0  # Default rate if no match is found

    # Apply the custom function to calculate time-based toll rates
    df['time_based_toll_rate'] = df.apply(get_time_interval_rate, axis=1)

    # Calculate toll charges based on distance and time-based toll rate
    df['time_based_toll_charge'] = df['distance'] * df['time_based_toll_rate']

    return df

