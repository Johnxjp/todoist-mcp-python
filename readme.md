# Todoist Python MCP Server

This is a Model Context Protocol (MCP) server that allows MCP Clients like Claude to interact with Todoist, enabling task management capabilities through natural language. The server acts as an intermediary between Claude and the Todoist API, handling authentication, data transformation, and command processing.

## Features

- **Task Creation**: Create new tasks with required content and optional attributes
- **Task Retrieval**: Get task by ID or list tasks with filtering options
- **Task Management**: Update task attributes, mark tasks as complete, delete tasks

## Prerequisites

- Python 3.12
- uv
- A Todoist account and API token

### How to get Todoist API Token
1. Login to your Todoist account
2. Go to User Settings -> Integrations -> Developer
3. Copy API token

## Usage with Claude Desktop

First clone this locally e.g. with SSH

```
git clone git@github.com:Johnxjp/todoist-mcp-python.git
```

Then add to your Claude config file.
```
{
  "mcpServers": {
    "todoist-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "todoist_api_python",
        "mcp",
        "run",
        "/full/path/to/todoist_server.py"
      ],
      "env": {
        "TODOIST_API_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

## Available Tools

The server provides the following tools for Claude to use:

1. **create_task**: Create a new task in Todoist
   - Required: content (title of the task)
   - Optional: 
      - description, 
      - due_date, 
      - priority, 
      - project_id, 
      - section_id,
      - labels

2. **get_tasks**: Get a list of tasks and Ids from Todoist with various filters
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
