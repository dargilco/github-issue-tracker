import os
import re
import requests
import argparse
import pytz
from datetime import datetime, timezone, timedelta
from typing import List, Any, Dict

# Update these lists with the repositories you want to search
REPOS = ["azure-sdk-for-python", "azure-sdk-for-net", "azure-sdk-for-java", "azure-sdk-for-js"]

# And the labels you want to search
LABELS = ["AI Projects", "AI Model Inference"]

# Additional labels you want to show in the output table, in the "label" column.
ADDITIONAL_LABELS= ["feature-request", "issue-addressed"]


# Extract the programming language part from a GitHub issue URL
def extract_language(url) -> str:
    match = re.search(r'azure-sdk-for-(\w+)/', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract language from URL: {url}")

def print_console_report_header(args) -> None:
    print(f"Repos: {', '.join(REPOS)}")
    print(f"Labels: {', '.join(LABELS)}")
    if args.no_features and args.no_issue_addressed:
        print(f"Excluding labels: feature-request, issue-addressed")
    elif args.no_features:
        print(f"Excluding label: feature-request")
    elif args.no_issue_addressed:
        print(f"Excluding label: issue-addressed")
    if args.closed:
        print(f"Issue state: closed")
    else:
        print(f"Issue state: open")
    if args.html:
        print(f"Output HTML file: {args.html}")
    if args.sort:
        print(f"Sort by: {args.sort} {'(reversed)' if args.reverse else ''}")
    print("")


# Print the resulting table to the console
def print_console_report(results: List[Dict[str, Any]], max_len: Dict[str, int]) -> None:

    is_closed: bool  = 'closed' in results[0]

    print(
        f"{'user'.ljust(max_len['user'])} | " +
        f"{'language'.ljust(max_len['language'])} | " +
        f"{'label'.ljust(max_len['label'])} | " +
        f"{'number'.ljust(max_len['number'])} | " +
        f"{'title'.ljust(max_len['title'])} | " +
        f"{'days'.ljust(max_len['days'])} | " +
        f"{'closed'.ljust(max_len['closed']) if is_closed else 'created'.ljust(max_len['created'])} | " +
        "url"
    )
    print(
        f"{'-' * max_len['user']} + " +
        f"{'-' * max_len['language']} + " +
        f"{'-' * max_len['label']} + " +
        f"{'-' * max_len['number']} + " +
        f"{'-' * max_len['title']} + " +
        f"{'-' * max_len['days']} + " +
        f"{'-' * max_len['closed'] if is_closed else '-' * max_len['created']} + " +
        f"{'-' * max_len['url']}"
    )
    for result in results:
        print(
            f"{result['user'].ljust(max_len['user']) if result['user'] else 'UNASSIGNED'.ljust(max_len['user'])} | "
            f"{result['language'].ljust(max_len['language'])} | "
            f"{result['label'].ljust(max_len['label']) if result['label'] else 'NO LABELS'.ljust(max_len['label'])} | "
            f"{result['number'].ljust(max_len['number'])} | "
            f"{result['title'].ljust(max_len['title'])} | "
            f"{result['days'].ljust(max_len['days'])} | "
            f"{result['closed'].ljust(max_len['closed']) if is_closed else result['created'].ljust(max_len['created'])} | "
            f"{result['url'].ljust(max_len['url'])}"
        )


def print_html_report(args, results: List[Dict[str, Any]], max_len: Dict[str, int], filename: str) -> None:
    is_closed: bool = 'closed' in results[0]

    with open(filename, 'w') as f:

        pacific = pytz.timezone("US/Pacific")
        current_time = datetime.now(timezone.utc).astimezone(pacific).strftime("%Y-%m-%d %H:%M:%S %Z")

        f.write("<table border='1' style='border-collapse: collapse;'>\n<tr>")
        f.write(f"<td><b>Generated on:</b></td><td>{current_time}</td></tr>\n")
        f.write(f"<tr><td><b>Repos:</b></td><td>{', '.join(REPOS)}</td></tr>\n")
        f.write(f"<tr><td><b>Labels:</b></td><td>{', '.join(LABELS)}</td></tr>\n")
        if args.no_features and args.no_issue_addressed:
            f.write(f"<tr><td><b>Excluding labels:</b></td><td>feature-request, issue-addressed</td></tr>\n")
        elif args.no_features:
            f.write(f"<tr><td><b>Excluding label:</b></td><td>feature-request</td></tr>\n")
        elif args.no_issue_addressed:
            f.write(f"<tr><td><b>Excluding label:</b></td><td>issue-addressed</td></tr>\n")
        if args.closed:
            f.write(f"<tr><td><b>Issue state:</b></td><td>closed</td></tr>\n")
        else:
            f.write(f"<tr><td><b>Issue state:</b></td><td>open</td></tr>\n")
        if args.html:
            f.write(f"<tr><td><b>Output HTML file:</b></td><td>{args.html}</td></tr>\n")
        if args.sort:
            f.write(f"<tr><td><b>Sort by:</b></td><td>{args.sort} {'(reversed)' if args.reverse else ''}</td></tr>\n")
        f.write("</table><br>\n")

        f.write("<html><body><table border='1' style='border-collapse: collapse;'>\n")
        f.write("<tr style='background-color: lightblue;'>")
        f.write(f"<th>{'user'.ljust(max_len['user'])}</th>")
        f.write(f"<th>{'language'.ljust(max_len['language'])}</th>")
        f.write(f"<th>{'label'.ljust(max_len['label'])}</th>")
        f.write(f"<th>{'number'.ljust(max_len['number'])}</th>")
        f.write(f"<th>{'title'.ljust(max_len['title'])}</th>")
        f.write(f"<th>{'days'.ljust(max_len['days'])}</th>")
        f.write(f"<th>{'closed'.ljust(max_len['closed']) if is_closed else 'created'.ljust(max_len['created'])}</th>")
        f.write("<th>url</th>")
        f.write("</tr>\n")

        for result in results:
            f.write("<tr>")
            f.write(f"<td>{result['user'] if result['user'] else 'UNASSIGNED'}</td>")
            f.write(f"<td>{result['language']}</td>")
            f.write(f"<td>{result['label'] if result['label'] else 'NO LABELS'}</td>")
            f.write(f"<td>{result['number']}</td>")
            f.write(f"<td>{result['title']}</td>")
            f.write(f"<td>{result['days']}</td>")
            f.write(f"<td>{result['closed'] if is_closed else result['created']}</td>")
            f.write(f"<td><a href='{result['url']}'>{result['url']}</a></td>")
            #f.write(f"<td><a href='{result['url']}' target='_blank'>{result['url']}</a></td>")
            f.write("</tr>\n")

        f.write("</table></body></html>\n")


def main() -> None:

    # Parse input argument. We support sorting by multiple columns, separated by comma
    parser = argparse.ArgumentParser(
        description=f"List open GitHub issues in repositories {', '.join(REPOS)}.\nOnly issues with labels {', '.join(LABELS)} are shown.\nYou first need to set the environment variable GITHUB_TOKEN.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--sort", type=str, required=False, help="Sort by any column name, like '-s user'. Or sort by multiple columns, separated by comma, like '-s user,language'")
    parser.add_argument("-r", "--reverse", action='store_true', required=False, help="Reverse sort")
    parser.add_argument("-f", "--no-features", action='store_true', required=False, help="Do not include issues labeled `feature-request`")
    parser.add_argument("-a", "--no-issue-addressed", action='store_true', required=False, help="Do not include issues labeled `issue-addressed`")
    parser.add_argument("-c", "--closed", action='store_true', required=False, help="Show closed issues instead of opened issues")
    parser.add_argument("-t", "--html", type=str, required=False, help="Export results as HTML to this file name, for example '-t report.html'")

    args = parser.parse_args()
    if hasattr(args, 'help'):
        parser.print_help()
        return

    print_console_report_header(args)

    try:
        github_token = os.environ["GITHUB_TOKEN"]
    except KeyError:
        print(
            "\nERROR: environment variable GITHUB_TOKEN not defined.\n"
            "To get a GitHub token, and configure it for Single Sign On (SSO) to the Azure group (https://github.com/Azure), do the following:\n"
            "(1) Go to https://github.com/settings/apps -> Personal access tokens -> Tokens (classic) -> Select 'Generate new token', then click' Generate new token (classic)'.\n"
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
        "days": len("days"),
    }

    if args.closed:
        result_max_len["closed"] = len("closed")
    else:
        result_max_len["created"] = len("created")

    # Loop through all repos and labels and make one REST API call for each combination to get the list of open issues
    for repo in REPOS:
        for label in LABELS:

            # See https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues
            headers = {
                "Authorization": f"token {github_token}"
            }
            url = f"https://api.github.com/repos/Azure/{repo}/issues"

            params = {
                "state": "closed" if args.closed else "open",
                "labels": label,
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed with status code: {response.status_code}, message: {response.text})")
                return

            issues = response.json()

            # Enable this for project service response in JSON format
            #import json
            #print(json.dumps(issues, indent=4))

            for issue in issues:
                # Skip pull requests. We only want to list GitHub issues
                if "/pull/" in issue['html_url']:
                    continue

                # Enable these two lines to dump the raw response in JSON format
                #import json
                #print(json.dumps(issue, indent=4))

                # Skip showing issues labeled as `feature-request` if the user requested it
                if (args.no_features and 'feature-request' in [label['name'] for label in issue['labels']]):
                    continue

                # Skip showing issues labeled as `issue-addressed` if the user requested it
                if (args.no_issue_addressed and 'issue-addressed' in [label['name'] for label in issue['labels']]):
                    continue

                # We don't show all the labels, only the ones we care about as defined above.
                # First show labels from LABELS, then show labels from ADDITIONAL_LABELS.
                labels: List[str] = []
                for label in issue['labels']:
                    if label['name'] in LABELS:
                        labels.append(label['name'])
                for label in issue['labels']:
                    if label['name'] in ADDITIONAL_LABELS:
                        labels.append(label['name'])

                # Parse the created date and convert it to a datetime object, UTC time zone
                if (args.closed):
                    closed = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                    closed = closed.replace(tzinfo=timezone.utc)
                else:
                    created = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    created = created.replace(tzinfo=timezone.utc)


                # Extract only the info you need from the result, to build one row in the output table
                result : Dict[str,str] = {
                    "number": str(issue['number']),
                    "title": issue['title'],
                    "url": issue['html_url'],
                    "language": extract_language(issue['html_url']),
                    "user": ", ".join([assignee['login'].lower() for assignee in issue['assignees']]),
                    "label": ", ".join(labels),
                }
                if args.closed:
                    result["closed"] = closed.date().strftime("%Y-%m-%d")
                    result["days"] = str((datetime.now(timezone.utc).date() - closed.date()).days)
                else:
                    result["created"] = created.date().strftime("%Y-%m-%d")
                    result["days"] = str((datetime.now(timezone.utc).date() - created.date()).days)


                # Update the max length of each column if needed, so we can align columns during printout
                for key in result_max_len.keys():
                    if len(result[key]) > result_max_len[key]:
                        result_max_len[key] = len(result[key])

                results.append(result)

    # Sort the table (if required)
    if args.sort:
        sort_keys = [key.strip() for key in args.sort.split(',')]
        def sort_key_func(d):
            return tuple((int(d[key]) if (key == 'days' or key =='number') else d[key]) for key in sort_keys)
        results.sort(key=sort_key_func, reverse=args.reverse)

    # Print the table to the console
    print_console_report(results, result_max_len)

    if args.html:
        # Print the table to HTML file
        print_html_report(args, results, result_max_len, args.html)


if __name__ == "__main__":
    main()