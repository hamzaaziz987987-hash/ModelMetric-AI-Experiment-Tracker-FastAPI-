
A fast, robust, and beautiful FastAPI-based experiment tracker for AI/ML model training runs.

Log your models, compare results, find the best one, and clean up failed experiments — all with zero crashes and professional responses.

## Features

| Feature                | Endpoint                       | Description                                                                 |
|------------------------|--------------------------------|-----------------------------------------------------------------------------|
| Log Experiment         | `POST /experiments/log`        | Save model name, hyperparameters, and metrics                               |
| Search & Filter        | `GET /experiments`             | Filter by model name, minimum accuracy, maximum loss                        |
| Get Best Model         | `GET /experiments/best`        | Returns the single experiment with highest accuracy                         |
| Delete Failed Runs     | `DELETE /experiments/{id}`     | Only deletes runs with `accuracy < 0.60` or `loss > 1.0`                    |

## Live Docs & Playground
Run → **http://127.0.0.1:8000/docs**  
Interactive Swagger UI with perfect examples!

## Example Request

```json
{
  "model_name": "ResNet50",
  "parameters": {
    "learning_rate": 0.01,
    "optimizer": "Adam",
    "batch_size": 64
  },
  "metrics": {
    "accuracy": 0.92,
    "loss": 0.15
  }
}


Tech Stack

FastAPI – Web framework & automatic interactive documentation
Pydantic – Strong data validation and parsing
Uvicorn – ASGI server (runs the app)
Python 3.8+ – Language


How to Run
Bashgit clone https://github.com/yourusername/ModelMetric.git
cd ModelMetric

pip install fastapi uvicorn

uvicorn main:app --reload
Open → http://127.0.0.1:8000/docs
Why This Project Stands Out

100% crash-proof — handles missing keys, invalid data, empty database
Professional error messages — clear 404s, 400s, and success confirmations
Defensive programming — missing accuracy = 0.0, missing loss = 999 → auto-fail
Clean number formatting — uses :.4f for beautiful floats
Real-world REST design — proper status codes, IDs, helpful responses
Fully interactive docs — perfect examples pre-filled in Swagger UI
