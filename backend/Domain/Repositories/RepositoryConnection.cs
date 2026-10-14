namespace DevPilot.Api.Domain.Repositories;

public class RepositoryConnection
{
    public long Id { get; set; }
    public long ProjectId { get; set; }
    public required string RepositoryOwner { get; set; }
    public required string RepositoryName { get; set; }
    public string DefaultBranch { get; set; } = "main";

    public DateTimeOffset ConnectedAt { get; set; } = DateTimeOffset.UtcNow;
}
