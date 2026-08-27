using DevPilot.Api.Data;
using DevPilot.Api.Features.Projects;
using FluentValidation;
using Microsoft.EntityFrameworkCore;
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddScoped<IValidator<CreateProjectRequest>, CreateProjectValidator>();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddOpenApi();
builder.Services.AddCors(options =>
{ options.AddDefaultPolicy(policy =>
      policy.WithOrigins("http://localhost:5173")
          .AllowAnyHeader()
          .AllowAnyMethod()); });
builder.Services.AddHealthChecks();

var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseCors();
app.MapHealthChecks("/health");
app.MapProjectEndpoints();

app.Run();
