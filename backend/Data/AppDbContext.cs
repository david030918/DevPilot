using DevPilot.Api.Domain.Projects;
using DevPilot.Api.Domain.Repositories;
using Microsoft.EntityFrameworkCore;
namespace DevPilot.Api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Project> Projects => Set<Project>();
    public DbSet<RepositoryConnection> RepositoryConnections => Set<RepositoryConnection>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(AppDbContext).Assembly);
    }
}
