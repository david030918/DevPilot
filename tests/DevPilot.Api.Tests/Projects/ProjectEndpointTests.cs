using System.Net;
using System.Net.Http.Json;
using DevPilot.Api.Features.Projects;
using DevPilot.Api.Tests.Infrastructure;
namespace DevPilot.Api.Tests.Projects;

public class ProjectEndpointTests
{
    [Fact]
    public async Task CreateProject_ReturnsCreatedProject()
    {
        await using var factory =
            new DevPilotWebApplicationFactory();

        await factory.InitializeAsync();

        var client = factory.CreateClient();

        var request = new CreateProjectRequest
        {
            Name = "DevPilot",
            RepositoryOwner = "david030918",
            RepositoryName = "DevPilot",
            DefaultBranch = "main"
        };

        var response = await client.PostAsJsonAsync(
            "/api/projects",
            request);

        var responseBody = await response.Content.ReadAsStringAsync();

        Assert.True(
            response.StatusCode == HttpStatusCode.Created,
            $"Expected 201 Created, but received {(int)response.StatusCode} {response.StatusCode}. Body: {responseBody}");

        var project =
            await response.Content
                .ReadFromJsonAsync<ProjectResponse>();

        Assert.NotNull(project);

        Assert.Equal(
            "DevPilot",
            project.Name);

        Assert.Equal(
            "david030918",
            project.RepositoryOwner);
    }

    [Fact]
    public async Task GetProjects_ReturnsProjects()
    {
        await using var factory =
            new DevPilotWebApplicationFactory();
        await factory.InitializeAsync();
        var client = factory.CreateClient();
        var request = new CreateProjectRequest
        {
            Name = "GetProject_ReturnsProject",
            RepositoryOwner = "david030918",
            RepositoryName = "DevPilot",
            DefaultBranch = "main"
        };
        var response = await client.PostAsJsonAsync(
            "/api/projects",
            request);

        var responseBody = await response.Content.ReadAsStringAsync();
        Assert.True(
            response.StatusCode == HttpStatusCode.Created,
            $"Expected 201 Created, but received {(int)response.StatusCode} {response.StatusCode}. Body: {responseBody}");

        var project = await client.GetAsync(
            "/api/projects");
        Assert.NotNull(project);
        var list = await project.Content.ReadFromJsonAsync<List<ProjectResponse>>();
        Assert.Equal(HttpStatusCode.OK, project.StatusCode);
        Assert.NotNull(list);
        Assert.Equal("GetProject_ReturnsProject", list.Single().Name);
    }

    [Fact]
    public async Task GetProject_ReturnsProject()
    {
        await using var factory = new DevPilotWebApplicationFactory();
        await factory.InitializeAsync();
        var client = factory.CreateClient();
        var request = new CreateProjectRequest
        {
            Name = "GetProject_ReturnsProject",
            RepositoryOwner = "david030918",
            RepositoryName = "DevPilot",
            DefaultBranch = "main"
        };
        var response = await client.PostAsJsonAsync(
            "/api/projects",
            request);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var project =
            await response.Content
                .ReadFromJsonAsync<ProjectResponse>();
        Assert.NotNull(project);

        var projectId = project.Id;
        var getResponse = await client.GetAsync(
            $"/api/projects/{projectId}");
        var body = await getResponse.Content.ReadAsStringAsync();
        Assert.True(
            getResponse.StatusCode == HttpStatusCode.OK,
            $"Expected 200 OK, but got {(int)getResponse.StatusCode} " +
            $"{getResponse.StatusCode}. Body: {body}");
        Assert.Equal(HttpStatusCode.OK, getResponse.StatusCode);

        var returnedProject = await getResponse.Content.ReadFromJsonAsync<ProjectResponse>();

        Assert.NotNull(returnedProject);
        Assert.Equal(projectId, returnedProject.Id);
        Assert.Equal("GetProject_ReturnsProject", returnedProject.Name);
    }

    [Fact]
    public async Task GetProjects_NotFound()
    {
        await using var factory =
            new DevPilotWebApplicationFactory();
        await factory.InitializeAsync();
        var client = factory.CreateClient();
        var projectId = 999999L;
        var getResponse = await client.GetAsync(
            $"/api/projects/{projectId}");
        Assert.Equal(HttpStatusCode.NotFound, getResponse.StatusCode);
    }

    [Fact]
    public async Task Duplicate_Authorized()
    {
        await using var factory =
            new DevPilotWebApplicationFactory();
        await factory.InitializeAsync();
        var client = factory.CreateClient();
        var request = new CreateProjectRequest
        {
            Name = "GetProject_ReturnsProject",
            RepositoryOwner = "david030918",
            RepositoryName = "DevPilot",
            DefaultBranch = "main"
        };
        var response = await client.PostAsJsonAsync(
            "/api/projects",
            request);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        //Duplicate
        var response2 = await client.PostAsJsonAsync(
            "/api/projects",
            request);
        Assert.Equal(HttpStatusCode.Conflict, response2.StatusCode);
    }
}
