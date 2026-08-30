namespace DevPilot.Api.Endpoints;

public static class OverviewEndpoints
{
    public static void MapOverviewEndpoints(
        this WebApplication app)
    {
        app.MapGet(
            "/api/overview",
            () => Results.Ok(new
            {
                product = "DevPilot",
                version = "V1.0 skeleton",
                status = "Application API is ready",
                workflow = new[]
                {
                    "Select repository", "Choose issue", "Run investigation", "Review evidence", "Create tasks"
                }
            }));
    }
}
