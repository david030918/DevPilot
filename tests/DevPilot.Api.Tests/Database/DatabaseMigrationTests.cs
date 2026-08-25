using DevPilot.Api.Data;
using Microsoft.EntityFrameworkCore;
using Testcontainers.PostgreSql;

namespace DevPilot.Api.Tests.Database;

public class DatabaseMigrationTests : IAsyncLifetime
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
    }

    public async Task DisposeAsync()
    {
        await _postgres.DisposeAsync();
    }

    [Fact]
    public async Task Migrations_CanBeAppliedToEmptyDatabase()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(_postgres.GetConnectionString())
            .Options;

        await using var db = new AppDbContext(options);

        await db.Database.MigrateAsync();

        Assert.True(await db.Database.CanConnectAsync());
    }
}
