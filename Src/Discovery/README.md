## Description:
TFS (Team Foundation Server) 2013 server discovery reports are generated for the active tfs transformation progress tracking.

## Flow Chart

```mermaid
graph LR
A[TFS on-premise Server] -- Source Code Discovery --> B[Discovery Reports for source code]
A -- Work Item Discovery --> C[Discovery Reports for work items]
A -- User / Access control Discovery --> D[Discovery Reports for Github Organization]
```

## Pre-requisites:
- python - Minimum 3.9 or Greater
- packages - requirement.txt
- Github credentials - 1. User id and token
- git tfs 

## Code file details:
main.py - performs the source code migration and workitem migration.
library.py - defines the methods which are needed and reusability of methods across the execution.
credentials.py - defines the secrets / sensitive details in the file store.

## Program execution in sequential order: 
First of all we have to execute 

> pip install -r requirements.txt
> python main.py

This script will give a output list of all the repos that is there in remote tfs server.

## Goals:
- Discovery of the Team Foundation Version Control[TFVC] source code with history of commits and branches to GitHUB repository.
- Discovery of the Team Foundation Version Control[TFVC] work items with history of issues and changes to Azure DevOps Services.
- Discovery of the Team Foundation server [TFVC] User and access control to GitHUB and ADO