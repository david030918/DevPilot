using FluentValidation;
namespace DevPilot.Api.Features.Projects;

public class CreateProjectValidator : AbstractValidator<CreateProjectRequest>
{
    public CreateProjectValidator()
    {
        RuleFor(x => x.Name).NotNull().NotEmpty().MaximumLength(200);
        RuleFor(x => x.RepositoryOwner).NotNull().NotEmpty().MaximumLength(100);
        RuleFor(x => x.RepositoryName).NotNull().NotEmpty().MaximumLength(100);
        RuleFor(x => x.DefaultBranch).NotNull().NotEmpty().MaximumLength(255);
    }
}
