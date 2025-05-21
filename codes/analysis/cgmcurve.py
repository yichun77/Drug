import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# path
input_folder = r'C:\Users\adayc\Desktop\code\Drug\DA_data\CGM_id_only'      
output_folder = r'C:\Users\adayc\Desktop\code\Drug\reports\results\figures\CGM_curve'   
os.makedirs(output_folder, exist_ok=True)

# read all TXT files
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        patient_id = filename.split('.')[0]  # ID
        file_path = os.path.join(input_folder, filename)

        # output path
        patient_folder = os.path.join(output_folder, patient_id)
        os.makedirs(patient_folder, exist_ok=True)

        # read data
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8', skiprows=1)
        df = df.iloc[1:].reset_index(drop=True)
        df['时间'] = pd.to_datetime(df['时间'])
        df['日期'] = df['时间'].dt.date

        # plot daily glucose curves
        for date, group in df.groupby('日期'):
            plt.figure(figsize=(10, 4))
            plt.plot(group['时间'], group['葡萄糖历史记录（mmol/L）'], marker='o', linestyle='-')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.title(f'{patient_id} Blood Glucose Curve ({date})')
            plt.xlabel('Time (hour)')
            plt.ylabel('Blood Glucose (mmol/L)')
            plt.xticks(rotation=30)
            plt.grid(True)
            plt.tight_layout()

            # save the plot
            save_path = os.path.join(patient_folder, f'{date}.png')
            plt.savefig(save_path)
            plt.close()

print("finished")
