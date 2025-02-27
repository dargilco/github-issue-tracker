import os
import re
import requests
import argparse
from datetime import datetime
from typing import List, Any, Dict

# Update these lists with the repositories and labels you want to search for
REPOS = ["azure-sdk-for-python", "azure-sdk-for-net", "azure-sdk-for-java", "azure-sdk-for-js"]
LABELS = ["AI Projects", "AI Model Inference"]


# Extract the programming language part from a GitHub issue URL
def extract_language(url) -> str:
    match = re.search(r'azure-sdk-for-(\w+)/', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract language from URL: {url}")


# Print the resulting table to the console
def print_results(results: List[Dict[str, Any]], max_len: Dict[str, int]) -> None:
    print(
        f"{'user'.ljust(max_len['user'])} | " +
        f"{'language'.ljust(max_len['language'])} | " +
        f"{'label'.ljust(max_len['label'])} | " +
        f"{'number'.ljust(max_len['number'])} | " +
        f"{'title'.ljust(max_len['title'])} | " +
        f"{'created'.ljust(max_len['created'])} | " +
        "url"
    )
    print(
        f"{'-' * max_len['user']} + " +
        f"{'-' * max_len['language']} + " +
        f"{'-' * max_len['label']} + " +
        f"{'-' * max_len['number']} + " +
        f"{'-' * max_len['title']} + " +
        f"{'-' * max_len['created']} + " +
        f"{'-' * max_len['url']}"
    )
    for result in results:
        print(
            f"{result['user'].ljust(max_len['user']) if result['user'] else 'UNASSIGNED'.ljust(max_len['user'])} | "
            f"{result['language'].ljust(max_len['language'])} | "
            f"{result['label'].ljust(max_len['label']) if result['label'] else 'NO LABELS'.ljust(max_len['label'])} | "
            f"{result['number'].ljust(max_len['number'])} | "
            f"{result['title'].ljust(max_len['title'])} | "
            f"{result['created'].ljust(max_len['created'])} | "
            f"{result['url'].ljust(max_len['url'])}"
        )


def main() -> None:

    # Parse input argument. We support sorting by multiple columns, separated by comma
    parser = argparse.ArgumentParser(
        description=f"List open GitHub issues in repositories {', '.join(REPOS)}.\nOnly issues with labels {', '.join(LABELS)} are shown.\nYou first need to set the environment variable GITHUB_TOKEN.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--sort", type=str, required=False, help="Sort by any column name, like '-s name'. Or sort by multiple columns, separated by comma, like '-s name,label'")
    parser.add_argument("-r", "--reverse", action='store_true', required=False, help="Reverse sort")
    args = parser.parse_args()
    if hasattr(args, 'help'):
        parser.print_help()
        return
    if args.sort:
        print(f"Sort by: {args.sort} {'(reversed)' if args.reverse else ''}\n")

    try:
        github_token = os.environ["GITHUB_TOKEN"]
    except KeyError:
        print(
            "\nERROR: environment variable GITHUB_TOKEN not defined.\n"
            "To get a GitHub token, and configure it for Single Sign On (SSO), do the following:\n"
            "(1) Go to https://github.com/settings/apps -> Personal access tokens -> Tokens (classic) -> Select 'Generate new toke'n, then click' Generate new token (classic)'.\n"
            "(2) After you created the token, go back to https://github.com/settings/apps -> Personal access tokens -> Tokens (classic) , then click on 'Configure SSO' on the right, and select 'Azure'.\n\n"
        )
        parser.print_help()
        return

    # Will hold the resulting table to print to console
    results: List[Dict[str, str]] = []

    # Will hold the max number of chars for each column, so we can align columns during printout
    result_max_len : Dict[str, int] = {
        "number": len("number"),
        "title":len("title"),
        "url": len("url"),
        "language": len("language"),
        "user": len("UNASSIGNED"),
        "label": len("label"),
        "created": len("created")
    }

    # Loop through all repos and labels and make one REST API call for each combination to get the list of open issues
    for repo in REPOS:
        for label in LABELS:

            # See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues
            headers = {
                "Authorization": f"token {github_token}"
            }
            url = f"https://api.github.com/repos/Azure/{repo}/issues"

            params = {
                "state": "open",
                "labels": label,
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed with status code: {response.status_code}, message: {response.text})")
                return

            issues = response.json()

            for issue in issues:
                # Skip pull requests. We only want to list GitHub issues
                if "/pull/" in issue['html_url']:
                    continue

                # Enable these two lines to dump the raw response in JSON format
                #import json
                #print(json.dumps(issue, indent=4))

                # We don't show all the labels, only the ones we care about as defined above
                labels: List[str] = []
                for label in issue['labels']:
                    if label['name'] in LABELS:
                        labels.append(label['name'])

                # Extract only the info you need from the result, to build one row in the output table
                result : Dict[str,str] = {
                    "number": str(issue['number']),
                    "title": issue['title'],
                    "url": issue['html_url'],
                    "language": extract_language(issue['html_url']),
                    "user": ", ".join([assignee['login'].lower() for assignee in issue['assignees']]),
                    "label": ", ".join(labels),
                    "created": datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ").date().strftime("%Y-%m-%d")
                }

                # Update the max length of each column if needed, so we can align columns during printout
                for key in result_max_len.keys():
                    if len(result[key]) > result_max_len[key]:
                        result_max_len[key] = len(result[key])

                results.append(result)

    # Sort the table (if required)
    if args.sort:
        sort_keys = [key.strip() for key in args.sort.split(',')]
        def sort_key_func(d):
            return tuple(d[key] for key in sort_keys)
        results.sort(key=sort_key_func, reverse=args.reverse)

    # Print the table to the console
    print_results(results, result_max_len)


if __name__ == "__main__":
    main()