# Python script to list open GitHub issues in Azure repositories

## Usage help

Run the script with `-h` or `--help` argument to get usage help:

```python
python gh_issues.py -h
```

You will see the following:

```
usage: gh_issues.py [-h] [-s SORT] [-r]

List open GitHub issues in repositories azure-sdk-for-python, azure-sdk-for-net, azure-sdk-for-java, azure-sdk-for-js.
Only issues with labels AI Projects, AI Model Inference are shown.
You first need to set the environment variable GITHUB_TOKEN.

options:
  -h, --help            show this help message and exit
  -s SORT, --sort SORT  Sort by any column name, like '-s user'. Or sort by multiple columns, separated by comma, like '-s user,language'
  -r, --reverse         Reverse sort
```

## Set environment variable GITHUB_TOKEN before running the script

To get a GitHub token, and configure it for Single Sign On (SSO) to the Azure group (https://github.com/Azure), do the following:

1. Go to https://github.com/settings/apps -> Personal access tokens -> Tokens (classic) -> Select `Generate new toke`, then click `Generate new token (classic)`.\n"
1. After you created the token, go back to https://github.com/settings/apps -> Personal access tokens -> Tokens (classic) , then click on `Configure SSO` on the right, and select `Azure`.\n\n"

## Example output

```text
Sort by: user,language

user       | language | label              | number | title                                                                                                      | created    | url
---------- + -------- + ------------------ + ------ + ---------------------------------------------------------------------------------------------------------- + ---------- + ----------------------------------------------------------
dargilco   | python   | AI Projects        | 39782  | Prerequisite lists "Contributor" role but "Azure AI Developer" role needed                                 | 2025-02-18 | https://github.com/Azure/azure-sdk-for-python/issues/39782
jhakulin   | python   | AI Projects        | 39816  | AzureAISearchTool fails with missing_required_parameter - AML connections are required for AI Search tool. | 2025-02-21 | https://github.com/Azure/azure-sdk-for-python/issues/39816
lmolkova   | python   | AI Projects        | 39753  | Agents tracing: we don't suppress generic spans                                                            | 2025-02-14 | https://github.com/Azure/azure-sdk-for-python/issues/39753
m-hietala  | python   | AI Projects        | 39833  | Agent Service Tracing: 'AIProjectClient' object does not support the context manager protocol              | 2025-02-22 | https://github.com/Azure/azure-sdk-for-python/issues/39833
nick863    | net      | AI Projects        | 48333  | [BUG] AI Agent SDK fails to deserialize file search when using streaming                                   | 2025-02-18 | https://github.com/Azure/azure-sdk-for-net/issues/48333
nick863    | python   | AI Projects        | 39778  | AI Project client says "Invalid tool value(s): azure_function"                                             | 2025-02-18 | https://github.com/Azure/azure-sdk-for-python/issues/39778
trangevi   | net      | AI Model Inference | 48414  | Inconsistent API results in CompleteStreamingAsync                                                         | 2025-02-24 | https://github.com/Azure/azure-sdk-for-net/issues/48414
trangevi   | net      | AI Model Inference | 48405  | [FEATURE REQ] Allow the API version in AzureAIInferenceClientOptions to be configurable                    | 2025-02-23 | https://github.com/Azure/azure-sdk-for-net/issues/48405
trangevi   | net      | AI Model Inference | 47069  | [FEATURE REQ] Resolve Native AOT Warnings in Azure.AI.Inference                                            | 2024-11-11 | https://github.com/Azure/azure-sdk-for-net/issues/47069
trangevi   | net      | AI Model Inference | 46830  | [BUG] Impossible to correctly handle parallel tool calls with Azure.AI.Inference                           | 2024-10-24 | https://github.com/Azure/azure-sdk-for-net/issues/46830
trangevi   | python   | AI Model Inference | 39835  | ResourceNotFoundError exception raised on client.complete method                                           | 2025-02-23 | https://github.com/Azure/azure-sdk-for-python/issues/39835

```