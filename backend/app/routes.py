from fastapi import APIRouter
from app.data_generator import generate_user_data
from app.clustering import cluster_users

router = APIRouter()

@router.get("/generate")
def generate_data():
    data = generate_user_data(num_users=100)
    return {"data": data.to_dict(orient="records")}

@router.get("/cluster")
def cluster_data():
    data = generate_user_data(num_users=100)
    labels = cluster_users(data)
    data["cluster"] = labels
    return {"clustered_data": data.to_dict(orient="records")}
