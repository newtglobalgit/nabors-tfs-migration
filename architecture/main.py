from diagrams import Diagram
from diagrams.c4 import Container, SystemBoundary, Relationship

graph_attr = {
    "splines": "spline",
}

with Diagram("TFS Migration - Architecture", direction="TB", graph_attr=graph_attr):
    with SystemBoundary("TFS 2013"):
        TFS = Container(
            name="Team Foundation Server 2013",
            technology="On-premise SCM / Working boards",
            description="Manages the projects on Team Foundation Server version 2013",
        )

    with SystemBoundary("Azure DevOps"):
        boards = Container(
            name="Azure Boards",
            technology="Azure DevOps",
            description="Azure DevOps account which manages the Work Items on projects basis migration from Team Foundation Server 2013",
        )

    with SystemBoundary("GitHub"):
        github = Container(
            name="GitHub",
            technology="SCM",
            description="Source code management solution which manages the source code on projects migration from Team Foundation Server 2013",
        )

    TFS >> Relationship("Work Item migration") >> boards
    TFS >> Relationship("Source code migration") >> github
