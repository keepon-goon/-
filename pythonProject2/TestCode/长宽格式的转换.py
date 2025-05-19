import pandas as pd
import numpy as np

# 宽格式示例（每列是一个站点，每行是一个时间点）
no2_pivoted = pd.DataFrame({
    'date.utc': ['2019-04-09 01:00:00+00:00', '2019-04-09 02:00:00+00:00'],
    'BETR801': [22.5, 53.5],
    'FR04014': [24.4, 27.4],
    'London Westminster': [np.nan, 67.0]
})

print(no2_pivoted)


no_2 = no2_pivoted.melt(id_vars="date.utc")
#该方法会将所有未在 id_vars 中提及的列熔化成两个列：一个包含列头名称的列，以及一个包含值本身的列。后一个列默认名为 value
print(no_2)