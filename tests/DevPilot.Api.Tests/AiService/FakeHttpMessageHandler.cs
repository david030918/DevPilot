namespace DevPilot.Api.Tests.AiService;

public sealed class FakeHttpMessageHandler : HttpMessageHandler
{
    private readonly Func<CancellationToken, Task<HttpResponseMessage>>? _handler;
    private readonly HttpResponseMessage _response;

    public FakeHttpMessageHandler(HttpResponseMessage response) => _response = response;

    public FakeHttpMessageHandler(Func<CancellationToken, Task<HttpResponseMessage>> handler) => _handler = handler;
    public HttpRequestMessage? Request { get; private set; }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Request = request;
        if (_handler is not null)
        {
            return _handler(cancellationToken);
        }
        return Task.FromResult(_response);
    }
}
