from sklearn.cluster import KMeans

def cluster_logic(df, k=3):
    features = df[["age", "monthly_spend", "num_txns", "savings"]]
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(features)
    return labels.tolist()
