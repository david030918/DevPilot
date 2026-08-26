namespace DevPilot.Api.Features.Projects;

public record ProjectResponse(
    long Id,
    string Name,
    string RepositoryOwner,
    string RepositoryName,
    string DefaultBranch,
    DateTimeOffset CreatedAt
);

