using DevPilot.Api.Data;
using DevPilot.Api.Domain.Projects;
using FluentValidation;
using Microsoft.EntityFrameworkCore;
namespace DevPilot.Api.Features.Projects;

public static class ProjectEndpoints
{
    public static void MapProjectEndpoints(this WebApplication endpoints)
    {
        endpoints.MapGet("/api/database-check", async (AppDbContext db) =>
        { var canConnect = await db.Database.CanConnectAsync();
          return Results.Ok(new
          {
              database = "PostgreSQL",
              connected = canConnect
          }); });

        endpoints.MapGet("/api/overview", () => Results.Ok(new
        {
            product = "DevPilot",
            version = "V1.0 skeleton",
            status = "Application API is ready",
            workflow = new[]
            {
                "Select repository", "Choose issue", "Run investigation", "Review evidence", "Create tasks"
            }
        }));

        //Create Projects
        endpoints.MapPost(
            "/api/projects",
            async (
                CreateProjectRequest createProjectRequest,
                AppDbContext appDbContext,
                IValidator<CreateProjectRequest> validator
            ) =>
            { var validationResult =
                  await validator.ValidateAsync(createProjectRequest);

              if (!validationResult.IsValid)
              {
                  return Results.ValidationProblem(
                      validationResult.ToDictionary()
                  );
              }

              var repositoryExists =
                  await appDbContext.Projects.AnyAsync(p =>
                      p.RepositoryOwner == createProjectRequest.RepositoryOwner &&
                      p.RepositoryName == createProjectRequest.RepositoryName
                  );

              if (repositoryExists)
              {
                  return Results.Conflict(new
                  {
                      error = "Repository already exists"
                  });
              }

              var project = new Project
              {
                  Name = createProjectRequest.Name,
                  RepositoryOwner = createProjectRequest.RepositoryOwner,
                  RepositoryName = createProjectRequest.RepositoryName,
                  DefaultBranch = createProjectRequest.DefaultBranch
              };

              appDbContext.Projects.Add(project);

              await appDbContext.SaveChangesAsync();

              var response = new ProjectResponse(
                  project.Id,
                  project.Name,
                  project.RepositoryOwner,
                  project.RepositoryName,
                  project.DefaultBranch,
                  project.CreatedAt
              );

              return Results.Created(
                  $"/api/projects/{project.Id}",
                  response
              ); });

        //Get Projects
        endpoints.MapGet(
            "/api/projects/{projectId:long}",
            async (
                AppDbContext appDbContext,
                long projectId
            ) =>
            { var project = await appDbContext.Projects
                  .AsNoTracking()
                  .Where(p => p.Id == projectId)
                  .Select(p => new ProjectResponse(
                      p.Id,
                      p.Name,
                      p.RepositoryOwner,
                      p.RepositoryName,
                      p.DefaultBranch,
                      p.CreatedAt
                  ))
                  .FirstOrDefaultAsync();
              if (project is null)
              {
                  return Results.NotFound();
              }
              return Results.Ok(project); });

        //Get Projects
        endpoints.MapGet(
            "/api/projects",
            async (
                AppDbContext appDbContext
            ) =>
            { var projects = await appDbContext.Projects
                  .AsNoTracking()
                  .OrderByDescending(project => project.CreatedAt)
                  .Select(p => new ProjectResponse(
                      p.Id,
                      p.Name,
                      p.RepositoryOwner,
                      p.RepositoryName,
                      p.DefaultBranch,
                      p.CreatedAt
                  ))
                  .ToListAsync();
              return Results.Ok(projects); });
    }
}
