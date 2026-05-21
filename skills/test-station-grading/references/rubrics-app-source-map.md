# Rubrics App Source Map

- `src/blueprints/test_station/grading.py`: divides rubric items by `Mode`, prepares grading payloads, and queues grading jobs.
- `src/grading_services/test_station_service.py`: embedded grading prompt templates for `audio`, `video`, and `note`.
- `src/grading_schemas/multimodal_grading.py`: Pydantic schemas and JSON schemas for multimodal grading responses.
- `src/llm_clients/gemini_client.py`: multimodal grading calls for media inputs.
