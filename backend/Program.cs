var builder = WebApplication.CreateBuilder(args);

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

app.Run();

