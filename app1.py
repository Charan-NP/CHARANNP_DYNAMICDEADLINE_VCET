import requests
from datetime import datetime, timedelta
import time

# Configuration
ASANA_TOKEN = '2/1208823802846181/1208823816745598:9da0e64aff631846a0c152d4adb9ca3a'  # Replace with your Asana Personal Access Token
API_URL = 'https://app.asana.com/api/1.0'

headers = {
    'Authorization': f'Bearer {ASANA_TOKEN}',
    'Content-Type': 'application/json'
}

def calculate_due_date(priority):
    """Calculate the due date based on priority."""
    current_date = datetime.now()
    if priority.lower() == 'low':
        return (current_date + timedelta(days=14)).strftime('%Y-%m-%d')
    elif priority.lower() == 'medium':
        return (current_date + timedelta(days=7)).strftime('%Y-%m-%d')
    elif priority.lower() == 'high':
        return (current_date + timedelta(days=2)).strftime('%Y-%m-%d')
    return None

def fetch_task_details(task_id, opt_fields=None):
    """Fetch task details with optional fields."""
    fields = f"?opt_fields={','.join(opt_fields)}" if opt_fields else ""
    response = requests.get(f'{API_URL}/tasks/{task_id}{fields}', headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {})
    else:
        print(f"Failed to fetch task details for {task_id}: {response.json()}")
        return {}

def fetch_tasks_in_progress_section(project_id):
    """Fetch all tasks in the 'In Progress' section of a project."""
    response = requests.get(f'{API_URL}/projects/{project_id}/tasks?opt_fields=memberships,due_on', headers=headers)
    if response.status_code == 200:
        tasks = response.json().get('data', [])
        return [task for task in tasks if any(m.get('section', {}).get('name') == 'In Progress' for m in task.get('memberships', []))]
    else:
        print(f"Failed to fetch tasks for project {project_id}: {response.json()}")
        return []

def update_due_date(task_id, due_date):
    """Update the due date for a task."""
    payload = {
        'data': {'due_on': due_date}
    }
    response = requests.put(f'{API_URL}/tasks/{task_id}', json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Task {task_id} due date updated to {due_date}")
    else:
        print(f"Failed to update due date for task {task_id}: {response.json()}")

def adjust_due_dates_in_progress(high_priority_task_id, project_id):
    """Adjust due dates of all other tasks in the 'In Progress' section."""
    tasks = fetch_tasks_in_progress_section(project_id)
    for task in tasks:
        if task['gid'] != high_priority_task_id and task.get('due_on'):
            # Extend due date by 2 days
            current_due_date = datetime.strptime(task['due_on'], '%Y-%m-%d')
            new_due_date = (current_due_date + timedelta(days=2)).strftime('%Y-%m-%d')
            update_due_date(task['gid'], new_due_date)
            time.sleep(1)  # Avoid rate limits

def initialize_task(task_id, project_id):
    """Initialize a task with the appropriate due date and handle dynamic deadline adjustments."""
    task_details = fetch_task_details(task_id, opt_fields=['custom_fields', 'due_on', 'memberships'])

    # Debugging: Print task details to inspect response
    print(f"Task Details for {task_id}: {task_details}")

    # Get task priority
    custom_fields = task_details.get('custom_fields', [])
    priority = next((field['enum_value']['name'] for field in custom_fields if field.get('name') == 'Priority'), 'Low')
    
    # Get task's current section safely
    current_section = (task_details.get('memberships', [{}])[0]
                       .get('section', {})
                       .get('name', None))
    
    if current_section is None:
        print(f"Task {task_id} is not assigned to any section.")
    
    # Assign initial due date
    due_date = calculate_due_date(priority)
    if due_date and task_details.get('due_on') != due_date:
        update_due_date(task_id, due_date)
        time.sleep(1)  # Avoid rate limits
    
    # Handle dynamic deadline adjustments
    if current_section == 'In Progress' and priority.lower() == 'high':
        adjust_due_dates_in_progress(task_id, project_id)

if __name__ == '__main__':
    task_ids = [
        '1208823951501674',  # Replace with valid Task IDs
        '1208823951501677',
        '1208823951501680'
    ]
    project_id = '1208823950476884'  # Replace with your Asana project ID

    print("Processing tasks...")
    for task_id in task_ids:
        initialize_task(task_id, project_id)

    print("Task processing complete.")
