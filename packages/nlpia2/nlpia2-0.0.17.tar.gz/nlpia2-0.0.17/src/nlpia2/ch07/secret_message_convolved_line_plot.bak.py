import pandas as pd
from matplotlib import pyplot as plt
import seaborn

seaborn.set_theme('notebook')
seaborn.set_style('whitegrid')


df = pd.read_csv('secret_message_convolved_line_plot.csv', index_col=0)
figsize = (10, 6)
fig = plt.figure(figsize=figsize)
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
