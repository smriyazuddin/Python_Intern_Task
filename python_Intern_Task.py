import requests
from typing import List, Dict, Any

# Define the target resource endpoint (API URL)
API_URL: str = "https://jsonplaceholder.typicode.com/users"
# Define the filtering constraint for the city name
FILTER_CITY_START: str = 'S'


def fetch_and_display_users(url: str, filter_start_char: str):
    """
    Executes a synchronous HTTP GET request, deserializes the JSON payload,
    applies a city filter, and prints the results to standard output.
    """

    print(f"--- Client: Initiating GET request to {url} ---")
    print(f"--- Constraint: Filtering for cities starting with '{filter_start_char}' ---")
    print("-" * 50)

    try:
        # 1. Network Communication (HTTP GET)
        response = requests.get(url, timeout=10)  # Added timeout for robustness

        # 2. Protocol Validation (Error Handling for 4xx/5xx status codes)
        response.raise_for_status()

        # 3. JSON Deserialization
        users_data: List[Dict[str, Any]] = response.json()

    except requests.exceptions.HTTPError as e:
        print(f"❌ ERROR: Received HTTP Status Error: {e.response.status_code}. Request failed.")
        return
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Network or Connection Failure. Details: {e}")
        return

    # Post-request Data Integrity Check
    if not users_data:
        print("✅ Success, but the API returned an empty list of user records.")
        return

    record_index: int = 0

    # 4. Iterative Processing and Filtering
    for user in users_data:
        # Safe access to top-level fields
        name: str = user.get('name', 'N/A')
        username: str = user.get('username', 'N/A')
        email: str = user.get('email', 'N/A')

        # Safe access to nested field (address.city)
        city: str = user.get('address', {}).get('city', 'N/A')

        # Apply the required filtering logic
        if city.upper().startswith(filter_start_char.upper()):
            record_index += 1

            # 5. Output Generation
            print(f"User {record_index}:")
            print(f"Name: {name}")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"City: {city}")
            print("------------------------")

    # Final Summary
    if record_index == 0:
        print(f"\nResult: Zero records matched the city filter '{filter_start_char}'.")
    else:
        print(f"\nResult: Successfully processed and displayed {record_index} user records.")


# Execution Entry Point
if __name__ == "__main__":
    fetch_and_display_users(API_URL, FILTER_CITY_START)