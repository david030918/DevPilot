using DevPilot.Api.Data;
using Microsoft.EntityFrameworkCore;
namespace DevPilot.Api.Features.GitHub;

public static class GitHubEndpoints
{
    public static void MapGitHubEndpoints(this WebApplication endpoints)
    {
        //Get issues from DB
        endpoints.MapGet(
            "/issues",
            async (AppDbContext appDbContext) =>
            { var issuess = await appDbContext.Projects
                  .AsNoTracking()
                  .ToListAsync();
              return Results.Ok(issuess); });

        //get issues from Github
        endpoints.MapGet(
            "/projects/{projectId:long}/issues",
            async (GitHubClient gitHubClient, AppDbContext appDbContext, CancellationToken cancellationToken, long projectId) =>
            { //get Project detail from DB
              var project = await appDbContext.Projects.AsNoTracking()
                  .SingleOrDefaultAsync(project => project.Id == projectId, cancellationToken);
              if (project is null)
              {
                  return Results.NotFound();
              }

              var issues = await gitHubClient.GetIssuesAsync(project.RepositoryOwner, project.RepositoryName, cancellationToken);
              return Results.Ok(issues);
            }
        );
    }
}
