using System.Net;
using System.Text;
using DevPilot.Api.Features.Investigations;
namespace DevPilot.Api.Tests.AiService;

public class AiServiceTest
{
    [Fact]
    public async Task InvestigateIssueAsync_SendsExpectedRequest_AndDeserializesResponse()
    {
        var response = new HttpResponseMessage
        {
            StatusCode = HttpStatusCode.OK,
            Content = new StringContent(
                "{\n  \"investigation\": {\n    \"summary\": \"...\",\n    \"possible_causes\": [],\n    \"investigation_steps\": [],\n    \"assumptions\": [],\n    \"suggested_tests\": []\n  },\n  \"metadata\": {\n    \"provider\": \"fake\",\n    \"model\": \"fake-model\",\n    \"prompt_version\": \"v1\",\n    \"schema_version\": \"v1\"\n  }\n}",
                Encoding.UTF8,
                "application/json"
            )
        };

        var fakeHandler = new FakeHttpMessageHandler(response);

        var httpClient = new HttpClient(fakeHandler)
        {
            BaseAddress = new("http://fake-ai/")
        };


        var factory = new TestHttpClientFactory(httpClient);
        var client = new AiServiceClient(factory);


        var request = new InvestigationRequest
        {
            Issue = new()
            {
                Body = "dddd",
                Number = 1,
                Title = "title"
            },
            Repository = new()
            {
                Name = "fake-repository",
                Owner = "fake-owner"
            }
        };
        var re =
            await client.InvestigateIssueAsync(
                request,
                CancellationToken.None);
    }
    private sealed class TestHttpClientFactory : IHttpClientFactory
    {
        private readonly HttpClient _httpClient;

        public TestHttpClientFactory(HttpClient httpClient) => _httpClient = httpClient;

        public HttpClient CreateClient(string name) => _httpClient;
    }
}
