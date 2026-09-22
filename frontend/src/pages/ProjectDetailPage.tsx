import {useParams} from "react-router-dom";

export default function ProjectDetailPage() {
    const {projectId} = useParams();

    return (
        <div>
            Project Detail Page for Project ID: {projectId}
        </div>
    );
}