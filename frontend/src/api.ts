export type Overview = {
  product: string;
  version: string;
  status: string;
  workflow: string[];
};

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080";

export async function getOverview(): Promise<Overview> {
  const response = await fetch(`${apiBaseUrl}/api/overview`);
  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}`);
  }
  return response.json() as Promise<Overview>;
}

