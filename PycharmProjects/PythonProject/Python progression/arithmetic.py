from pydoc_data import module_docs

import numpy as np

math = np.array([85, 92, 67, 74, 96])
physics = np.array([78, 88, 72, 81, 94])

print(math+physics)

mean = [(math+physics)/2]
print(mean)
mean = (math+physics)/2
good_average = (mean >= 80)
print(good_average)
wow_average = (math > 90) | (physics > 90)
print(wow_average)
midwow_average =(math > 80)&(physics >80)
print(midwow_average)


