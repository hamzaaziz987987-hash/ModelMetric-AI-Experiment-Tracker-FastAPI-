from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

app = FastAPI()


experiments: Dict[
    str, Dict
] = {}  # we write : Dict[str, Dict] part so that if you get a non dict or then the code stops there(its just for coding eddicuite)
next_id = 1


class Experiment(BaseModel):
    model_name: str
    parameters: Dict[str, Any]
    metrics: Dict[str, float]


# what an example valid input should look like:

# {
#  "model_name": "ResNet50",
#  "parameters": {"learning_rate": 0.01, "optimizer": "Adam"},
#  "metrics": {"accuracy": 0.92, "loss": 0.15}
# }


@app.post("/experiments/log")
def log_experiment(exp: Experiment):
    global next_id  # global makes it so that this variable can be used anywhere and isint treated as a local var inside a function(can be updated)
    experiment_id = str(next_id)
    next_id += 1

    experiments[experiment_id] = {
        "model_name": exp.model_name,
        "parameters": exp.parameters,
        "metrics": exp.metrics,
    }

    return {"id": experiment_id, **experiments[experiment_id]}


####### Feature B: GET /experiments


@app.get("/experiments")
def get_experiments(
    model_name: str | None = None,
    min_accuracy: float | None = None,
    max_loss: float | None = None,
) -> List[dict]:
    # Return all experiments, optionally filtered by:
    #  - model_name (has to be exact match)
    #  - min_accuracy (accuracy >= value)
    #  - max_loss (loss <= value)

    results = []

    for (
        exp_id,
        exp,
    ) in experiments.items():  # this is how to look through dicts where exp_id becomes key and exp becomes values also .items returns whole pair (key and value)
        # filter 1: model_name
        if model_name is not None and exp["model_name"] != model_name:
            continue

        # filter 2: min_accuracy
        if min_accuracy is not None:
            # get accuracy (might be missing!)
            accuracy_value = exp["metrics"].get("accuracy")
            if accuracy_value is None:  # key not present
                accuracy_value = 0.0  # treat missing as terrible
            if accuracy_value < min_accuracy:
                continue

        # filter 3: max_loss
        if max_loss is not None:
            # Safely get loss (might be missing!)
            loss_value = exp["metrics"].get("loss")
            if loss_value is None:  # key not present
                loss_value = 999.0  # treat missing as terrible
            if loss_value > max_loss:
                continue

        # if we get here → this experiment passed all filters
        results.append({"id": exp_id, **exp})

    return results


############ feature C: GET /experiments/best


@app.get("/experiments/best")
def get_best_experiment():
    # Returns ONLY the single experiment with the highest accuracy
    # If no experiments exist it gives 404 error
    # If multiple have the same accuracy it returns any one of them

    if not experiments:
        raise HTTPException(status_code=404, detail="No experiments logged yet")

    # Find the experiment with maximum accuracy
    best_id = None
    best_accuracy = (
        -1.0
    )  # impossible value (accuracy can't be negative soo any acc will become best)

    for exp_id, exp in experiments.items():
        # Safely get accuracy (same defensive trick as before)
        accuracy = exp["metrics"].get("accuracy")
        if accuracy is None:
            accuracy = 0.0  # treat missing accuracy as terrible

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_id = exp_id

    # Return the best one with its ID
    best_exp = experiments[best_id]
    return {"id": best_id, **best_exp}


########## Feature D: Delete Failed Runs


@app.delete("/experiments/{experiment_id}", status_code=200)
def delete_experiment(experiment_id: str):
    if experiment_id not in experiments:
        raise HTTPException(status_code=404, detail="Experiment not found")

    exp = experiments[experiment_id]

    accuracy = exp["metrics"].get("accuracy", 0.0)  # if acc is none it will give 0.0
    loss = exp["metrics"].get("loss", 999.0)  # if loss is none it gives 999

    # Only delete failed runs which i decided as less than 0.60 acc or more than 1 loss
    if accuracy < 0.60 or loss > 1.0:
        deleted_exp = experiments.pop(experiment_id)
        return {
            "message": "Experiment successfully deleted — considered a failed run",
            "deleted_id": experiment_id,
            "reason": f"accuracy={accuracy:.4f}, loss={loss:.4f}",  # .examplenumberf is used to customise the number of numbers after decimal point in floats
            "deleted_experiment": {"id": experiment_id, **deleted_exp},
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Refused to delete experiment {experiment_id}: "
            f"accuracy={accuracy:.4f} ≥ 0.60 and loss={loss:.4f} ≤ 1.0 → not a failed run",
        )


#   uvicorn ModelMetric_fastapi_project:app --reload
#   http://127.0.0.1:8000/docs
