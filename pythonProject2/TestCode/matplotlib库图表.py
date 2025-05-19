import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')# 设置 Matplotlib 后端为 TkAgg，避免 PyCharm 兼容性问题
# 创建示例数据（实际中可能从文件读取）
data = {
    'datetime': pd.date_range(start='2023-01-01', periods=5, freq='D'),
    'PM2.5': [35, 42, 38, 29, 45],
    'PM10': [65, 70, 58, 50, 75]
}
air_quality = pd.DataFrame(data).set_index('datetime')

# # 绘制数据（自动创建图表）
air_quality.plot()
fig, axs = plt.subplots(figsize=(12, 4))

air_quality.plot.area(ax=axs)#将面积图绘制在已有的 axs 子图上，而非创建新的图表。

axs.set_ylabel("NO$_2$ concentration")

fig.savefig("no2_concentrations.png")

# 在普通 Python 脚本中需要这行，Jupyter 中可省略
plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
#
# # 创建一个包含2个子图的图表
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
#
# # 设置整个图表的标题
# fig.suptitle('Two Subplots')
#
# # 在第一个子图上绘制正弦曲线
# x = np.linspace(0, 2 * np.pi, 100)
# axs[0].plot(x, np.sin(x))
# axs[0].set_title('Sin Curve')
#
# # 在第二个子图上绘制余弦曲线
# axs[1].plot(x, np.cos(x))
# axs[1].set_title('Cos Curve')
#
# plt.show()
# # import sys
# # print(sys.executable)