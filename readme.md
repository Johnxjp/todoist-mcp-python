# Todoist MCP Server for Claude

This is a Managed Context Profile (MCP) server that allows Claude to interact with Todoist, enabling task management capabilities through natural language. The server acts as an intermediary between Claude and the Todoist API, handling authentication, data transformation, and command processing.

## Features

- **Task Creation**: Create new tasks with required content and optional attributes
- **Task Retrieval**: Get task by ID or list tasks with filtering options
- **Task Management**: Update task attributes, mark tasks as complete, delete tasks

## Prerequisites

- Python 3.8 or higher
- A Todoist account and API token

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/todoist-mcp.git
   cd todoist-mcp
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the `.env.example` file:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file and add your Todoist API token:
   ```
   TODOIST_API_TOKEN=your_todoist_api_token_here
   ```

   You can get your API token from [Todoist Settings > Integrations](https://todoist.com/app/settings/integrations).

## Usage

Run the MCP server:

```
python todoist_mcp_server.py
```

The server will start and listen for requests on stdio.

## Available Tools

The server provides the following tools for Claude to use:

1. **todoist_create_task**: Create a new task in Todoist
   - Required: content (title of the task)
   - Optional: description, due_string, priority

2. **get_tasks**: Get a list of tasks from Todoist with various filters
   - Optional: 
      - project_id, 
      - project_name,
      - task_name,
      - priority,
      - labels,
      - is_overdue,
      - limit

3. **update_task**: Update an existing task by searching for it by name
   - Required: task_id
   - Optional: 
      - content, 
      - description, 
      - labels,
      - priority,
      - due_date (YYYY-MM-DD),
      - deadline_date (YYYY-MM-DD)

4. **delete_task**: Delete a task by searching for it by name
   - Required: task_id

5. **complete_task**: Mark a task as complete by searching for it by name
   - Required: task_id

## Example Interactions

Here are some examples of how Claude can interact with Todoist through this MCP server:

- "Add a task to buy groceries"
- "Show me all my urgent tasks"
- "What tasks are due today?"
- "Mark the laundry task as done"
- "Change the priority of my dentist appointment to urgent"

## Security Considerations

- The server securely handles your Todoist API token through environment variables
- Never share your `.env` file or expose your API token
- The server runs locally and communicates only with the Todoist API

## License

[MIT License](LICENSE)

## Acknowledgements

- [Todoist API Python Client](https://github.com/Doist/todoist-api-python)
- [Model Context Protocol](https://github.com/anthropics/model-context-protocol)