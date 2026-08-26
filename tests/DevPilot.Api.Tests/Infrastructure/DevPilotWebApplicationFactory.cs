using DevPilot.Api.Data;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Testcontainers.PostgreSql;

namespace DevPilot.Api.Tests.Infrastructure;

public class DevPilotWebApplicationFactory
    : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres =
        new PostgreSqlBuilder("postgres:17")
            .WithDatabase("devpilot_test")
            .WithUsername("devpilot")
            .WithPassword("devpilot")
            .Build();

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();
        using var scope=Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await db.Database.MigrateAsync();
        var canConnect = await db.Database.CanConnectAsync();
        var appliedMigrations =
            await db.Database.GetAppliedMigrationsAsync();
        Console.WriteLine(
            $"Test database connected: {canConnect}");
        Console.WriteLine(
            $"Applied migrations: {string.Join(", ", appliedMigrations)}");
    }

    public new async Task DisposeAsync()
    {
        await _postgres.DisposeAsync();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<AppDbContext>();
            services.RemoveAll<DbContextOptions<AppDbContext>>();

            services.AddDbContext<AppDbContext>(options =>
                options.UseNpgsql(_postgres.GetConnectionString()));
        });
    }
}
