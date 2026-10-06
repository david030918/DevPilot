using System.Text.Json.Serialization;
namespace DevPilot.Api.Features.GitHub;

public record GitHubIssueResponse(
    long Number,
    string Title,
    string? Body,
    string State,
    [property: JsonPropertyName("html_url")] string HtmlUrl,
    GitHubLabel[] Labels,
    [property: JsonPropertyName("pull_request")] PullRequest? PullRequests
);
public record GitHubLabel(
    string Name,
    string? Description
);
public record PullRequest(
    [property: JsonPropertyName("html_url")] string HtmlUrl
    // string? DiffUrl,
);
