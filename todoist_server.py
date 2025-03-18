from dataclasses import dataclass
import os
import sys

from mcp.server.fastmcp import FastMCP, Context
from todoist_api_python.api import TodoistAPI


TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
# if not TODOIST_API_KEY:
#     raise Exception('TODOIST_API_KEY not set. Add to MCP config file.')

todoist_api = TodoistAPI(TODOIST_API_KEY)
mcp = FastMCP("todoist-server", dependencies=["todoist_api_python"])

@mcp.tool()
def output_context(ctx: Context):
    """ Output the context """
    for i in range(10):
        ctx.info(f"Processing file: {i}")

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
    """ Get all projects """
    try:
        projects: TodoistProjectResponse = todoist_api.get_projects()
        return [Project(p.id, p.name) for p in projects]
    except Exception as e:
        return f"Couldn't fetch projects {str(e)}"
    

if __name__ == "__main__":
    # Initialize and run the server
    print('...', file=sys.stderr)
    mcp.run(transport='stdio')