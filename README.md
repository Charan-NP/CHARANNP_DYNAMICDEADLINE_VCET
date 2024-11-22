Dynamic Deadline Automation
This project automates task management in Asana using REST API. It dynamically assigns due dates based on task priority and adjusts deadlines when tasks are moved to the "In Progress" section.

Features
Initial Due Date Assignment
Automatically sets the due date for a task based on its priority:

Low: 14 days from today
Medium: 7 days from today
High: 2 days from today
Dynamic Deadline Adjustment
When a task with High priority is moved to the "In Progress" section:

Extends the due date of all other tasks in the "In Progress" section by 2 days.
Graceful Error Handling
Ensures safe API calls and avoids redundant operations.

Prerequisites
Python 3.7+
Asana Personal Access Token (PAT)
An Asana project with tasks and custom fields for priority (High, Medium, Low).
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/YOUR_USERNAME/DynamicDeadline.git
cd DynamicDeadline
2. Install Required Libraries
Install dependencies using pip:

bash
Copy code
pip install requests
3. Configure Environment Variables
Replace placeholders in the script:

YOUR_ASANA_PERSONAL_ACCESS_TOKEN with your Asana PAT.
TASK_ID_1, TASK_ID_2 with actual Asana Task IDs.
YOUR_PROJECT_ID with your Asana Project ID.
4. Run the Script
Execute the script:

bash
Copy code
python asana_utils.py
Files and Directories
asana_utils.py: Main script containing the automation logic.
README.md: Project documentation.
requirements.txt: Dependencies list (if needed for production).
How It Works
Initial Due Date Assignment
The script calculates the due date based on the task's priority (Low, Medium, High) and updates it via Asana's REST API.

Dynamic Deadline Adjustment
If a High-priority task is moved to the "In Progress" section, the script fetches all tasks in that section and extends their due dates by 2 days.

Error Handling

Safely accesses API data to avoid crashes.
Prints helpful debug logs for troubleshooting.
Example Outputs
Task Details
plaintext
Copy code
Task Details for 1208823951501674: {
    'gid': '1208823951501674',
    'name': 'Example Task',
    'due_on': '2024-12-01',
    'custom_fields': [{'name': 'Priority', 'enum_value': {'name': 'High'}}],
    'memberships': [{'section': {'name': 'In Progress'}}]
}
Due Date Updates
plaintext
Copy code
Task 1208823951501674 due date updated to 2024-12-01
Known Issues
Rate limits: Avoid frequent API calls to prevent being throttled.
Missing section: Tasks without sections are logged and skipped.
Contribution
Feel free to fork and submit pull requests. Contributions are welcome!

License
This project is licensed under the MIT License. See LICENSE for details.

