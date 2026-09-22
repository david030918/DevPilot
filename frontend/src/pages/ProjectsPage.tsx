import {getProjects} from "../api";
import {useQuery} from "@tanstack/react-query";
import CreateProjectForm from "../projects/CreateProjectForm";
import {Link} from "react-router-dom";

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
        return (
            <div>No projects found
                <CreateProjectForm/>
            </div>
        )
    }

    return (
        <div>
            <h1>Projects</h1>
            {projects.data.map((project) => (
                <Link to={"/projects/" + project.id} key={project.id}>{project.name}</Link>
            ))}

            <CreateProjectForm/>

        </div>
    );
}