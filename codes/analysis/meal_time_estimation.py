import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# path settings
input_folder = r'C:\Users\adayc\Desktop\code\Drug\DA_data\CGM_id_only'
output_csv = r'C:\Users\adayc\Desktop\code\Drug\reports\results\Tables\estimated_meal_times.csv'
cluster_plot_dir = r'C:\Users\adayc\Desktop\code\Drug\reports\results\figures\meal_time'
os.makedirs(cluster_plot_dir, exist_ok=True)

results = []

def estimate_meal_times(df_day):
    df_day = df_day.sort_values(by='时间').reset_index(drop=True)
    df_day['glucose_smooth'] = df_day['葡萄糖'].rolling(window=3, center=True).mean()
    df_day['delta'] = df_day['glucose_smooth'].diff()

    peaks, _ = find_peaks(df_day['delta'].fillna(0), distance=4, height=0.1)
    if len(peaks) < 4:
        return []

    peak_times = df_day.loc[peaks, '时间'].dt.hour + df_day.loc[peaks, '时间'].dt.minute / 60.0
    peak_time_values = peak_times.values.reshape(-1, 1)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto').fit(peak_time_values)
    clustered_peaks = pd.DataFrame({
        'time': peak_times.values,
        'label': kmeans.labels_
    })

    centers = clustered_peaks.groupby('label')['time'].mean()

    # Meal time ranges
    meal_ranges = {
        'Meal1': (6, 9),
        'Meal2': (11, 13),
        'Meal3': (16, 18),
        'Meal4': (19, 23)
    }

    selected_meals = []
    for meal_name, (start, end) in meal_ranges.items():
        in_range = centers[(centers >= start) & (centers <= end)]
        if not in_range.empty:
            center_val = in_range.iloc[0]
            nearest_peak = clustered_peaks.loc[(clustered_peaks['time'] >= start) & 
                                               (clustered_peaks['time'] <= end)]
            if not nearest_peak.empty:
                nearest_center = nearest_peak.groupby('label')['time'].mean().sub(center_val).abs().idxmin()
                true_time = centers[nearest_center]
                selected_meals.append(f"{int(true_time)}:{int((true_time % 1)*60):02d}")
            else:
                selected_meals.append(None)
        else:
            selected_meals.append(None)

    # save cluster plot
    plt.figure(figsize=(6, 4))
    plt.scatter(peak_times, [1]*len(peak_times), c=kmeans.labels_, cmap='tab10')
    for center in centers:
        plt.axvline(center, color='gray', linestyle='--', alpha=0.5)
    plt.title(f'{patient_id} {date} Clustered Meal Times')
    plt.xlabel('Time (hours)')
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(os.path.join(cluster_plot_dir, f'{patient_id}_{date}_clusters.png'))
    plt.close()

    return selected_meals if all(m is not None for m in selected_meals) else []


# read files
for i in range(201):
    filename = f'DA{i:03d}.txt'
    file_path = os.path.join(input_folder, filename)

    if not os.path.exists(file_path):
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            _ = f.readline()   # skip header
            df = pd.read_csv(f, sep='\t')
        
        patient_id = os.path.splitext(filename)[0]

        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
        df = df.dropna(subset=['时间'])
        df['葡萄糖'] = pd.to_numeric(df['葡萄糖历史记录（mmol/L）'], errors='coerce')
        df = df.dropna(subset=['葡萄糖'])
        df['日期'] = df['时间'].dt.date

    except Exception as e:
        print(f"failed {e}")
        continue

    # Day
    for date, df_day in df.groupby('日期'):
        est_meals = estimate_meal_times(df_day)
        if len(est_meals) == 4:
            results.append([patient_id, date] + est_meals)

# save CSV
df_result = pd.DataFrame(results, columns=['PatientID', 'Date', 'Meal1', 'Meal2', 'Meal3', 'Meal4'])
df_result.to_csv(output_csv, index=False, encoding='utf-8-sig')

print('finished', output_csv)
