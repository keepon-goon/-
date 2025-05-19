import matplotlib
import matplotlib.pyplot as plt


# 获取系统中文字体列表（可查看有哪些字体可用）
print(plt.rcParams["font.family"])  # 查看当前字体
print(matplotlib.font_manager.fontManager.ttflist)  # 打印所有可用字体名称

# # 直接指定系统中已有的中文字体名称（例如黑体、微软雅黑等）
# plt.rcParams["font.family"] = "SimHei"  # 黑体
# # 或 plt.rcParams["font.family"] = "Microsoft YaHei"  # 微软雅黑