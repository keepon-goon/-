import matplotlib.pyplot as plt

# 绘制图表
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("示例图表")

# 保存图表（确保在 plt.show() 之前调用）
plt.savefig("my_plot.png")  # 保存为 PNG 格式

# 显示图表（可选）
plt.show()