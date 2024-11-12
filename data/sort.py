import pandas as pd

# 读取 Excel 文件
file_path = "./times.csv"  # 替换为你的文件路径
df = pd.read_csv(file_path)
df = df.sort_values('time', ascending=True)
# 初始化变量
max_tasks = 0
current_tasks = 0

print(df)
# 遍历所有的事件
for _, row in df.iterrows():
    if row['type'] == 'start':
        current_tasks += 1  # 起始时间，增加任务数
    else:
        current_tasks -= 1  # 结束时间，减少任务数

    max_tasks = max(max_tasks, current_tasks)  # 更新最大同时运行任务数

print(f"同时运行中的最大行数是：{max_tasks}")
