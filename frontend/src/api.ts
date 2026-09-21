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

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080";

export async function getOverview(): Promise<Overview> {
    const response = await fetch(`${apiBaseUrl}/api/overview`);
    if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
    }
    return response.json() as Promise<Overview>;
}

export async function getProjects(): Promise<Project[]> {
    const response = await fetch(`${apiBaseUrl}/api/projects`);
    if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
    }
    return response.json() as Promise<Project[]>;
}

