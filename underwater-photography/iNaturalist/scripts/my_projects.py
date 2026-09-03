"""
Fetches and prints all iNaturalist projects joined by a given user.

Uses the iNaturalist API endpoint:
  GET /v1/users/{user_id}/projects

Output: project title, type, and URL for each joined project.

Note: the iNaturalist API accepts either the numeric user ID or the login
string interchangeably for this endpoint.  The login "andreiastra" (numeric
ID 10958443) is used consistently across all scripts in this project.
"""
import requests

USER_ID = "andreiastra"
url = f"https://api.inaturalist.org/v1/users/{USER_ID}/projects"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    projects = response.json().get("results", [])

    if projects:
        print(f"Projects joined ({len(projects)}):")
        for proj in projects:
            project_title = proj.get("title")
            project_type = proj.get("project_type", "collection")
            print(
                f"- {project_title} [{project_type}] (https://www.inaturalist.org/projects/{proj.get('slug')})"
            )
    else:
        print("No explicitly joined projects found.")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # Python 3.6+
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred during the request: {req_err}")
except ValueError as json_err:
    print(f"JSONDecodeError: Could not decode JSON response: {json_err}")
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
