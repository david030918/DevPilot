using DevPilot.Api.Data;
using DevPilot.Api.Endpoints;
using DevPilot.Api.Features.Investigations;
using DevPilot.Api.Features.Projects;
using FluentValidation;
using Microsoft.EntityFrameworkCore;
var builder = WebApplication.CreateBuilder(args);

// Application services
builder.Services.AddScoped<IValidator<CreateProjectRequest>, CreateProjectValidator>();
builder.Services.AddScoped<AiServiceClient>();

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

// API infrastructure
builder.Services.AddOpenApi();
builder.Services.AddHealthChecks();
builder.Services.AddCors(options =>
{ options.AddDefaultPolicy(policy =>
      policy.WithOrigins("http://localhost:5173")
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

app.Run();
