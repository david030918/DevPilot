import {getProjects} from "../api";
import {useQuery} from "@tanstack/react-query";

export default function ProjectsPage() {
    const projects = useQuery({
        queryKey: ["projects"],
        queryFn: getProjects,
    });
    if (projects.isPending) {
        return <div>Loading...</div>
    }
    if (projects.isError) {
        return <div>Error: {projects.error.message}</div>
    }
    if (!projects.data || projects.data.length === 0) {
        return <div>No projects found</div>
    }

    return (
        <div>
            <h1>Projects</h1>
            {projects.data.map((project) => (
                <div key={project.id}>
                    <h2>{project.name}</h2>
                    <p>{project.repositoryOwner}</p>
                </div>
            ))}
        </div>
    );
}