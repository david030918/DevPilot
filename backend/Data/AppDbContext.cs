using Microsoft.EntityFrameworkCore;
using DevPilot.Api.Domain.Projects;

namespace DevPilot.Api.Data;
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }
    
    public DbSet<Project> Projects => Set<Project>();
}
