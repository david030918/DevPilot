using DevPilot.Api.Data;
using Microsoft.EntityFrameworkCore;
using DevPilot.Api.Domain.Projects;
using DevPilot.Api.Features.Projects;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.WithOrigins("http://localhost:5173")
            .AllowAnyHeader()
            .AllowAnyMethod());
});
builder.Services.AddHealthChecks();

var app = builder.Build();

app.UseCors();
app.MapHealthChecks("/health");

app.MapGet("/api/database-check", async (AppDbContext db) =>
{
    var canConnect = await db.Database.CanConnectAsync();
    return Results.Ok(new
    {
        database = "PostgreSQL",
        connected = canConnect
    });
});

app.MapGet("/api/overview", () => Results.Ok(new
{
    product = "DevPilot",
    version = "V1.0 skeleton",
    status = "Application API is ready",
    workflow = new[]
    {
        "Select repository",
        "Choose issue",
        "Run investigation",
        "Review evidence",
        "Create tasks"
    }
}));
app.MapPost(
    "/api/projects",
    async (CreateProjectRequest request, AppDbContext db) =>
    {
        var project = new Project
        {
            Name = request.Name,
            RepositoryOwner = request.RepositoryOwner,
            RepositoryName = request.RepositoryName,
            DefaultBranch = request.DefaultBranch
        };
    db.Projects.Add(project);
    await db.SaveChangesAsync();
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
        response);
    });

app.Run();

