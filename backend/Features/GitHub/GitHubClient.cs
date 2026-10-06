namespace DevPilot.Api.Features.GitHub;

public sealed class GitHubClient
{
    private readonly IHttpClientFactory _httpClientFactory;

    public GitHubClient(IHttpClientFactory httpClientFactory) => _httpClientFactory = httpClientFactory;

    private void HandleGitHubResponse(HttpResponseMessage response)
    {
        if (!response.IsSuccessStatusCode)
        {
            throw new HttpRequestException(
                "Github request failed.", null, response.StatusCode);
        }
    }

    public async Task<GitHubIssueResponse[]> GetIssuesAsync(
        string owner,
        string repositoryName,
        CancellationToken cancellationToken
    )
    {
        var httpClient = _httpClientFactory.CreateClient("GitHubService");
        var response = await httpClient.GetAsync(
            $"repos/{owner}/{repositoryName}/issues?per_page=100",
            cancellationToken
        );

        HandleGitHubResponse(response);
        var issue = await response.Content.ReadFromJsonAsync<GitHubIssueResponse[]>(cancellationToken: cancellationToken);
        return issue ?? throw new InvalidOperationException("Github returned an empty investigation response.");
    }

    // public async Task<GitHubIssueResponse> GetIssueAsync(
    //     string owner,
    //     string repositoryName,
    //     int issueNumber, CancellationToken cancellationToken
    // )
    // {
    // }
}
