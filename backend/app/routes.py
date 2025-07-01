from fastapi import APIRouter
from app.data_generator import generate_user_data
from app.clustering import cluster_logic

router = APIRouter()

generated_data = []  # Global variable to hold generated data

@router.get("/generate")
def generate_users():
    global generated_data
    generated_data = generate_user_data(100)
    return {"data": generated_data}

@router.get("/cluster")
def cluster_users():
    global generated_data
    if not generated_data:
        return {"error": "No data to cluster. Please generate users first."}
    
    import pandas as pd
    df = pd.DataFrame(generated_data)  # ✅ Convert list of dicts to DataFrame
    labels = cluster_logic(df)

    # Attach cluster labels to original user dicts
    for user, label in zip(generated_data, labels):
        user["cluster"] = int(label)  # ✅ ensure it's JSON-serializable

    return {"clustered_data": generated_data}


