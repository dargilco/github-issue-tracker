# Python script to list open GitHub issues in Azure repositories

## Usage

Run the script with `-h` or `--help` argument to get usage help:

```bash
python gh_issues.py -h
```

You will see the following:

```txt
usage: gh_issues.py [-h] [-s SORT] [-r] [-f] [-a] [-n] [-c] [-t HTML]

List open GitHub issues in repositories azure-sdk-for-python, azure-sdk-for-net, azure-sdk-for-java, azure-sdk-for-js.
Only issues with labels AI Agents, AI Projects are shown.

options:
  -h, --help            show this help message and exit
  -s SORT, --sort SORT  Sort by any column name, like '-s user'. Or sort by multiple columns, separated by comma, like '-s user,language'
  -r, --reverse         Reverse sort
  -f, --no-features     Do not include issues labeled `feature-request`
  -a, --no-issue-addressed
                        Do not include issues labeled `issue-addressed`
  -n, --no-needs-author-feedback
                        Do not include issues labeled `needs-author-feedback`
  -c, --closed          Show closed issues instead of opened issues
  -t HTML, --html HTML  Export results as HTML to this file name, for example '-t report.html'
```
<!--
## Set environment variable GITHUB_TOKEN before running the script

To get a GitHub token, and configure it for Single Sign On (SSO) to the Azure group (https://github.com/Azure), do the following:

1. Go to https://github.com/settings/apps -> `Personal access tokens` -> `Tokens (classic)` -> Select `Generate new token`, then click `Generate new token (classic)`."
1. After you created the token, go back to https://github.com/settings/apps -> `Personal access tokens` -> `Tokens (classic)` , then click on `Configure SSO` on the right, and select `Azure`.
-->

## Example output

This is an example output for the command `python gh_issues.py -s days,user  -f -a`:

```text
Repos: azure-sdk-for-python, azure-sdk-for-net, azure-sdk-for-java, azure-sdk-for-js
Labels: AI Projects, AI Model Inference
Excluding labels: feature-request, issue-addressed
Issue state: open
Sort by: days,user

user       | language | label              | number | title                                                                                        | days | created    | url
---------- + -------- + ------------------ + ------ + -------------------------------------------------------------------------------------------- + ---- + ---------- + ----------------------------------------------------------
UNASSIGNED | net      | AI Projects        | 49265  | [QUERY] AI Foundry Tracing with C#                                                           | 1    | 2025-04-07 | https://github.com/Azure/azure-sdk-for-net/issues/49265
jhakulin   | net      | AI Projects        | 49143  | [QUERY] AI Agent Service SDK - GetThreads()                                                  | 9    | 2025-03-30 | https://github.com/Azure/azure-sdk-for-net/issues/49143
howieleung | python   | AI Projects        | 40247  | Azure agent / open AI vector stores: add timeout when attaching file to vector stores        | 12   | 2025-03-27 | https://github.com/Azure/azure-sdk-for-python/issues/40247
trangevi   | python   | AI Model Inference | 40113  | azure-ai-inference: token count attributes missing for streaming calls in traces             | 21   | 2025-03-18 | https://github.com/Azure/azure-sdk-for-python/issues/40113
lmolkova   | java     | AI Model Inference | 44602  | Document AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED env var in azure-ai-inference        | 28   | 2025-03-11 | https://github.com/Azure/azure-sdk-for-java/issues/44602
marygao    | js       | AI Model Inference | 33333  | [@azure-rest/ai-inference] missing exported/re-exported types                                | 28   | 2025-03-11 | https://github.com/Azure/azure-sdk-for-js/issues/33333
trangevi   | python   | AI Model Inference | 39928  | Audio completions samples do not work with Phi 4.0 Multimodal Instruct Serverless deployment | 35   | 2025-03-04 | https://github.com/Azure/azure-sdk-for-python/issues/39928
trangevi   | python   | AI Model Inference | 39900  | Invalid Input in sample_chat_completions_with_audio_data.py                                  | 39   | 2025-02-28 | https://github.com/Azure/azure-sdk-for-python/issues/39900
trangevi   | net      | AI Model Inference | 48414  | Inconsistent API results in CompleteStreamingAsync                                           | 43   | 2025-02-24 | https://github.com/Azure/azure-sdk-for-net/issues/48414
```