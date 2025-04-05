import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import db_config

def get_anpr_data(weather_filter="All"):
    """Fetch data from database with optional weather filter"""
    conn = db_config.get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        t.weather_condition,
        AVG(t.processing_time) AS traditional_time,
        AVG(y.processing_time) AS yolo_time,
        SUM(t.false_positive) AS traditional_fp,
        SUM(y.false_positive) AS yolo_fp,
        SUM(t.false_negative) AS traditional_fn,
        SUM(y.false_negative) AS yolo_fn
    FROM traditional_anpr t
    JOIN yolo_v11_anpr y ON t.weather_condition = y.weather_condition
    GROUP BY t.weather_condition;
    """
    
    df = pd.read_sql(query, conn)
    cursor.close()
    conn.close()
    
    if weather_filter != "All":
        df = df[df['weather_condition'] == weather_filter]
    
    return df

def create_plot(graph_type="Processing Time", weather_filter="All", ax=None):
    """Create plot for PyQt application"""
    df = get_anpr_data(weather_filter)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))
    else:
        fig = ax.figure
    
    ax.clear()
    ax.set_facecolor('white')
    
    x = np.arange(len(df['weather_condition']))
    width = 0.4
    
    if graph_type == "Processing Time":
        traditional_bars = ax.bar(x - width/2, df['traditional_time'], width, 
                                color='#1E90FF', label='Traditional ANPR')
        yolo_bars = ax.bar(x + width/2, df['yolo_time'], width, 
                          color='#FF6347', label='YOLO v11 ANPR')
        ylabel = 'Processing Time (s)'
    elif graph_type == "False Positives":
        traditional_bars = ax.bar(x - width/2, df['traditional_fp'], width, 
                                color='#1E90FF', label='Traditional ANPR')
        yolo_bars = ax.bar(x + width/2, df['yolo_fp'], width, 
                          color='#FF6347', label='YOLO v11 ANPR')
        ylabel = 'False Positives Count'
    else:  # False Negatives
        traditional_bars = ax.bar(x - width/2, df['traditional_fn'], width, 
                                color='#1E90FF', label='Traditional ANPR')
        yolo_bars = ax.bar(x + width/2, df['yolo_fn'], width, 
                          color='#FF6347', label='YOLO v11 ANPR')
        ylabel = 'False Negatives Count'
    
    # Add value labels
    for bars in [traditional_bars, yolo_bars]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, 
                   f'{height:.2f}' if graph_type == "Processing Time" else f'{int(height)}', 
                   ha='center', va='bottom', fontweight='bold', color='white')
    
    # Customize plot
    ax.set_xlabel('Weather Condition', fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(f'ANPR {graph_type} Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df['weather_condition'], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig