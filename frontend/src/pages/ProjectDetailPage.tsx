import {useParams} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";
import {ApiError, getProjectById} from "../api";

export default function ProjectDetailPage() {
    const {projectId} = useParams();
    const numericProjectId = Number(projectId);

    const isValidProjectId =
        Number.isInteger(numericProjectId) &&
        numericProjectId > 0;

    const project = useQuery({
        enabled: isValidProjectId,
        queryKey: ["projects", projectId],
        queryFn: () => getProjectById(numericProjectId),
    });
    if (!isValidProjectId)
        return (
            <div>Invalid project ID</div>
        )

    if (project.isPending) {
        return <div>Loading...</div>
    }
    if (project.error instanceof ApiError && project.error.status === 404) {
        return <div>Project not found</div>;
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