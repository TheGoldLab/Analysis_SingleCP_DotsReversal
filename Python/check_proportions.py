"""
Is it normal to see well-above-chance performance at 0%-coherence?

---------------------------------------------
         Excerpt of Shell session 
---------------------------------------------

(r-environment)$ python
Python 3.7.3 | packaged by conda-forge | (default, Jul  1 2019, 21:52:21)
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> import numpy as np
>>> data = pd.read_csv('Block2.csv')
>>> data.head()
  coh     cp    dir   vd
0   0  False   left  300
1   0  False  right  300
2   0  False  right  400
3   0  False   left  300
4   0  False  right  300
>>> data = data.iloc[:204]
>>> len(data)
204
>>> data = data[data['coh'] == '0']
>>> len(data)
81
>>> vds = [100,200,300,400]
>>> datas = [data[data['vd'] == v] for v in vds]
>>> [len(d) for d in datas]
[8, 10, 32, 31]
>>> tnum = [len(d) for d in datas]
>>> props_left = [len(d[d['dir'] == 'left']) / tnum[i] for i, d in enumerate(datas)]
>>> props_left
[0.25, 0.8, 0.53125, 0.6451612903225806]
>>> quit()

-----------------------------------------------
As can be seen above, a subject who answers 'left' all the time on 0%-coherence trials 
would be correct in Block2:
64.5% of the time on 400-msec trials
53.1% of the time on 300-msec trials
80% of the time on 200-msec trials
25% of the time on 100-msec trials
"""
