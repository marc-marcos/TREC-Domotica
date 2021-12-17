import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time



data = pd.read_excel('excel.xlsx')
fig = plt.figure()
plt.plot(np.arange(0, len(data['Light Level'])), data['Light Level'])
# plt.ylim([40, 70])

plt.show()