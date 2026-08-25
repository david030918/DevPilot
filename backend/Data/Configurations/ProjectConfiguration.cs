using DevPilot.Api.Domain.Projects;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace DevPilot.Api.Data.Configurations;

public class ProjectConfiguration : IEntityTypeConfiguration<Project>
{
    public void Configure(EntityTypeBuilder<Project> builder)
    {
        builder.ToTable("Projects");
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Name).IsRequired().HasMaxLength(200);
        builder.Property(p=> p.RepositoryOwner).IsRequired().HasMaxLength(100);
        builder.Property(p=> p.RepositoryName).IsRequired().HasMaxLength(100);
        builder.Property(p=> p.DefaultBranch).IsRequired().HasMaxLength(255);
        builder.HasIndex(x => new
            {
                x.RepositoryOwner,
                x.RepositoryName
            })
            .IsUnique();
    }
}
