# Python script to list open GitHub issues in Azure repositories

## Usage

Run the script with `-h` or `--help` argument to get usage help:

```bash
python gh_issues.py -h
```

You will see the following:

```txt
usage: gh_issues.py [-h] [-s SORT] [-r] [-n]

List open GitHub issues in repositories azure-sdk-for-python, azure-sdk-for-net, azure-sdk-for-java, azure-sdk-for-js.
Only issues with labels AI Projects, AI Model Inference are shown.
You first need to set the environment variable GITHUB_TOKEN.

options:
  -h, --help            show this help message and exit
  -s SORT, --sort SORT  Sort by any column name, like '-s user'. Or sort by multiple columns, separated by comma, like '-s user,language'
  -r, --reverse         Reverse sort
  -n, --no-features     Do not include issues labeled `feature-request`
```

## Set environment variable GITHUB_TOKEN before running the script

To get a GitHub token, and configure it for Single Sign On (SSO) to the Azure group (https://github.com/Azure), do the following:

1. Go to https://github.com/settings/apps -> `Personal access tokens` -> `Tokens (classic)` -> Select `Generate new token`, then click `Generate new token (classic)`."
1. After you created the token, go back to https://github.com/settings/apps -> `Personal access tokens` -> `Tokens (classic)` , then click on `Configure SSO` on the right, and select `Azure`.

## Example output

This is an example output for the command `python gh_issues.py -s days,label --no-features`:

```text
Repos: azure-sdk-for-python, azure-sdk-for-net, azure-sdk-for-java, azure-sdk-for-js
Labels: AI Projects, AI Model Inference
Excluding label: feature-request
Sort by: days,label

user       | language | label              | number | title                                                                                                      | days | created    | url
---------- + -------- + ------------------ + ------ + ---------------------------------------------------------------------------------------------------------- + ---- + ---------- + ----------------------------------------------------------
trangevi   | python   | AI Model Inference | 39958  | [azure-ai-inference] Citations not available in ChatCompletionClient Complete call result                  | 5    | 2025-03-06 | https://github.com/Azure/azure-sdk-for-python/issues/39958
trangevi   | python   | AI Model Inference | 39928  | Audio completions samples do not work with Phi 4.0 Multimodal Instruct Serverless deployment               | 7    | 2025-03-04 | https://github.com/Azure/azure-sdk-for-python/issues/39928
nick863    | python   | AI Projects        | 39887  | azure-ai-projects 403 nginx forbidden returned for get_agent                                               | 12   | 2025-02-27 | https://github.com/Azure/azure-sdk-for-python/issues/39887
trangevi   | net      | AI Model Inference | 48414  | Inconsistent API results in CompleteStreamingAsync                                                         | 15   | 2025-02-24 | https://github.com/Azure/azure-sdk-for-net/issues/48414
m-hietala  | python   | AI Projects        | 39833  | Agent Service Tracing: 'AIProjectClient' object does not support the context manager protocol              | 17   | 2025-02-22 | https://github.com/Azure/azure-sdk-for-python/issues/39833
jhakulin   | python   | AI Projects        | 39816  | AzureAISearchTool fails with missing_required_parameter - AML connections are required for AI Search tool. | 18   | 2025-02-21 | https://github.com/Azure/azure-sdk-for-python/issues/39816
nick863    | python   | AI Projects        | 39778  | AI Project client says "Invalid tool value(s): azure_function"                                             | 21   | 2025-02-18 | https://github.com/Azure/azure-sdk-for-python/issues/39778
lmolkova   | python   | AI Projects        | 39753  | Agents tracing: we don't suppress generic spans                                                            | 25   | 2025-02-14 | https://github.com/Azure/azure-sdk-for-python/issues/39753
```