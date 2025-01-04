import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import configparser
import os
import sys
import datetime

print(f"Using Python executable: {sys.executable}")

config_path = 'config.ini'

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
working_dir = os.getcwd()

file_path = os.path.join(working_dir, config_path)

# print(current_file_path)
# print(current_dir)
# print(working_dir)
print(file_path)

config = configparser.ConfigParser()
config.read(file_path)

def find_top_scores(heatmap, top_n=2):
    flattened = heatmap.flatten()
    indices = flattened.argsort()[::-1]  # เรียงค่าจากมากไปน้อย
    unique_scores = set()  # เก็บคะแนนที่เจอแล้ว
    top_scores = []

    for i in indices:
        score = flattened[i]
        if score > 0 and score not in unique_scores:
            unique_scores.add(score)  # เพิ่มคะแนนลงในเซ็ต
            positions = np.where(heatmap == score)
            cells = [f"{row * 10 + col}" for row, col in zip(positions[0], positions[1])]
            top_scores.append((score, cells))
            if len(top_scores) == top_n:  # ถ้าครบจำนวนที่ต้องการแล้ว ให้หยุด
                break

    return top_scores

if 'History' not in config.sections():
    print("Program completed. Press Enter to exit...")
    input()

# ดึงข้อมูล upper_data และ lower_data
upper_data = config.get('History', 'upper_data').split(', ')
lower_data = config.get('History', 'lower_data').split(', ')

## สร้างข้อมูลตัวเลข 2 หลักแบบสุ่ม (upper และ lower)
# upper_data = ['93', '53', '36', '57', '18', '98', '01', '41', '92', '85', '89', '67', '65']
# lower_data = ['44', '63', '90', '54', '93', '94', '46', '37', '50', '92', '99', '86', '92']

# แปลงข้อมูลเป็นตัวเลข
upper_data = [int(i) for i in upper_data]
lower_data = [int(i) for i in lower_data]

# สร้าง 2D array สำหรับ heatmap (00-99)
upper_heatmap = np.zeros((10, 10))
lower_heatmap = np.zeros((10, 10))
combined_heatmap = np.zeros((10, 10))

modified_heatmap = np.zeros_like(combined_heatmap)

# ทิศทางการเพิ่มหรือลดค่าตำแหน่ง
directions = [-1, 1, 9, -9, 10, -10, 11, -11]

# เติมข้อมูลลงใน heatmap
for value in upper_data:
    row, col = divmod(value, 10)
    upper_heatmap[row, col] += 1

for value in lower_data:
    row, col = divmod(value, 10)
    lower_heatmap[row, col] += 1

for value in upper_data + lower_data:
    row, col = divmod(value, 10)
    combined_heatmap[row, col] += 1

for row in range(combined_heatmap.shape[0]):
    for col in range(combined_heatmap.shape[1]):
        if combined_heatmap[row, col] >= 1:
            # คำนวณค่าตำแหน่งใหม่ตาม directions
            for direction in directions:
                new_value = (row * 10 + col) + direction
                if 0 <= new_value < 100:  # ตรวจสอบว่าค่าที่ได้อยู่ในช่วง 0-99
                    new_row, new_col = divmod(new_value, 10)
                    modified_heatmap[new_row, new_col] += 1


# คำนวณ top 3 scores สำหรับ modified heatmap
top_scores = find_top_scores(modified_heatmap, top_n=3)
# print("Top scores in Modified Heatmap:")
# for score, cells in top_scores:
#     print(f"Score {int(score)}: {', '.join(cells)}")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"{timestamp}.txt"

# เขียนผลลัพธ์ลงในไฟล์
with open(output_filename, "w") as file:
    file.write("Top scores in Modified Heatmap:\n")
    for score, cells in top_scores:
        file.write(f"Score {int(score)}: {', '.join(cells)}\n")

print(f"Results written to {output_filename}")


# Plot heatmap
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
sns.heatmap(upper_heatmap, annot=True, fmt='.0f', cmap='coolwarm', ax=axes[0,0], xticklabels=range(10), yticklabels=range(10))
axes[0,0].set_title("Heatmap of Upper Data")
axes[0,0].set_xlabel("Column (0-9)")
axes[0,0].set_ylabel("Row (0-9)")

sns.heatmap(lower_heatmap, annot=True, fmt='.0f', cmap='coolwarm', ax=axes[0,1], xticklabels=range(10), yticklabels=range(10))
axes[0,1].set_title("Heatmap of Lower Data")
axes[0,1].set_xlabel("Column (0-9)")
axes[0,1].set_ylabel("Row (0-9)")

sns.heatmap(combined_heatmap, annot=True, fmt='.0f', cmap='coolwarm', ax=axes[1,0], xticklabels=range(10), yticklabels=range(10))
axes[1,0].set_title("Combined Heatmap of Upper and Lower Data")
axes[1,0].set_xlabel("Column (0-9)")
axes[1,0].set_ylabel("Row (0-9)")

sns.heatmap(modified_heatmap, annot=True, fmt='.0f', cmap='coolwarm', ax=axes[1,1], xticklabels=range(10), yticklabels=range(10))
axes[1,0].set_title("Modify Heatmap of Upper and Lower Data")
axes[1,0].set_xlabel("Column (0-9)")
axes[1,0].set_ylabel("Row (0-9)")

fig.canvas.manager.set_window_title("Data History")

plt.tight_layout()
plt.show()
