from sklearn.cluster import KMeans
import pandas as pd

def cluster_logic(df, k=3):
    features = df[["age", "monthly_spend", "num_txns", "savings"]]
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(features)

    # Assign labels to original data
    df = df.copy()  # avoid modifying original
    df["cluster"] = labels

    # Calculate summary statistics
    summary = df.groupby("cluster").mean(numeric_only=True)

    # Optional: Add a basic interpretation based on summary
    cluster_descriptions = {}
    for idx, row in summary.iterrows():
        desc = []
        if row["monthly_spend"] > 2000:
            desc.append("high spender")
        if row["savings"] > 30000:
            desc.append("wealthy")
        if row["age"] < 30:
            desc.append("young")
        if row["num_txns"] > 60:
            desc.append("frequent user")

        label = ", ".join(desc) if desc else "unclassified"
        cluster_descriptions[idx] = label

    # Attach descriptions back to each row
    df["cluster_description"] = df["cluster"].map(cluster_descriptions)

    return df  # now includes cluster + description
