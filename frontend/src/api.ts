export type Overview = {
    product: string;
    version: string;
    status: string;
    workflow: string[];
};
export type Project = {
    id: number;
    name: string,
    repositoryOwner: string,
    repositoryName: string,
    defaultBranch: string,
    createdAt: string
};
type ProjectInput = Omit<Project, "id" | "createdAt">;

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080";

export class ApiError extends Error {
    status: number;

    constructor(message: string, status: number) {
        super(message);
        this.status = status;
    }
}

export async function getOverview(): Promise<Overview> {
    const response = await fetch(`${apiBaseUrl}/api/overview`);
    if (!response.ok) {
        throw new ApiError(`Backend returned ${response.status}`, response.status);
    }
    return response.json() as Promise<Overview>;
}

export async function getProjects(): Promise<Project[]> {
    const response = await fetch(`${apiBaseUrl}/api/projects`);
    if (!response.ok) {
        throw new ApiError(`Backend returned ${response.status}`, response.status);
    }
    return response.json() as Promise<Project[]>;
}

export async function createProject(input: ProjectInput): Promise<Project> {
    const response = await fetch(`${apiBaseUrl}/api/projects`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(input)
    });
    if (!response.ok) {
        throw new ApiError(`Backend returned ${response.status}`, response.status);
    }
    return response.json() as Promise<Project>;
}

