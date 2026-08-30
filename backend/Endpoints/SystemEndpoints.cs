using DevPilot.Api.Data;
namespace DevPilot.Api.Endpoints;

public static class SystemEndpoints
{
    public static void MapSystemEndpoints(
        this WebApplication app)
    {
        app.MapGet(
            "/api/database-check",
            async (AppDbContext db) =>
            { var canConnect =
                  await db.Database.CanConnectAsync();

              return Results.Ok(new
              {
                  database = "PostgreSQL",
                  connected = canConnect
              }); });
    }
}
