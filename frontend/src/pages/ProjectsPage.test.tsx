import {expect, test, vi} from "vitest";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {render, screen} from "@testing-library/react";
import {MemoryRouter, Route, Routes} from "react-router-dom";
import ProjectsPage from "./ProjectsPage";
import {ApiError, createProject, getProjects} from "../api";
import userEvent from "@testing-library/user-event";

vi.mock("../api", async (importOriginal) => {
    const actual = await importOriginal<typeof import("../api")>();

    return {
        ...actual,
        getProjects: vi.fn(),
        createProject: vi.fn(),
    };
});
test("return Empty state.", async () => {
    const queryClient = new QueryClient();
    vi.mocked(getProjects).mockResolvedValue([]);

    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects"]}>
                <Routes>
                    <Route
                        path="/projects"
                        element={<ProjectsPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    expect(
        await screen.findByText("No projects found")
    ).toBeInTheDocument();
});

test("shows project list when projects are returned", async () => {
    const queryClient = new QueryClient();
    vi.mocked(getProjects).mockResolvedValue([
        {
            id: 1,
            name: "DevPilot",
            repositoryOwner: "david",
            repositoryName: "DevPilot",
            defaultBranch: "main",
            createdAt: "2023-09-01T00:00:00Z",
        }, {
            id: 2,
            name: "DevPilot2",
            repositoryOwner: "david",
            repositoryName: "DevPilot",
            defaultBranch: "sub",
            createdAt: "2023-09-01T10:00:00Z",
        },
    ]);

    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects"]}>
                <Routes>
                    <Route
                        path="/projects"
                        element={<ProjectsPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    expect(
        await screen.findByText("DevPilot")
    ).toBeInTheDocument();

    expect(
        await screen.findByText("DevPilot2")
    ).toBeInTheDocument();
});

test("shows conflict error when creating a duplicate project", async () => {
    // Arrange
    const user = userEvent.setup();
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
            },
        },
    });
    const fakeProject = new ApiError("Conflict", 409);
    vi.mocked(getProjects).mockResolvedValue([]);
    vi.mocked(createProject).mockRejectedValue(fakeProject);

    // Act
    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects"]}>
                <Routes>
                    <Route
                        path="/projects"
                        element={<ProjectsPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    await user.type(await screen.findByLabelText("Name"), "DevPilot")
    await user.type(await screen.findByLabelText("Repository Owner"), "david");
    await user.type(await screen.findByLabelText("Repository Name"), "DevPilot");
    await user.click(
        screen.getByRole("button", {name: "Create Project"})
    );

    // Assert
    expect(await screen.findByText("No projects found")).toBeInTheDocument();
    expect(
        await screen.findByText("Project already exists")
    ).toBeInTheDocument();
});

test("show projects when it created", async () => {
    // Arrange
    const user = userEvent.setup();
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
            },
        },
    });
    vi.mocked(getProjects).mockResolvedValueOnce([]).mockResolvedValueOnce([{
        id: 2,
        name: "DevPilot",
        repositoryOwner: "david",
        repositoryName: "DevPilot",
        defaultBranch: "sub",
        createdAt: "2023-09-01T10:00:00Z",
    }]);
    vi.mocked(createProject).mockResolvedValue({
        id: 2,
        name: "DevPilot",
        repositoryOwner: "david",
        repositoryName: "DevPilot",
        defaultBranch: "sub",
        createdAt: "2023-09-01T10:00:00Z",
    })

    // Act
    render(
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={["/projects"]}>
                <Routes>
                    <Route
                        path="/projects"
                        element={<ProjectsPage/>}
                    />
                </Routes>
            </MemoryRouter>,
        </QueryClientProvider>,
    );

    await user.type(await screen.findByLabelText("Name"), "DevPilot")
    await user.type(await screen.findByLabelText("Repository Owner"), "david");
    await user.type(await screen.findByLabelText("Repository Name"), "DevPilot");
    await user.click(
        screen.getByRole("button", {name: "Create Project"})
    );

    // Assert
    expect(
        await screen.findByText("DevPilot")
    ).toBeInTheDocument();

    expect(getProjects).toHaveBeenCalledTimes(2);
});