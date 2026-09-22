import {useParams} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {getProjectById} from "../api";

export default function ProjectDetailPage() {
    const {projectId} = useParams();
    const project = useQuery({
        enabled: projectId !== undefined,
        queryKey: ["projects", projectId],
        queryFn: () => getProjectById(Number(projectId)),
    });
    if (project.isPending) {
        return <div>Loading...</div>
    }
    if (project.isError) {
        return <div>Error: {project.error.message}</div>
    }
    if (!project.data) {
        return (
            <div>No projects found </div>
        )
    }

    return (
        <div>
            Project Detail Page for Project ID: {projectId}

            <h2>{project.data.name}</h2>
            <p>{project.data.repositoryOwner}</p>
        </div>


    );
}