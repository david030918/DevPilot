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
        var pageNumber = 1;
        var result = new List<GitHubIssueResponse>();
        while (true)
        {
            var response = await httpClient.GetAsync(
                $"repos/{owner}/{repositoryName}/issues?state=all&per_page=1&page={pageNumber}",
                cancellationToken
            );
            HandleGitHubResponse(response);
            var issues = await response.Content.ReadFromJsonAsync<GitHubIssueResponse[]>(cancellationToken: cancellationToken);
            result.AddRange(issues ?? throw new InvalidOperationException("Github returned an empty investigation response."));
            if (response.Headers.TryGetValues("Link", out var linkValues) && linkValues.Any(linkValue => linkValue.Contains("rel=\"next\"")))
                pageNumber++;
            else
            {
                break;
            }
        }
        return result.ToArray();
    }

    public async Task<GitHubIssueResponse> GetIssueAsync(
        string owner,
        string repositoryName,
        int issueNumber, CancellationToken cancellationToken
    )
    {
        var httpClient = _httpClientFactory.CreateClient("GitHubService");
        var response = await httpClient.GetAsync(
            $"repos/{owner}/{repositoryName}/issues/{issueNumber}",
            cancellationToken
        );
        HandleGitHubResponse(response);
        var issue = await response.Content.ReadFromJsonAsync<GitHubIssueResponse>(cancellationToken: cancellationToken);
        return issue ?? throw new InvalidOperationException("Github returned an empty issue.");
    }
}
