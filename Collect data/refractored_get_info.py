import pandas as pd
import requests
import json
import time

# Define function to retry requests when rate limit is reached
def retry_on_rate_limit(request_fn, *args, **kwargs):
    retries = 0
    max_retries = 5
    while True:
        response = request_fn(*args, **kwargs)
        if response.status_code == 200:
            return response
        elif (
            response.status_code == 403
            and "X-RateLimit-Remaining" in response.headers
            and int(response.headers["X-RateLimit-Remaining"]) == 0
        ):
            reset_time = int(response.headers["X-RateLimit-Reset"])
            wait_time = max(reset_time - time.time() + 1, 0)
            print(f"Rate limit reached, waiting for reset ({wait_time} seconds)...")
            time.sleep(wait_time)
        elif response.status_code == 502:
            if retries < max_retries:
                retries += 1
                print(f"Encountered 502 error, retrying in {retries} seconds...")
                time.sleep(retries)
            else:
                print(f"Encountered 502 error {max_retries} times, giving up...")
                return None
        else:
            print(f"Error Code {response.status_code}: {response.text}")
            return None


# Dataframes
df = pd.read_csv("repos_with_owners", sep=",")
scheme = pd.read_csv("scheme_info", sep=",")
failed_requests = pd.read_csv("failed_info", sep=",")

tokens = [
    # Add Github Tokens here
]

for i in range(0, len(df)):
    owner_and_name = df["Owners_and_Repos"][i]

    # Checking empty strings
    if len(str(owner_and_name).split("/", 1)) != 2:
        continue
    owner, name = str(owner_and_name).split("/", 1)

    # Switching between the 2 token per every 4000 requests
    j = 0
    if i % 1000 == 0:
        if j == 0:
            j = 1

        elif j == 1:
            j = 2

        elif j == 2:
            j = 0

    # Passing tokens into header frame of the api
    headers = {
        "Authorization": f"bearer {tokens[j]}",
        "Content-Type": "application/json",
    }

    # Passing query based on on name and owner of a repo from the dataframe
    query = f"""
{{
   repository(name: "{name}", owner:"{owner}"){{
       name
       description
       url
       isPrivate
       isFork
       forkCount
       stargazerCount
       object(expression:"main"){{
           ... on Commit {{
               history {{
                   totalCount
               }}
           }}
       }}
       secondObject: object(expression:"master"){{
           ... on Commit {{
               history {{
                   totalCount
               }}
           }}
       }}
   }}
}}
"""

    # Graphql post request with retry_on_rate_limit
    request = retry_on_rate_limit(
        requests.post,
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers,
        timeout=15,
    )

    if request is not None and request.status_code == 200:
        info = request.json()

        # error checking for failed responces from the github graphql api
        if "errors" in json.loads(request.text):
            print(i)
            failed_requests._set_value(i, "index", i)
            failed_requests._set_value(i, "name", name)
            failed_requests._set_value(i, "owner", owner)
            failed_requests._set_value(i, "error", request.text)
            failed_requests.to_csv("failed_info", index=False, sep=",")
            continue
        print(i)
        if info["data"]["repository"]["name"] is None:
            repo_name = ""
        else:
            repo_name = info["data"]["repository"]["name"]

        if info["data"]["repository"]["description"] is None:
            repo_description = ""
        else:
            repo_description = info["data"]["repository"]["description"]

        if info["data"]["repository"]["url"] is None:
            repo_url = ""
        else:
            repo_url = info["data"]["repository"]["url"]

        if info["data"]["repository"]["isPrivate"] is None:
            is_Private = ""
        else:
            is_Private = info["data"]["repository"]["isPrivate"]

        if info["data"]["repository"]["isFork"] is None:
            is_Forked = ""
        else:
            is_Forked = info["data"]["repository"]["isFork"]

        if info["data"]["repository"]["forkCount"] is None:
            fork_Count = ""
        else:
            fork_Count = info["data"]["repository"]["forkCount"]

        if info["data"]["repository"]["stargazerCount"] is None:
            stars = ""
        else:
            stars = info["data"]["repository"]["stargazerCount"]

        # Error checking for main and master branch
        if (
            info["data"]["repository"]["object"] is None
            and info["data"]["repository"]["secondObject"] is not None
        ):
            commits = info["data"]["repository"]["secondObject"]["history"][
                "totalCount"
            ]
        elif (
            info["data"]["repository"]["secondObject"] is None
            and info["data"]["repository"]["object"] is not None
        ):
            commits = info["data"]["repository"]["object"]["history"]["totalCount"]
        else:
            commits = 0

    else:
        print(name + owner)
        print("Error Code " + str(request.status_code))

    if repo_name != None:
        scheme._set_value(i, "Name", repo_name)
    if repo_description != None:
        scheme._set_value(i, "Description", repo_description)
    if repo_url != None:
        scheme._set_value(i, "Url", repo_url)
    if is_Private != None:
        scheme._set_value(i, "Private", is_Private)
    if is_Forked != None:
        scheme._set_value(i, "Fork", is_Forked)
    if fork_Count != None:
        scheme._set_value(i, "ForkCount", fork_Count)
    if stars != None:
        scheme._set_value(i, "Stars", stars)

    if commits != None:
        scheme._set_value(i, "Commits", commits)
    else:
        scheme._set_value(i, "Commits", None)

    scheme.to_csv("scheme_info", index=False, sep=",")
