namespace DevPilot.Api.Domain.Projects;

public class Project
{
    public long Id { get; set; }
    public required string Name { get; set; }
    public required string RepositoryOwner { get; set; }
    public required string RepositoryName { get; set; }
    public string DefaultBranch { get; set; } = "main";
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
