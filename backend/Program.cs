using DevPilot.Api.Data;
using DevPilot.Api.Endpoints;
using DevPilot.Api.Features.GitHub;
using DevPilot.Api.Features.Investigations;
using DevPilot.Api.Features.Projects;
using FluentValidation;
using Microsoft.EntityFrameworkCore;
var builder = WebApplication.CreateBuilder(args);

// Application services
builder.Services.AddScoped<IValidator<CreateProjectRequest>, CreateProjectValidator>();
builder.Services.AddScoped<AiServiceClient>();
builder.Services.AddScoped<GitHubClient>();

// Database
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// External services
builder.Services.AddHttpClient("AiService", client =>
{ var baseUrl = builder.Configuration["AiService:BaseUrl"] ?? throw new InvalidOperationException(
      "AiService:BaseUrl is not configured.");
  client.BaseAddress = new(baseUrl!);
  client.Timeout = TimeSpan.FromSeconds(int.Parse(builder.Configuration["AiService:TimeoutSeconds"] ?? "50")); });

builder.Services.AddHttpClient("GitHubService", client =>
{ var baseUrl = builder.Configuration["GitHubService:BaseUrl"] ?? throw new InvalidOperationException(
      "GitHubService:BaseUrl is not configured.");
  client.DefaultRequestHeaders.UserAgent.ParseAdd("DevPilot/1.0");
  client.DefaultRequestHeaders.Accept.ParseAdd("application/vnd.github+json");
  client.DefaultRequestHeaders.Add(
      "X-GitHub-Api-Version",
      "2022-11-28");
  client.BaseAddress = new(baseUrl!);
  client.Timeout = TimeSpan.FromSeconds(int.Parse(builder.Configuration["GitHubService:TimeoutSeconds"] ?? "50")); });


// API infrastructure
builder.Services.AddOpenApi();
builder.Services.AddHealthChecks();
builder.Services.AddCors(options =>
{ options.AddDefaultPolicy(policy =>
      policy.WithOrigins(builder.Configuration["Frontend:Origin"] ?? "http://localhost:5174")
          .AllowAnyHeader()
          .AllowAnyMethod()); });

var app = builder.Build();
// Development
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}
// Middleware
app.UseCors();

// Endpoints
app.MapHealthChecks("/health");
app.MapProjectEndpoints();
app.MapSystemEndpoints();
app.MapOverviewEndpoints();
app.MapGitHubEndpoints();

app.Run();
