from dataclasses import dataclass
import logging
import os
import sys
from typing import Literal, Optional

from mcp.server.lowlevel import server 
from mcp.server.fastmcp import FastMCP, Context
from todoist_api_python.api import TodoistAPI


TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
# if not TODOIST_API_KEY:
#     raise Exception('TODOIST_API_KEY not set. Add to MCP config file.')

todoist_api = TodoistAPI(TODOIST_API_KEY)
mcp = FastMCP("todoist-server", dependencies=["todoist_api_python"])
logger = logging.getLogger('todoist_server')

@dataclass
class Project:
    id: str
    name: str

# Abstraction for Todoist project
# https://developer.todoist.com/rest/v2/#get-all-projects
@dataclass
class TodoistProjectResponse:
    id: str
    name: str


@mcp.tool()
def get_projects() -> list[Project]:
    """ Get all todo projects. These are like folders for tasks in Todoist """
    try:
        projects: TodoistProjectResponse = todoist_api.get_projects()
        return [Project(p.id, p.name) for p in projects]
    except Exception as e:
        return f"Error: Couldn't fetch projects {str(e)}"


def get_project_id_by_name(project_name: str) -> str:
    """ Search for a project by name and return its ID """
    projects = get_projects()
    for project in projects:
        if project.name.lower() == project_name.lower():
            return project.id
    return None


@mcp.tool()
def get_tasks(
    project_id: Optional[str] = None, 
    project_name: Optional[str] = None, 
    labels: Optional[list[str]] = None, 
    priority: Optional[Literal[1, 2, 3, 4]] = None,
) -> list[str]:
    """ 
    Fetch user's tasks. These can be filtered by project, labels, time, etc. If no filters are provided, all tasks are returned.

    Args:
        project_id: The string ID of the project to fetch tasks from. Example '1234567890'
        project_name: Name of the project to fetch tasks from. Example 'Work' or 'Inbox'
        labels: List of tags used to filter tasks.
        priority: Filter tasks by priority level. 4 (urgent), 3 (high), 2 (normal), 1 (low)
    """

    tasks = todoist_api.get_tasks()
    
    # How to implement "did you mean this project?" feature?
    if project_name:
        project_id = get_project_id_by_name(project_name)
        if not project_id:
            raise ValueError(f"Project '{project_name}' not found")

    if project_id:
        tasks = [t for t in tasks if t.project_id == project_id]

    if labels:
        for label in labels:
            tasks = [t for t in tasks if label.lower() in [l.lower() for l in t.labels]]

    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    
    return [t.content for t in tasks]



if __name__ == "__main__":
    # Initialize and run the server
    print('...', file=sys.stderr)
    mcp.run(transport='stdio')