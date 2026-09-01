# async def main() -> None:
#     async with httpx.AsyncClient(
#         timeout=300,
#     ) as client:
#         response = await client.post(
#             "http://localhost:11434/api/chat",
#             json={
#                 "model": "qwen2.5-coder:14b",
#                 "stream": False,
#                 "format": InvestigationResponse.model_json_schema(),
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": (
#                             "You are a software engineering investigation assistant."
#                         ),
#                     },
#                     {
#                         "role": "user",
#                         "content": (
#                             "Repository: david030918/DevPilot. "
#                             "Issue: Project API returns 500."
#                         ),
#                     },
#                 ],
#             },
#         )
#
#         print(response.status_code)
#         print(response.json())


# asyncio.run(main())
