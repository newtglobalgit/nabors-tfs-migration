from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.c4 import Container, SystemBoundary, Relationship

graph_attr = {
    "splines": "spline",
}

with Diagram("TFS Migration - Architecture", direction="LR", graph_attr=graph_attr):
    with Cluster("Migration"):
        with Cluster("On-Premise"):
            with SystemBoundary("TFS 2013"):
                TFS = Container(
                    name="Team Foundation Server 2013",
                    technology="On-premise SCM / Working boards",
                    description="Manages the projects on Team Foundation Server version 2013",
                )
        with Cluster("Azure Cloud"):
            with SystemBoundary("Azure DevOps"):
                boards = Container(
                    name="Azure Boards",
                    technology="Azure DevOps",
                    description="Azure DevOps account which manages the Work Items on projects basis migration from Team Foundation Server 2013",
                )

        with Cluster("Source Code Management"):
            with Cluster("GitHub"):
                with SystemBoundary("Source Control"):
                    github_lfs = Container(
                        name="LFS",
                        technology="Large file storage",
                        description="large file storage solution which manages the source code binaries and ascii on projects migration from Team Foundation Server 2013",
                    )
                    github = Container(
                        name="Repository",
                        technology="SCM",
                        description="Source code management solution which manages the source code on projects migration from Team Foundation Server 2013",
                    )

    github << Relationship("Source code migration") << TFS >> Relationship("Work Item migration") >> boards
    github_lfs << Relationship("Binary / ASCII file migration") << TFS