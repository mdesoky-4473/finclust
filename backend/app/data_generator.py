import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_user_data(num_users=100):
    users = []
    for _ in range(num_users):
        users.append({
            "name": fake.first_name(),
            "age": np.random.randint(18, 70),
            "monthly_spend": round(np.random.normal(2000, 500), 2),
            "num_txns": np.random.poisson(30),
            "savings": round(np.random.normal(15000, 5000), 2)
        })
    return pd.DataFrame(users)
