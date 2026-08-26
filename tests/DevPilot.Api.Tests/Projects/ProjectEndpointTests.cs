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
}
