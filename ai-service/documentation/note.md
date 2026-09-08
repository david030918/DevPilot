### Ollama limitations

- **Hardware dependency:** Local Ollama performance and usable model size depend on the host machine's available CPU/GPU
  and memory.
- **Latency variability:** Investigation latency can vary with hardware, model size, current system load, and input
  size. No fixed latency guarantee is assumed for V1.
- **Model-quality variability:** Investigation quality depends on the selected local model. Outputs remain suggestions
  and must not be treated as established facts without review.
- **Context limitations:** Model context is finite. Large issues or future repository context may exceed practical
  context limits and may require input selection or truncation.