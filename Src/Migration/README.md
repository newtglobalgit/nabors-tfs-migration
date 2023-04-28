## Description:
TFS (Team Foundation Server) 2013 server project migration with work items using the python codes available here.

## Flow Chart

```mermaid
graph LR
A[TFS on-premise Server] -- Source Code Migration --> B[GitHub Organization source code migration]
A -- Work Item Migration --> C[ADO work items migration]
A -- User / Access control Migration --> D[Github Organization user privilege migration]
A -- User / Access control Migration --> E[ADO user privilege migration]
```

## Pre-requisites:
- python - Minimum 3.9 or Greater
- packages - requirements.txt
- Github credentials - 1. User id and token
- Ado credentials - Org, token
- git tfs
- Visual Studio 2013/2019/2022
- Team Foundation Power Tools Extension for Visual Studio

## Code file details:
- main.py - performs the source code migration and work item migration.
- library.py - defines the methods which are needed and reusability of methods across the execution.
- credentials.py - defines the secrets / sensitive details in the file store.

## Program execution in sequential order: 

> pip install -r requirements.txt

> python main.py

## Goals:
- Migration of the Team Foundation Version Control[TFVC] source code with history of commits and branches to GitHUB repository.
- Migration of the Team Foundation Version Control[TFVC] work items with history of issues and changes to Azure DevOps Services.
- Migration of the Team Foundation server [TFVC] User and access control to GitHUB and ADO