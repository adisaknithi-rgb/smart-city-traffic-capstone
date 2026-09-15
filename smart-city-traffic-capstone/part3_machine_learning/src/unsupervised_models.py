import os
import logging
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules

logger = logging.getLogger(__name__)

def run_kmeans_clustering(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """Task 2A: K-Means Clustering จัดกลุ่มสภาวะการจราจร"""
    logger.info("--- Starting Task 2A: K-Means Clustering (K=%d) ---", n_clusters)
    
    cluster_features = ["traffic_volume", "temp", "hour_sin", "hour_cos", "is_low_visibility"]
    X = df[cluster_features].dropna()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_clustered = df.copy()
    df_clustered["cluster"] = kmeans.fit_predict(X_scaled)
    
    # สรุปค่าเฉลี่ยของแต่ละ Cluster เพื่อนำไปเขียนผลตีความ
    cluster_summary = df_clustered.groupby("cluster")[cluster_features].mean()
    logger.info("K-Means Cluster Summary:\n%s", cluster_summary.to_string())
    
    return df_clustered

def run_association_rules(df: pd.DataFrame, min_support: float = 0.03, min_lift: float = 1.2):
    """Task 2B: Association Rule Mining ค้นหากฎความสัมพันธ์ของ Congestion"""
    logger.info("--- Starting Task 2B: Association Rule Mining ---")
    
    df_basket = pd.DataFrame()
    
    # 1. Discretization / Categorical Binning
    df_basket["Is_Weekday"] = df["date_time"].dt.dayofweek.apply(lambda x: "Weekday" if x < 5 else "Weekend")
    
    def get_time_slot(hour):
        if 6 <= hour <= 9: return "Time_MorningPeak"
        elif 10 <= hour <= 15: return "Time_Day"
        elif 16 <= hour <= 19: return "Time_EveningPeak"
        else: return "Time_Night"
        
    df_basket["Time_Slot"] = df["date_time"].dt.hour.apply(get_time_slot)
    df_basket["Weather"] = df["weather_main"].apply(lambda x: f"Weather_{x}")
    df_basket["Congestion"] = df["congestion_category"].apply(lambda x: f"Congestion_{x}")
    
    # 2. One-Hot Encoding
    basket_sets = pd.get_dummies(df_basket)
    
    # 3. Mining Frequent Itemsets & Rules
    frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    
    # กรองเฉพาะกฎที่นำไปสู่ผลลัพธ์ Congestion_High หรือ Congestion_Severe
    target_rules = rules[rules["consequents"].apply(lambda x: any("Congestion_High" in item or "Congestion_Severe" in item for item in x))]
    target_rules = target_rules.sort_values(by="lift", ascending=False)
    
    logger.info("Top 5 Association Rules for High/Severe Congestion:\n%s", 
                target_rules[["antecedents", "consequents", "support", "confidence", "lift"]].head(5).to_string())
    
    return target_rules

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/unsupervised_models.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    from src.data_processing import process_pipeline
    df_processed = process_pipeline("data/featured_traffic_data.csv")
    
    # รัน Task 2
    clustered_df = run_kmeans_clustering(df_processed, n_clusters=3)
    rules_df = run_association_rules(df_processed)
    logger.info("Unsupervised Task 2 completed successfully. Audit log saved to logs/unsupervised_models.log")