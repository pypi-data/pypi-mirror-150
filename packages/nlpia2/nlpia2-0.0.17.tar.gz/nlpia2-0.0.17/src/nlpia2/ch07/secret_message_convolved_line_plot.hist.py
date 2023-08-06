from scipy.io import wavfile
samplerate, data = wavfile.read('1210secretmorzecode.wav')
ls -hal
ls 1*
who
samplerate
data
data = data.abs()
data = np.abs(data)
import numpy as np
data = np.abs(data)
import pandas as pd
df = pd.DataFrame()
df['x'] = data[:3*samplerate]
df['t'] = range(len(df)) / samplerate
df['t'] = np.arange(len(df)) / samplerate
df
df = df.iloc[::samplerate / 100]
df.iloc[np.arange(0, samplerate / 100, -1)]
np.arange?
df.iloc[np.arange(0, -1, samplerate / 100)]
df.iloc[np.arange(0, None, samplerate / 100)]
df
samplerate
df.iloc[np.arange(0, len(df), samplerate / 100)]
df = df.iloc[np.arange(0, len(df), samplerate / 100)]
df
df.set_index('t')
df = df.set_index('t')
df.plot()
from matplotlib import pyplot as plt
plt.show()
df = df / 255
df
dot = [0] * 3 + [1] * 3 + [0] * 3
dash = [0] * 3 + [1] * 3 + [0] * 3
dash = [0] * 3 + [1] * 1 + [0] * 3
df.argmin()
df['x'].argmin()
df['x'][7]
df['x'].iloc[7]
i0 = df['x'].argmin()
df['x'].iloc[i0:].argmax()
i1 = df['x'].iloc[i0:].argmax()
i2 = df['x'].iloc[i1:].argmin()
i2
i2 = df['x'].iloc[i1+1:].argmin()
i2
i1 = df['x'].iloc[i0:].argmax()
i1
i2 = df['x'].iloc[i0+i1:].argmin()
i2
i1 = i0 + df['x'].iloc[i0:].argmax()
i2 = i1 + df['x'].iloc[i1:].argmin()
i3 = i2 + df['x'].iloc[i2:].argmax()
i1 - i0
i2 - i1
i3 - i2
dot = [0] * 6 + [1] * 6 + [0] * 6
dash = [0] * 6 + [1] * 6 * 3 + [0] * 6
df.convolve(dot)
df.x.convolve(dot)
df.x.values.convolve(dot)
np.convolve(df.x, dot)
df['dot'] = np.convolve(df.x, dot)
df['dot'] = [0] * (len(dot) / 2) + list(np.convolve(df.x, dot)) + [0] * (len(dot) / 2)
df['dot'] = [0] * int(len(dot) / 2) + list(np.convolve(df.x, dot)) + [0] * int(len(dot) / 2)
padlen = int(len(dot) / 2)
padlen
len(dot)
df['dot'] = np.convolve(df.x, dot)[padlen:-padlen]
df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
df.plot()
plt.show()
df.plot()
plt.show()
df['x'] - 1
4 * (df['x'] - .75)
df['x'] = 4 * (df['x'] - .75)
df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
df.plot()
plt.show()
dot = [-1] * 6 + [1] * 6 + [-1] * 6
dash = [-1] * 6 + [1] * 6 * 3 + [-1] * 6
df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
df['dash'] = np.convolve(df.x, dash)[padlen:-padlen+1]
padlen
dotpadlen = int(len(dot) / 2)
dashpadlen = int(len(dash) / 2)
df['dash'] = np.convolve(df.x, dash)[dashpadlen:-dashpadlen+1]
df['dot'] = np.convolve(df.x, dot)[dotpadlen:-dotpadlen+1]
df.plot()
plt.show()
df.plot()
plt.grid('on')
plt.show()
np.convolve?
df['dot'] = np.convolve(df.x, dot, mode='same')
df['dash'] = np.convolve(df.x, dash, mode='same')
df.plot()
plt.grid('on')
plt.show()
dot = np.array([-1] * 6 + [1] * 6 + [-1] * 6)
dot = dot / dot.abs().sum()
dot = dot / np.abs(dot).sum()
dot
dash = np.array([-1] * 6 + [1] * 6 * 3 + [-1] * 6)
dot = dash / np.abs(dash).sum()
dot = np.array([-1] * 6 + [1] * 6 + [-1] * 6)
dot = dot / np.abs(dot).sum()
dash = dash np.abs(dash).sum()
dash = dash / np.abs(dash).sum()
dash
df['dash'] = np.convolve(df.x, dash, mode='same')
df['dot'] = np.convolve(df.x, dot, mode='same')
df.plot()
plt.grid('on')
plt.show()
df.plot(style=['_','.','-'])
plt.show()
df.plot(style=['-','.','_'])
plt.grid('on')
plt.show()
df.plot(style=['-','.','_'], linewidth=[.5, 2, 4])
df['x'].plot(style='-', linewidth=.75, alpha=.5)
df['dot'].plot(style='.', linewidth=2, alpha=.75)
df['dash'].plot(style='_', linewidth=5, alpha=.75)
plt.show()
df['x'].plot(linestyle='solid', linewidth=1, alpha=1)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.4)
df['dot'].plot(linestyle='dotted', linewidth=4, alpha=.35)
plt.show()
df['x'].plot(linestyle='solid', linewidth=2.5, alpha=1)
df['dash'].plot(linestyle='dashed', linewidth=2.5, alpha=.4)
df['dot'].plot(linestyle='dotted', linewidth=2.5, alpha=.35)
plt.grid('on')
plt.show()
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2.5, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=3, alpha=1)
plt.grid('on')
plt.show()
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.legend()
plt.show()
hist -f code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.py
hist -o -p -f code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.md
import seaborn
seaborn.set_theme()
hist
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.legend()
plt.show()
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
seaborn.set_theme('whitegrid')
seaborn.set_theme('paper')
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
seaborn.set_theme('talk')
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
seaborn.set_theme('poster')
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
seaborn.set_theme('whitegrid')
seaborn.set_theme('notebook')
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
seaborn.set_style('whitegrid')
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
fig = plt.figure(figsize=(700,300))
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
fig = plt.figure(figsize=(10,4))
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
fig = plt.figure(figsize=(10,7))
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
fig = plt.figure(figsize=(10,6))
df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
plt.grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Signal amplitude (-1 to +1)')
plt.legend()
plt.show()
hist
df.to_csv('secret_message_convolved_line_plot.csv')
ls
cd ~/code/tangibleai/nlpia-manuscript/manuscript/images/
df.to_csv('secret_message_convolved_line_plot.csv')
df2 = pd.read_csv('secret_message_convolved_line_plot.csv', index_col=0)
df
from matplotlib import pyplot as plt
from urllib.request import urlretrieve
f = urlretrieve(url, 'titanic-distress-signal-simulated.wav')
hist
PKG_DIR = Path('/home/hobs/code/tangibleai/nlpia2/src/nlpia2')
from pathlib import Path
PKG_DIR = Path('/home/hobs/code/tangibleai/nlpia2/src/nlpia2')
PKG_NAME = PKG_DIR.name
SRC_DIR = PKG_DIR.parent
REPO_DIR = SRC_DIR.parent
MANUSCRIPT_DIR = REPO_DIR.parent / 'nlpia-manuscript' / 'manuscript'
IMAGES_DIR = MANUSCRIPT_DIR / 'images'
ADOC_DIR = MANUSCRIPT_DIR / 'adoc'
MANUSCRIPT_DIR.is_dir()
IMAGES_DIR
IMAGES_DIR.is_dir()
pwd
ls -hal
mv secret_message_convolved_line_plot.csv /home/hobs/.nlpia2-data/
hist -o -p -f /home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.md
hist -f /home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.py
