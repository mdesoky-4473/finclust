from fastapi import APIRouter, HTTPException
from app.data_generator import generate_user_data
from app.clustering import cluster_logic
import pandas as pd

router = APIRouter()
generated_data = []  # Global variable for demo use only

@router.get("/generate")
def generate_users():
    global generated_data
    generated_data = generate_user_data(100)
    return {"data": generated_data}

@router.get("/cluster")
def cluster_users(k: int = 3):
    global generated_data
    if not generated_data:
        raise HTTPException(status_code=400, detail="No data available to cluster.")

    df = pd.DataFrame(generated_data)
    clustered_df = cluster_logic(df, k)
    return {"clustered_data": clustered_df.to_dict(orient="records")}
