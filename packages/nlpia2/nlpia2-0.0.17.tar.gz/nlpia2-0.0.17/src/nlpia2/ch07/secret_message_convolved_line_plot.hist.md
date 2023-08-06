>>> from scipy.io import wavfile
... samplerate, data = wavfile.read('1210secretmorzecode.wav')
...
>>> ls -hal
>>> ls 1*
>>> who
>>> samplerate
4000
>>> data
array([255,   0, 255, ...,   0, 255,   0], dtype=uint8)
>>> data = data.abs()
>>> data = np.abs(data)
>>> import numpy as np
>>> data = np.abs(data)
>>> import pandas as pd
>>> df = pd.DataFrame()
>>> df['x'] = data[:3*samplerate]
>>> df['t'] = range(len(df)) / samplerate
>>> df['t'] = np.arange(len(df)) / samplerate
>>> df
         x        t
0      255  0.00000
1        0  0.00025
2      255  0.00050
3        0  0.00075
4      255  0.00100
...    ...      ...
11995    0  2.99875
11996  255  2.99900
11997    0  2.99925
11998  255  2.99950
11999    0  2.99975

[12000 rows x 2 columns]
>>> df = df.iloc[::samplerate / 100]
>>> df.iloc[np.arange(0, samplerate / 100, -1)]
Empty DataFrame
Columns: [x, t]
Index: []
>>> np.arange?
>>> df.iloc[np.arange(0, -1, samplerate / 100)]
Empty DataFrame
Columns: [x, t]
Index: []
>>> df.iloc[np.arange(0, None, samplerate / 100)]
Empty DataFrame
Columns: [x, t]
Index: []
>>> df
         x        t
0      255  0.00000
1        0  0.00025
2      255  0.00050
3        0  0.00075
4      255  0.00100
...    ...      ...
11995    0  2.99875
11996  255  2.99900
11997    0  2.99925
11998  255  2.99950
11999    0  2.99975

[12000 rows x 2 columns]
>>> samplerate
4000
>>> df.iloc[np.arange(0, len(df), samplerate / 100)]
         x     t
0      255  0.00
40     255  0.01
80     255  0.02
120    255  0.03
160    255  0.04
...    ...   ...
11800  255  2.95
11840  255  2.96
11880  255  2.97
11920  255  2.98
11960  255  2.99

[300 rows x 2 columns]
>>> df = df.iloc[np.arange(0, len(df), samplerate / 100)]
>>> df
         x     t
0      255  0.00
40     255  0.01
80     255  0.02
120    255  0.03
160    255  0.04
...    ...   ...
11800  255  2.95
11840  255  2.96
11880  255  2.97
11920  255  2.98
11960  255  2.99

[300 rows x 2 columns]
>>> df.set_index('t')
        x
t        
0.00  255
0.01  255
0.02  255
0.03  255
0.04  255
...   ...
2.95  255
2.96  255
2.97  255
2.98  255
2.99  255

[300 rows x 1 columns]
>>> df = df.set_index('t')
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> from matplotlib import pyplot as plt
>>> plt.show()
>>> df = df / 255
>>> df
        x
t        
0.00  1.0
0.01  1.0
0.02  1.0
0.03  1.0
0.04  1.0
...   ...
2.95  1.0
2.96  1.0
2.97  1.0
2.98  1.0
2.99  1.0

[300 rows x 1 columns]
>>> dot = [0] * 3 + [1] * 3 + [0] * 3
>>> dash = [0] * 3 + [1] * 3 + [0] * 3
>>> dash = [0] * 3 + [1] * 1 + [0] * 3
>>> df.argmin()
>>> df['x'].argmin()
7
>>> df['x'][7]
>>> df['x'].iloc[7]
0.5019607843137255
>>> i0 = df['x'].argmin()
>>> df['x'].iloc[i0:].argmax()
6
>>> i1 = df['x'].iloc[i0:].argmax()
>>> i2 = df['x'].iloc[i1:].argmin()
>>> i2
1
>>> i2 = df['x'].iloc[i1+1:].argmin()
>>> i2
0
>>> i1 = df['x'].iloc[i0:].argmax()
>>> i1
6
>>> i2 = df['x'].iloc[i0+i1:].argmin()
>>> i2
7
>>> i1 = i0 + df['x'].iloc[i0:].argmax()
>>> i2 = i1 + df['x'].iloc[i1:].argmin()
>>> i3 = i2 + df['x'].iloc[i2:].argmax()
>>> i1 - i0
6
>>> i2 - i1
7
>>> i3 - i2
6
>>> dot = [0] * 6 + [1] * 6 + [0] * 6
>>> dash = [0] * 6 + [1] * 6 * 3 + [0] * 6
>>> df.convolve(dot)
>>> df.x.convolve(dot)
>>> df.x.values.convolve(dot)
>>> np.convolve(df.x, dot)
array([0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 1.        , 2.        , 3.        , 4.        ,
       5.        , 6.        , 6.        , 5.50196078, 5.00392157,
       4.50588235, 4.00784314, 3.50980392, 3.01176471, 3.50980392,
       4.00784314, 4.50588235, 5.00392157, 5.50196078, 6.        ,
       6.        , 5.50196078, 5.00392157, 4.50588235, 4.00784314,
       3.50980392, 3.01176471, 3.50980392, 4.00784314, 4.50588235,
       5.00392157, 5.50196078, 6.        , 5.50196078, 5.00392157,
       4.50588235, 4.00784314, 3.50980392, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.50980392, 4.00784314,
       4.50588235, 5.00392157, 5.50196078, 6.        , 5.50196078,
       5.00392157, 4.50588235, 4.00784314, 3.50980392, 3.01176471,
       3.50980392, 4.00784314, 4.50588235, 5.00392157, 5.50196078,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       5.50196078, 5.00392157, 4.50588235, 4.00784314, 3.50980392,
       3.01176471, 3.50980392, 4.00784314, 4.50588235, 5.00392157,
       5.50196078, 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       5.50196078, 5.00392157, 4.50588235, 4.00784314, 3.50980392,
       3.01176471, 3.01176471, 3.50980392, 4.00784314, 4.50588235,
       5.00392157, 5.50196078, 6.        , 5.50196078, 5.00392157,
       4.50588235, 4.00784314, 3.50980392, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.50980392, 4.00784314, 4.50588235,
       5.00392157, 5.50196078, 6.        , 6.        , 5.50196078,
       5.00392157, 4.50588235, 4.00784314, 3.50980392, 3.01176471,
       3.50980392, 4.00784314, 4.50588235, 5.00392157, 5.50196078,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 5.50196078,
       5.00392157, 4.50588235, 4.00784314, 3.50980392, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.50980392, 4.00784314,
       4.50588235, 5.00392157, 5.50196078, 6.        , 6.        ,
       5.50196078, 5.00392157, 4.50588235, 4.00784314, 3.50980392,
       3.01176471, 3.50980392, 4.00784314, 4.50588235, 5.00392157,
       5.50196078, 6.        , 6.        , 5.50196078, 5.00392157,
       4.50588235, 4.00784314, 3.50980392, 3.01176471, 3.50980392,
       4.00784314, 4.50588235, 5.00392157, 5.50196078, 6.        ,
       5.50196078, 5.00392157, 4.50588235, 4.00784314, 3.50980392,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.50980392, 4.00784314, 4.50588235, 5.00392157, 5.50196078,
       6.        , 5.50196078, 5.00392157, 4.50588235, 4.00784314,
       3.50980392, 3.01176471, 3.50980392, 4.00784314, 4.50588235,
       5.00392157, 5.50196078, 6.        , 6.        , 5.50196078,
       5.00392157, 4.50588235, 4.00784314, 3.50980392, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.01176471, 3.01176471,
       3.01176471, 3.01176471, 3.01176471, 3.50980392, 4.00784314,
       4.50588235, 5.00392157, 5.50196078, 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 6.        , 6.        , 6.        , 6.        ,
       6.        , 5.        , 4.        , 3.        , 2.        ,
       1.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        ])
>>> df['dot'] = np.convolve(df.x, dot)
>>> df['dot'] = [0] * (len(dot) / 2) + list(np.convolve(df.x, dot)) + [0] * (len(dot) / 2)
>>> df['dot'] = [0] * int(len(dot) / 2) + list(np.convolve(df.x, dot)) + [0] * int(len(dot) / 2)
>>> padlen = int(len(dot) / 2)
>>> padlen
9
>>> len(dot)
18
>>> df['dot'] = np.convolve(df.x, dot)[padlen:-padlen]
>>> df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df['x'] - 1
t
0.00    0.0
0.01    0.0
0.02    0.0
0.03    0.0
0.04    0.0
       ... 
2.95    0.0
2.96    0.0
2.97    0.0
2.98    0.0
2.99    0.0
Name: x, Length: 300, dtype: float64
>>> 4 * (df['x'] - .75)
t
0.00    1.0
0.01    1.0
0.02    1.0
0.03    1.0
0.04    1.0
       ... 
2.95    1.0
2.96    1.0
2.97    1.0
2.98    1.0
2.99    1.0
Name: x, Length: 300, dtype: float64
>>> df['x'] = 4 * (df['x'] - .75)
>>> df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> dot = [-1] * 6 + [1] * 6 + [-1] * 6
>>> dash = [-1] * 6 + [1] * 6 * 3 + [-1] * 6
>>> df['dot'] = np.convolve(df.x, dot)[padlen:-padlen+1]
>>> df['dash'] = np.convolve(df.x, dash)[padlen:-padlen+1]
>>> padlen
9
>>> dotpadlen = int(len(dot) / 2)
>>> dashpadlen = int(len(dash) / 2)
>>> df['dash'] = np.convolve(df.x, dash)[dashpadlen:-dashpadlen+1]
>>> df['dot'] = np.convolve(df.x, dot)[dotpadlen:-dotpadlen+1]
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> np.convolve?
>>> df['dot'] = np.convolve(df.x, dot, mode='same')
>>> df['dash'] = np.convolve(df.x, dash, mode='same')
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> dot = np.array([-1] * 6 + [1] * 6 + [-1] * 6)
>>> dot = dot / dot.abs().sum()
>>> dot = dot / np.abs(dot).sum()
>>> dot
array([-0.05555556, -0.05555556, -0.05555556, -0.05555556, -0.05555556,
       -0.05555556,  0.05555556,  0.05555556,  0.05555556,  0.05555556,
        0.05555556,  0.05555556, -0.05555556, -0.05555556, -0.05555556,
       -0.05555556, -0.05555556, -0.05555556])
>>> dash = np.array([-1] * 6 + [1] * 6 * 3 + [-1] * 6)
>>> dot = dash / np.abs(dash).sum()
>>> dot = np.array([-1] * 6 + [1] * 6 + [-1] * 6)
>>> dot = dot / np.abs(dot).sum()
>>> dash = dash np.abs(dash).sum()
>>> dash = dash / np.abs(dash).sum()
>>> dash
array([-0.03333333, -0.03333333, -0.03333333, -0.03333333, -0.03333333,
       -0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
        0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
        0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
        0.03333333,  0.03333333,  0.03333333,  0.03333333, -0.03333333,
       -0.03333333, -0.03333333, -0.03333333, -0.03333333, -0.03333333])
>>> df['dash'] = np.convolve(df.x, dash, mode='same')
>>> df['dot'] = np.convolve(df.x, dot, mode='same')
>>> df.plot()
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> df.plot(style=['_','.','-'])
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df.plot(style=['-','.','_'])
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> df.plot(style=['-','.','_'], linewidth=[.5, 2, 4])
>>> df['x'].plot(style='-', linewidth=.75, alpha=.5)
<AxesSubplot:xlabel='t'>
>>> df['dot'].plot(style='.', linewidth=2, alpha=.75)
<AxesSubplot:xlabel='t'>
>>> df['dash'].plot(style='_', linewidth=5, alpha=.75)
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df['x'].plot(linestyle='solid', linewidth=1, alpha=1)
<AxesSubplot:xlabel='t'>
>>> df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.4)
<AxesSubplot:xlabel='t'>
>>> df['dot'].plot(linestyle='dotted', linewidth=4, alpha=.35)
<AxesSubplot:xlabel='t'>
>>> plt.show()
>>> df['x'].plot(linestyle='solid', linewidth=2.5, alpha=1)
<AxesSubplot:xlabel='t'>
>>> df['dash'].plot(linestyle='dashed', linewidth=2.5, alpha=.4)
<AxesSubplot:xlabel='t'>
>>> df['dot'].plot(linestyle='dotted', linewidth=2.5, alpha=.35)
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
<AxesSubplot:xlabel='t'>
>>> df['dash'].plot(linestyle='dashed', linewidth=2.5, alpha=.75)
<AxesSubplot:xlabel='t'>
>>> df['dot'].plot(linestyle='dotted', linewidth=3, alpha=1)
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.show()
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
<AxesSubplot:xlabel='t'>
>>> df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
<AxesSubplot:xlabel='t'>
>>> df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
<AxesSubplot:xlabel='t'>
>>> plt.grid('on')
>>> plt.legend()
<matplotlib.legend.Legend at 0x7fd42a89df40>
>>> plt.show()
>>> hist -f code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.py
>>> hist -o -p -f code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.md
>>> import seaborn
>>> seaborn.set_theme()
>>> hist
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.legend()
... plt.show()
...
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> seaborn.set_theme('whitegrid')
>>> seaborn.set_theme('paper')
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> seaborn.set_theme('talk')
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> seaborn.set_theme('poster')
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> seaborn.set_theme('whitegrid')
>>> seaborn.set_theme('notebook')
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> seaborn.set_style('whitegrid')
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> fig = plt.figure(figsize=(700,300))
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> fig = plt.figure(figsize=(10,4))
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> fig = plt.figure(figsize=(10,7))
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> fig = plt.figure(figsize=(10,6))
>>> df['x'].plot(linestyle='solid', linewidth=2, alpha=.5)
... df['dash'].plot(linestyle='dashed', linewidth=2, alpha=.75)
... df['dot'].plot(linestyle='dotted', linewidth=2, alpha=1)
... plt.grid('on')
... plt.xlabel('Time (sec)')
... plt.ylabel('Signal amplitude (-1 to +1)')
... plt.legend()
... plt.show()
...
>>> hist
>>> df.to_csv('secret_message_convolved_line_plot.csv')
>>> ls
>>> cd ~/code/tangibleai/nlpia-manuscript/manuscript/images/
>>> df.to_csv('secret_message_convolved_line_plot.csv')
>>> df2 = pd.read_csv('secret_message_convolved_line_plot.csv', index_col=0)
>>> df
        x       dot      dash
t                            
0.00  1.0  0.054684  0.232810
0.01  1.0  0.220915  0.133333
0.02  1.0  0.387146  0.033856
0.03  1.0  0.553377 -0.065621
0.04  1.0  0.608497 -0.165098
...   ...       ...       ...
2.95  1.0 -0.111111  0.399477
2.96  1.0 -0.055556  0.299739
2.97  1.0  0.000000  0.200000
2.98  1.0 -0.055556  0.166667
2.99  1.0 -0.111111  0.133333

[300 rows x 3 columns]
>>> from matplotlib import pyplot as plt
>>> from urllib.request import urlretrieve
>>> f = urlretrieve(url, 'titanic-distress-signal-simulated.wav')
>>> hist
>>> PKG_DIR = Path('/home/hobs/code/tangibleai/nlpia2/src/nlpia2')
>>> from pathlib import Path
>>> PKG_DIR = Path('/home/hobs/code/tangibleai/nlpia2/src/nlpia2')
>>> PKG_NAME = PKG_DIR.name
... SRC_DIR = PKG_DIR.parent
... REPO_DIR = SRC_DIR.parent
... MANUSCRIPT_DIR = REPO_DIR.parent / 'nlpia-manuscript' / 'manuscript'
... IMAGES_DIR = MANUSCRIPT_DIR / 'images'
... ADOC_DIR = MANUSCRIPT_DIR / 'adoc'
...
>>> MANUSCRIPT_DIR.is_dir()
True
>>> IMAGES_DIR
PosixPath('/home/hobs/code/tangibleai/nlpia-manuscript/manuscript/images')
>>> IMAGES_DIR.is_dir()
True
>>> pwd
'/home/hobs/code/tangibleai/nlpia-manuscript/manuscript/images'
>>> ls -hal
>>> mv secret_message_convolved_line_plot.csv /home/hobs/.nlpia2-data/
>>> hist -o -p -f /home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch07/secret_message_convolved_line_plot.hist.md
