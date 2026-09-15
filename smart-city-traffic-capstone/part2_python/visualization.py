import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# ตั้งค่า Logging ให้อ่านไฟล์ pipeline.log เดียวกับ Pipeline หลัก
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_visualizations(data_path: str = "featured_traffic_data.csv", output_dir: str = "outputs"):
    """
    สร้างรูปภาพวิเคราะห์ Visualizations 3 รูปแบบ และเซฟลงโฟลเดอร์ outputs/ 
    พร้อมบันทึก INFO log ยืนยันเส้นทางไฟล์ตามเกณฑ์ NUS
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    df['date_time'] = pd.to_datetime(df['date_time'])

    sns.set_theme(style="whitegrid")

    # --- Figure 1: Hourly Traffic Demand (Weekday vs Weekend) ---
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='hour', y='traffic_volume', hue='is_weekend', palette={0: '#1f77b4', 1: '#ff7f0e'}, ci=None, marker='o')
    plt.title('Figure 1: Average Traffic Demand by Hour (Weekday vs Weekend)', fontsize=12, fontweight='bold')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Average Traffic Volume')
    plt.legend(title='Day Type', labels=['Weekday', 'Weekend'])
    plt.tight_layout()
    
    fig1_path = os.path.join(output_dir, 'traffic_hourly_demand.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    logger.info(f"Successfully generated and saved figure to '{fig1_path}'")

    # --- Figure 2: Traffic Volume Distribution across Congestion Levels ---
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x='congestion_level', y='traffic_volume', order=['Low', 'Medium', 'High'], palette='Blues')
    plt.title('Figure 2: Traffic Volume Distribution across Target Congestion Levels', fontsize=12, fontweight='bold')
    plt.xlabel('Congestion Target Level')
    plt.ylabel('Traffic Volume')
    plt.tight_layout()
    
    fig2_path = os.path.join(output_dir, 'traffic_distribution_congestion.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    logger.info(f"Successfully generated and saved figure to '{fig2_path}'")

    # --- Figure 3: Temperature vs Traffic Volume by Severe Weather ---
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df.sample(n=2000, random_state=42), x='temp_celsius', y='traffic_volume', hue='is_severe_weather', alpha=0.6, palette={0: '#2ca02c', 1: '#d62728'})
    plt.title('Figure 3: Temperature (°C) vs Traffic Volume by Severe Weather Condition', fontsize=12, fontweight='bold')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Traffic Volume')
    plt.legend(title='Condition', labels=['Normal', 'Severe Weather'])
    plt.tight_layout()
    
    fig3_path = os.path.join(output_dir, 'traffic_weather_relationship.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    logger.info(f"Successfully generated and saved figure to '{fig3_path}'")

if __name__ == "__main__":
    logger.info("Starting Task 3: Data Visualization Module...")
    generate_visualizations()
    logger.info("Task 3 Visualizations completed successfully.")