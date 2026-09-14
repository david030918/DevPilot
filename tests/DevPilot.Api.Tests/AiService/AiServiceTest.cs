using System.Net;
using System.Text;
using System.Text.Json;
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
                "{\n  \"investigation\": {\n    \"summary\": \"Test Summary\",\n    \"possible_causes\": [],\n    \"investigation_steps\": [],\n    \"assumptions\": [],\n    \"suggested_tests\": []\n  },\n  \"metadata\": {\n    \"provider\": \"fake\",\n    \"model\": \"fake-model\",\n    \"prompt_version\": \"v1\",\n    \"schema_version\": \"v1\"\n  }\n}",
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
        var result =
            await client.InvestigateIssueAsync(
                request,
                CancellationToken.None);
        Assert.Equal("Test Summary", result.Investigation.Summary);
        Assert.Equal(
            HttpMethod.Post,
            fakeHandler.Request?.Method);
        Assert.Equal("http://fake-ai/ai/investigate-issue", fakeHandler.Request?.RequestUri?.ToString());
        var content = await fakeHandler.Request?.Content?.ReadAsStringAsync();
        using var json = JsonDocument.Parse(content);
        var repository = json.RootElement.GetProperty("repository");
        Assert.Equal("fake-owner", repository.GetProperty("owner").GetString());
    }

    [Fact]
    public async Task InvestigateIssueAsync_Non_200()
    {
        var response = new HttpResponseMessage
        {
            StatusCode = HttpStatusCode.BadGateway,
            Content = new StringContent(
                "{\n  \"investigation\": {\n    \"summary\": \"Test Summary\",\n    \"possible_causes\": [],\n    \"investigation_steps\": [],\n    \"assumptions\": [],\n    \"suggested_tests\": []\n  },\n  \"metadata\": {\n    \"provider\": \"fake\",\n    \"model\": \"fake-model\",\n    \"prompt_version\": \"v1\",\n    \"schema_version\": \"v1\"\n  }\n}",
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
        // Act
        var exception = await Assert.ThrowsAsync<HttpRequestException>(() => client.InvestigateIssueAsync(
            request,
            CancellationToken.None));

        Assert.Equal(HttpStatusCode.BadGateway, exception.StatusCode);
    }

    [Fact]
    public async Task InvestigateIssueAsync_Caller_Cancellation()
    {
        using var cts = new CancellationTokenSource();

        var response = new HttpResponseMessage
        {
            StatusCode = HttpStatusCode.OK,
            Content = new StringContent(
                "{\n  \"investigation\": {\n    \"summary\": \"Test Summary\",\n    \"possible_causes\": [],\n    \"investigation_steps\": [],\n    \"assumptions\": [],\n    \"suggested_tests\": []\n  },\n  \"metadata\": {\n    \"provider\": \"fake\",\n    \"model\": \"fake-model\",\n    \"prompt_version\": \"v1\",\n    \"schema_version\": \"v1\"\n  }\n}",
                Encoding.UTF8,
                "application/json"
            )
        };

        var fakeHandler = new FakeHttpMessageHandler(async cancellationToken =>
            { await Task.Delay(
                  Timeout.Infinite, cancellationToken);
              return response; }
        );

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
        // Act
        var task = client.InvestigateIssueAsync(
            request,
            cts.Token);
        cts.Cancel();

        // Act
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => task);
    }

    [Fact]
    public async Task InvestigateIssueAsync_Timeout()
    {
        var response = new HttpResponseMessage
        {
            StatusCode = HttpStatusCode.OK,
            Content = new StringContent(
                "{\n  \"investigation\": {\n    \"summary\": \"Test Summary\",\n    \"possible_causes\": [],\n    \"investigation_steps\": [],\n    \"assumptions\": [],\n    \"suggested_tests\": []\n  },\n  \"metadata\": {\n    \"provider\": \"fake\",\n    \"model\": \"fake-model\",\n    \"prompt_version\": \"v1\",\n    \"schema_version\": \"v1\"\n  }\n}",
                Encoding.UTF8,
                "application/json"
            )
        };

        var fakeHandler = new FakeHttpMessageHandler(async cancellationToken =>
            { var timeout = TimeSpan.FromMilliseconds(100);
              await Task.Delay(
                  timeout, cancellationToken);
              return response; }
        );

        var httpClient = new HttpClient(fakeHandler)
        {
            BaseAddress = new("http://fake-ai/"),
            Timeout = TimeSpan.FromMilliseconds(20)
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
        // Act
        var task = client.InvestigateIssueAsync(request, CancellationToken.None);

        // Act
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => task);
    }


    private sealed class TestHttpClientFactory : IHttpClientFactory
    {
        private readonly HttpClient _httpClient;

        public TestHttpClientFactory(HttpClient httpClient) => _httpClient = httpClient;

        public HttpClient CreateClient(string name) => _httpClient;
    }
}
