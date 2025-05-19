import logging
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

matplotlib.use('TkAgg')  # 设置 Matplotlib 后端为 TkAgg，避免 PyCharm 兼容性问题
# 设置中文字体，确保中文正常显示
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun"]
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False
adress = r"C:\Users\lenovo\Desktop\课程开发平台试验excel表.xlsx"
excel_file = pd.ExcelFile(adress)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(levelname)s:%(message)s')


def sum_score_picture():
    '''
    生成试题与成绩分析表的数据分析图
    :return每个区间的人数列表
    '''
    df = excel_file.parse('学生成绩')[3:]  # 截取掉非所需班级的学生
    # 创建画布和子图
    fig, ax = plt.subplots(figsize=(8, 6))
    # 绘制不同分数区间的学生直方图
    wb = load_workbook(adress)
    ws = wb['学生成绩']
    # 忽略返回的区间边界值和直方图对象列表,n为每个区间的人数<numpy.ndarray>
    n, _, _ = ax.hist(df['总成绩'], bins=[0, 60, 70, 80, 90, 101],
                      color='skyblue', edgecolor='black')
    ax.set_title('总成绩分布')
    ax.set_xlabel('分数')
    ax.set_ylabel('学生人数')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # 保存图片
    save_path = r'E:\课程达成度平台开发数据分析图片\成绩区间分布图.png'
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info('successfully save 成绩区间分布图.png')
    return [int(x) for x in n]


def question_type_scoring_rate_picture():
    '''
    生成四种题型的得分率数据分析图
    :return:四种题型的得分率列表
    '''
    df = excel_file.parse('考试成绩')[4:]  # 截取掉非所需班级的学生
    question_types = ['选择题', '填空题', '程序分析题', '编程题']
    total_scores = [20, 20, 20, 40]
    # 将各题型总分变为Series类型
    total_scores_series = pd.Series(total_scores, index=question_types) * len(
        df)
    # 计算各题型总得分并处理为Series类型
    get_scores = df[question_types].sum()
    # 计算得分率
    scores_rates = get_scores / total_scores_series  # 逐行计算
    # 绘制数据分析图
    plt.figure(figsize=(8, 6))
    plt.bar(question_types, scores_rates)
    plt.title('不同题型得分率')
    plt.xlabel('题型')
    plt.ylabel('得分率')
    save_path = r'E:\课程达成度平台开发数据分析图片\题型得分率图.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info('successfully save 题型得分率图.png')
    # 返回得分率列表
    rate_list = scores_rates.tolist()
    rate_list = [round(x, 2) for x in rate_list]
    return rate_list


def goal_achievement_rate():
    '''
    生成考核总分，考核平均分，目标达成率数据分析图
    :return:[(考核总分，考核平均分，课程目标达成率)]
    '''
    # 截取掉非所需班级的学生,指定列名为第二行
    df = excel_file.parse('达成度汇总', header=1)[4:]
    goal_types = ['目标1', '目标2', '目标3']
    total_scores = [40, 40, 20]
    # 计算各目标总分
    total_scores_series = pd.Series(total_scores, index=goal_types)
    # 计算平均得分
    get_scores_average = df[['目标1.3', '目标2.3', '目标3.1']].sum() / len(df)
    # 计算返回列表
    goal_achievement_list = [(x, y, '{}%'.format(round((y / x) * 100))) for x, y
                             in zip(total_scores, get_scores_average.tolist())]
    # 绘制数据分析图
    fig, ax1 = plt.subplots(figsize=(8, 6))
    # 绘制左侧Y轴对应的考核平均分柱状图
    ax1.bar(goal_types, get_scores_average, color='skyblue',
            label='考核平均分')  # label设置标签图例
    ax1.set_ylabel('分数', color='blue')  # 在 Y 轴左侧显示文本 “分数”，颜色为蓝色，
    ax1.tick_params(axis='y',
                    labelcolor='blue')  # 设置坐标轴刻度线和刻度标签的样式,axis指定操作对象为 Y 轴
    # 绘制右侧Y轴对应的课程目标达成率折线图
    ax2 = ax1.twinx()  # 与ax1共享一个x轴
    ax2.plot(goal_types, [x[2] for x in goal_achievement_list], color='red',
             marker='o', label='课程目标达成率')  # marker设置数据点的标记形状为圆形
    ax2.set_ylabel('百分比(%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    # 添加标题和图例
    plt.title('课程目标达成度情况')
    ax1.legend(loc='upper left')  # 在图表左上角添加图例
    ax2.legend(loc='upper right')
    save_path = r'E:\课程达成度平台开发数据分析图片\课程目标达成度情况图.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info('successfully save 课程目标达成度情况图.png')
    return goal_achievement_list


def segmentation_achievement():
    '''
    生成课程目标达成情况(分段统计)表
    :return:不同分数的三个目标得分率，
    如:[[0.47, 0.35, 0.38, (0, 60)], [0.64, 0.68, 0.65, (60, 70)],
    [0.75, 0.76, 0.0, (70, 80)], [0.85, 0.84, 0.8, (80, 90)], [0.0, 0.94, 0.92,
    (90, 100)]]
    '''
    # 截取掉非所需班级的学生,指定列名为第二行
    df = excel_file.parse('达成度汇总', header=1)[4:]
    goal_types = ['目标1.4', '目标2.4', '目标3.2']
    # 计算:return:不同分数的三个目标得分率
    goal_rate_list = [
        segmentation_achievement2(10 * i, 10 * (i + 1), df, goal_types) for i in
        range(6, 10)]
    goal_rate_list.insert(0, segmentation_achievement2(0, 60, df, goal_types))
    # 绘制数据分析图
    plt.figure(figsize=(8, 6))
    data = [x[:3] for x in goal_rate_list]  # 各个分数段的得分率
    labels = [str(x[-1]) for x in goal_rate_list]  # 各个分数段
    # 初始化底部高度为0，每次绘制完一个目标就加上其五个分数段的高度，下一目标在此高度上进行绘制
    bottom = [0.0] * len(labels)
    width = 0.6
    for i in range(len(data[0])):  # 遍历三个目标
        # 提取当前目标的所有分数段数据
        current_scores = [row[i] for row in data]
        # labels为x坐标轴，label为图例
        plt.bar(labels, current_scores, width, bottom=bottom,
                label=f'目标{i + 1}')
        # 更新底部高度
        bottom = [bottom[j] + current_scores[j] for j in range(len(labels))]
    plt.xlabel('分数段')
    plt.ylabel('得分率')
    plt.title('不同分数段三个目标得分率')
    plt.legend()  # 自动读取图例并为图表添加
    save_path = r'E:\课程达成度平台开发数据分析图片\不同分数段三个目标得分率图.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info('successfully save 不同分数段三个目标得分率图.png')
    return goal_rate_list


def segmentation_achievement2(start_score, end_score, df, goal_tpyes):
    '''
    计算传入分段的三个目标得分率
    :goal_tpyes:三个目标的列名
    :return: (分段的三个目标得分率)
    '''
    lst = []
    for col in goal_tpyes:  # 遍历每一个目标进行处理
        if end_score == 100:
            df_score = df[(df[col] >= start_score * 0.01) & (
                    df[col] <= end_score * 0.01)]  # df_score为满足分数的学生
        else:
            df_score = df[(df[col] >= start_score * 0.01) & (
                    df[col] < end_score * 0.01)]  # df_score为满足分数的学生
        # print(df_score)
        # 处理空数据情况
        if len(df_score) == 0:
            lst.append(0.0)
            continue
        # 计算得分率（百分比）
        avg_score = df_score[col].mean()
        lst.append(avg_score)
    return [float(round(x, 2)) for x in lst] + [
        (start_score, end_score)]  # 将 np.float64类型的数据转换为float 类型


def main():
    score_list = sum_score_picture()
    rate_list = question_type_scoring_rate_picture()
    goal_achievement_list = goal_achievement_rate()
    goal_rate_list = segmentation_achievement()
    with open("F:\代码\Python代码\课程达成度平台开发\pythonProject2\excel表统计数据",'w') as file:
        file.write(str(score_list) + '\n')
        file.write(str(rate_list) + '\n')
        file.write(str(goal_achievement_list) + '\n')
        file.write(str(goal_rate_list) + '\n')
    print(score_list)
    print(rate_list)
    print(goal_achievement_list)
    print(goal_rate_list)


if __name__ == '__main__':
    main()
