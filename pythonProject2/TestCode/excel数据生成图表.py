import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，确保中文正常显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取 Excel 文件
excel_file = pd.ExcelFile('scores.xlsx')
df = excel_file.parse('Sheet1')  # 读取指定工作表中的数据

# 数据预览
print("数据基本信息：")
df.info()

# 计算平均分
average_scores = df[['数学', '语文', '英语']].mean()
print("\n各科平均分：")
print(average_scores)#average_scores 的类型是 Pandas 的 Series 对象

# 创建画布和两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))#见笔记-suoplots

# 子图1：数学成绩分布直方图
ax1.hist(df['数学'], bins=10, color='skyblue', edgecolor='black')
ax1.set_title('数学成绩分布')
ax1.set_xlabel('分数')
ax1.set_ylabel('学生人数')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 子图2：各科平均分对比条形图
ax2.bar(average_scores.index, average_scores.values, color=['#ff9999', '#99ff99', '#99ccff'])
ax2.set_title('各科平均分对比')
ax2.set_xlabel('科目')
ax2.set_ylabel('平均分')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 自动调整布局
plt.tight_layout()

# 显示图表
plt.show()