namespace DevPilot.Api.Features.GitHub;

public record GitHubIssueResponse(
    long Number,
    string Title,
    string? Body,
    string State,
    string HtmlUrl,
    GitHubLabel[] Labels
);
public record GitHubLabel(
    string Name,
    string? Description
);
