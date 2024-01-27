from datetime import date, datetime, timedelta
import holidays
from typing import Dict, List

def combine_subdivision_holidays(
        locations_dict: Dict[str, Dict[str, str]],
        years: List[int]
) -> List[str]:
    """
    Combine holidays for multiple subdivisions into a single list of unique dates.

    Parameters:
        - locations_dict (Dict): A dictionary containing location information for each subdivision.
        - years (List[int]): List of years for which to fetch holiday data.

    Returns:
        - List[str]: A combined list containing unique dates of holidays for all subdivisions.
    """
    combined_holidays = []

    for location_id, location_info in locations_dict.items():
        country = location_info['country']
        subdivision = location_info['subdivision']

        subdivision_holidays = holidays.country_holidays(
            country=country,
            subdiv=subdivision,
            years=years,
        )

        # Extract only the dates without the holiday names and convert to a list
        dates_only_list = [date for date in subdivision_holidays.keys()]

        # Extend the list with unique dates from the current subdivision
        combined_holidays.extend(date for date in dates_only_list if date not in combined_holidays)

    return combined_holidays

def generate_weekend_dates_list(years: List[int]):
    """
    Check if each day in the given years is a weekend.

    Parameters:
        - years (List[int]): List of years to check.

    Returns:
        - List[List[datetime.date]]: A list where each item is a list of datetime.date objects representing weekend dates for each year.
    """
    weekend_dates_list = []

    for year in years:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        current_date = start_date

        result_list = []

        while current_date <= end_date:
            if current_date.weekday() in [5, 6]:  # Check if the day is a weekend (Saturday or Sunday)
                result_list.append(current_date.date())
            current_date += timedelta(days=1)

        weekend_dates_list.extend(result_list)

    return weekend_dates_list

def weekend_and_holiday_dates(
    locations_dict: Dict[str, Dict[str, str]],
    years: List[int]
) -> List[date]:
    """
    Combine weekend dates and holidays while keeping only unique instances.

    Parameters:
        - locations_dict (Dict): A dictionary containing location information for each subdivision.
        - years (List[int]): List of years for which to fetch holiday data.

    Returns:
        - List[date]: A combined list containing unique instances of weekend dates and holidays.
    """
    weekends_list = generate_weekend_dates_list(years)
    holidays_list = combine_subdivision_holidays(locations_dict=locations_dict, years=years)

    # Combine weekends and holidays while keeping only unique instances
    weekends_and_holidays = list(set(weekends_list + holidays_list))

    return weekends_and_holidays


from datetime import datetime, date

def convert_to_date(date_str: str) -> date:
    """
    Check if the date string is in the format 'yyyy-mm-dd' and convert it to a datetime.date object.

    Parameters:
        - date_str (str): The date string to convert.

    Returns:
        - date: A datetime.date object representing the parsed date.

    Raises:
        - ValueError: If the date string is not in the expected format.
    """
    try:
        # Attempt to parse the date string
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return parsed_date
    except ValueError as e:
        # Raise an error if the date string is not in the expected format
        raise ValueError(f"Invalid date format. Expected 'yyyy-mm-dd'. Error: {e}")

def find_business_day(base_date: date, weekends_and_holiday_dates: list, direction: str = 'next') -> date:
    """
    Find either the next or previous business day from the given base date.

    Parameters:
        - base_date (date): The base date from which to start the search.
        - direction (str): The direction to search, either 'next' or 'previous'. Default is 'next'.

    Returns:
        - date: The next or previous business day.
    """

    # Set the step for searching forward or backward
    step = 1 if direction == 'next' else -1

    current_date = base_date

    while current_date in weekends_and_holiday_dates:
        current_date += timedelta(days=step)

    return current_date