namespace DevPilot.Api.Features.Investigations;

public sealed class AiServiceClient
{
    private readonly IHttpClientFactory _httpClientFactory;
    public AiServiceClient(IHttpClientFactory httpClientFactory) => _httpClientFactory = httpClientFactory;

    public async Task<InvestigationResult> InvestigateIssueAsync(
        InvestigationRequest request,
        CancellationToken cancellationToken)
    {
        var httpClient = _httpClientFactory.CreateClient("AiService");
        var response = await httpClient.PostAsJsonAsync(
            "ai/investigate-issue",
            request,
            cancellationToken);
        response.EnsureSuccessStatusCode();
        var result = await response.Content.ReadFromJsonAsync<InvestigationResult>(
            cancellationToken);
        return result ?? throw new InvalidOperationException("AI Service returned an empty investigation response.");
    }
}
