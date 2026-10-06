using DevPilot.Api.Data;
using Microsoft.EntityFrameworkCore;
namespace DevPilot.Api.Features.GitHub;

public static class GitHubEndpoints
{
    public static void MapGitHubEndpoints(this WebApplication endpoints)
    {
        //Get issues
        endpoints.MapGet(
            "/issues",
            async (AppDbContext appDbContext) =>
            { var issuess = await appDbContext.Projects
                  .AsNoTracking()
                  .ToListAsync();
              return Results.Ok(issuess); });
    }
}
