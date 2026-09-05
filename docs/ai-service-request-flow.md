# AI Service Request and Failure Flow

## Successful Request Flow
1. The client sends `POST /ai/investigate-issue` with an `InvestigationRequest`.
2. FastAPI resolves `InvestigationService` through depenency injection.
3. service `inverstigation` call the selected privoder - `OllamaInvestigationProvider`
4. `OllamaInvestigationProvider` uses the shared `AsyncClient` to call Ollama.
5. ollama return the HTTP responses
6. The provider validate the structurnd output and return an `InvestigationResponse`
7. FastAPI returns the successful response to the client.

## Failure Flow
1. The client sends `POST /ai/investigate-issue` with an `InvestigationRequest`.
2. FastAPI resolves `InvestigationService` through depenency injection.
3. service `inverstigation` call the selected privoder - `OllamaInvestigationProvider`
4. `OllamaInvestigationProvider` uses the shared `AsyncClient` to call Ollama.
5. If a timeout, connection error, or retryable HTTP error occurs, the provider retries with exponential backoff.
6. If retries are exhausted, or the HTTP error is not retryable, the provider raises the corresponding `ProviderError`.
7. If the HTTP request succeeds but the structured output is invalid, the provider raises `ProviderOutputError`.
8. The exception propagates through the service and endpoint to the FastAPI exception handler.
9. FastAPI converts the provider exception into a stable HTTP error response for the client.