import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
   if 'id_1' not in df.columns or 'id_2' not in df.columns or 'car' not in df.columns:
        raise ValueError("Columns 'id_1', 'id_2', and 'car' must be present in the DataFrame.")

    # Create a pivot table with 'id_1' as index, 'id_2' as columns, and 'car' as values
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # If there are missing values, you can fill them with a default value (e.g., 0)
    car_matrix = car_matrix.fillna(0)

    return generate_car_matrix
    result_matrix = generate_car_matrix(df)
    print(result_matrix)


def get_type_count(df):
    # Assuming 'car' is the column you want to categorize
    car_type_counts = df['car'].value_counts().to_dict()
    return car_type_counts

def get_bus_indexes(df):
    # Assuming 'bus' is the column you want to analyze
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    return bus_indexes


def filter_routes(df):
    # Assuming 'route' is the column containing route names, and 'truck' is the column you want to analyze
    routes_above_seven = df.groupby('route')['truck'].mean() > 7
    selected_routes = routes_above_seven[routes_above_seven].index.tolist()
    return selected_routes


def multiply_matrix(matrix):
    # Define a custom function to apply to each element of the matrix
    def custom_multiply(value):
        if value % 2 == 0:
            return value * 2
        else:
            return value * 3

    # Apply the custom function to each element of the matrix
    modified_matrix = matrix.applymap(custom_multiply)
    return modified_matrix


def time_check(df):
    # Assuming 'id', 'id_2', and 'timestamp' are the relevant columns in the DataFrame
    # Convert 'timestamp' to datetime if it's not already in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Define the time range for a full 24-hour period
    full_24_hour_range = pd.date_range(start='00:00:00', end='23:59:59', freq='1H')

    # Define the time range for a full 7 days period
    full_7_days_range = pd.date_range(start=df['timestamp'].min().floor('D'), end=df['timestamp'].max().ceil('D'), freq='1D')

    # Check if each (`id`, `id_2`) pair covers a full 24-hour and 7 days period
    completeness_series = df.groupby(['id', 'id_2'])['timestamp'].agg(
        lambda x: all(x.dt.hour.isin(full_24_hour_range.hour)) and all(x.dt.date.isin(full_7_days_range.date))
    )

    return completeness_series





