using System.Text.Json.Serialization;
namespace DevPilot.Api.Features.Investigations;

public sealed record RepositoryContext
{
    [JsonPropertyName("owner")]
    public required string Owner { get; init; }

    [JsonPropertyName("name")]
    public required string Name { get; init; }

    [JsonPropertyName("default_branch")]
    public string DefaultBranch { get; init; } = "main";
}
public sealed record IssueContext
{
    [JsonPropertyName("number")]
    public required int Number { get; init; }

    [JsonPropertyName("title")]
    public required string Title { get; init; }

    [JsonPropertyName("body")]
    public string? Body { get; init; } = null;
}
public sealed record InvestigationRequest
{
    [JsonPropertyName("repository")]
    public required RepositoryContext Repository { get; init; }

    [JsonPropertyName("issue")]
    public required IssueContext Issue { get; init; }
}
public sealed record PossibleCause
{
    [JsonPropertyName("title")]
    public required string Title { get; init; }

    [JsonPropertyName("explanation")]
    public required string Explanation { get; init; }

    [JsonPropertyName("confidence")]
    public required float Confidence { get; init; }
}
public sealed record InvestigationStep
{
    [JsonPropertyName("order")]
    public required int Order { get; init; }

    [JsonPropertyName("description")]
    public required string Description { get; init; }
}
public sealed record SuggestedTest
{
    [JsonPropertyName("name")]
    public required string Name { get; init; }

    [JsonPropertyName("description")]
    public required string Description { get; init; }
}
public sealed record InvestigationMetadata
{
    [JsonPropertyName("provider")]
    public required string Provider { get; init; }

    [JsonPropertyName("model")]
    public required string Model { get; init; }

    [JsonPropertyName("prompt_version")]
    public required string PromptVersion { get; init; }

    [JsonPropertyName("schema_version")]
    public required string SchemaVersion { get; init; }
}
public sealed record InvestigationResponse
{
    [JsonPropertyName("summary")]
    public required string Summary { get; init; }

    [JsonPropertyName("possible_causes")]
    public required List<PossibleCause> PossibleCauses { get; init; }

    [JsonPropertyName("investigation_steps")]
    public required List<InvestigationStep> InvestigationSteps { get; init; }

    [JsonPropertyName("assumptions")]
    public required List<string> Assumptions { get; init; }

    [JsonPropertyName("suggested_tests")]
    public required List<SuggestedTest> SuggestedTests { get; init; }
}
public sealed record InvestigationResult
{
    [JsonPropertyName("investigation")]
    public required InvestigationResponse Investigation { get; init; }

    [JsonPropertyName("metadata")]
    public required InvestigationMetadata Metadata { get; init; }
}
