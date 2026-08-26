namespace DevPilot.Api.Features.Projects;

public class CreateProjectRequest
{
    public required string Name { get; set; }
    public required string RepositoryOwner { get; set; }
    public required string RepositoryName { get; set; }
    public string DefaultBranch { get; set; } = "main";
}
