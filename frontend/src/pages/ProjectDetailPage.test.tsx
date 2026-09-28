import {render, screen} from "@testing-library/react";
import ProjectDetailPage from "./ProjectDetailPage";
import {MemoryRouter, Route, Routes} from "react-router-dom";
import {expect, test, vi} from "vitest";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {ApiError, getProjectById} from "../api";

test("shows an error for an invalid project id", () => {
    const queryClient = new QueryClient();
    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects/abc"]}>
                <Routes>
                    <Route
                        path="/projects/:projectId"
                        element={<ProjectDetailPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    expect(
        screen.getByText("Invalid project ID")
    ).toBeInTheDocument();
});

vi.mock("../api", async (importOriginal) => {
    const actual = await importOriginal<typeof import("../api")>();

    return {
        ...actual,
        getProjectById: vi.fn(),
    };
});
test("shows project details for a valid project id", async () => {
    const queryClient = new QueryClient();
    const fakeProject = {
        id: 123,
        name: "Test Project",
        repositoryOwner: "test-owner",
        repositoryName: "test-repository",
        defaultBranch: "main",
        createdAt: "2026-09-23T00:00:00Z",
    };
    vi.mocked(getProjectById).mockResolvedValue(fakeProject);
    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects/123"]}>
                <Routes>
                    <Route
                        path="/projects/:projectId"
                        element={<ProjectDetailPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    expect(
        await screen.findByText("Test Project")
    ).toBeInTheDocument();
})

test("shows project not found when the API returns 404", async () => {
    // Arrange
    // getProjectById mockRejectedValue(...)

    // Act
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
            },
        },
    });
    const fakeProject = new ApiError("Backend returned 404", 404);
    vi.mocked(getProjectById).mockRejectedValue(fakeProject);
    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects/999"]}>
                <Routes>
                    <Route
                        path="/projects/:projectId"
                        element={<ProjectDetailPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    // Assert
    expect(
        await screen.findByText("Project not found")
    ).toBeInTheDocument();
});