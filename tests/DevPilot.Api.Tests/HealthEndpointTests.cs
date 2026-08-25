using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;

namespace DevPilot.Api.Tests;

public class HealthEndpointTests
{
    [Fact]
    public async Task Health_ReturnsOk()
    {
        await using var factory =
            new WebApplicationFactory<Program>();

        var client = factory.CreateClient();

        var response = await client.GetAsync("/health");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
