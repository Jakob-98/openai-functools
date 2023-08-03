from datetime import datetime
import json
from typing import Any, Dict


def generate_spoof_logs(date, vm_id):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d')

    spoof_logs = f"VM: {vm_id} logs for date: {date.strftime('%Y-%m-%d')}\n"

    # Example log messages
    log_messages = [
        ("INFO", "main", "Starting application"),
        ("INFO", "main", "Loading configuration"),
        ("INFO", "main", "Connecting to database"),
        ("INFO", "main", "Fetching data from database"),
        ("INFO", "main", "Data successfully fetched"),
        ("INFO", "main", "Starting application"),
        ("INFO", "main", "Loading configuration"),
        ("WARNING", "main", "Database connection timeout"),
        ("WARNING", "main", "Low disk space on server"),
        ("ERROR", "main", "Error loading configuration"),
        ("ERROR", "component_a", "Failed to initialize component", "ERR001"),
    ]

    for index, log in enumerate(log_messages, 1):
        # Here we use the given date but the time from 'now'
        timestamp = date.replace(hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second, microsecond=datetime.now().microsecond).strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        log_level, log_source, log_message, *error_code = log
        if log_level == "ERROR" and error_code:
            log_entry = f"{timestamp} - {log_level} - {log_source} - {log_message} - Code: {error_code[0]}"
        else:
            log_entry = f"{timestamp} - {log_level} - {log_source} - {log_message}"
        spoof_logs += log_entry + "\n"

    return spoof_logs


def generate_spoof_log_analytics():
    data = {
        "tables": [
            {
                "name": "PrimaryResult",
                "columns": [
                    {"name": "VM ID", "type": "string"},
                    {"name": "Date", "type": "datetime"},
                    {"name": "Error Code", "type": "string"},
                ],
                "rows": [
                    ["VM123", "2023-02-01", "ERR001"]
                ]
            }
        ]
    }

    # Convert the data to JSON format
    spoof_response = json.dumps(data, indent=4)

    return spoof_response


def generate_spoof_api_response(vm_id: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates a spoof response for an API query. The response simulates the format of a typical HTTP response.

    :param str vm_id: The ID of the VM to query.
    :param str endpoint: The endpoint of the API to query.
    :param Dict[str, Any] params: A dictionary of parameters to include in the API query. Default is None.
    :return: A dictionary representing the response from the API.
    :rtype: Dict[str, Any]
    """

    # Format the response
    response = {
        "statusCode": 500,
        "message": "Internal Server Error",
        "vm_id": vm_id,
        "endpoint": endpoint,
        "params": params,
        "errorCode": "ERR001",
        "errorDetails": f"Internal server error encountered for VM ID: {vm_id} on endpoint: {endpoint}"
    }

    return response

def generate_spoof_vector_db_response(query) -> str:
    _ = query
    # Simulated response
    response = f"Error Code ERR001 is a critical alert indicating an Internal Server Error. " \
           f"This issue typically originates from a lower-level system on the server, such as a network socket or a database connection. " \
           f"Immediate recommended actions: " \
           f"\n1. Run a comprehensive health check on all lower-level systems. " \
           f"\n2. Check the server's logs for any additional error messages or warnings closely preceding this alert. " \
           f"\n3. Confirm the stability of network connections, especially for those involved in inter-process communication. " \
           f"\n4. If running a database, ensure connections are pooling correctly and that the DB is not approaching its max connections limit. " \
           f"\n5. If this error is recurring, consider profiling the server's operations to identify any potential bottlenecks or recurring issues. " \
           f"If these steps do not resolve the issue, it may be due to an underlying bug or a hardware issue and further investigation will be required."

    return response

