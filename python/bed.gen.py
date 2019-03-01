import numpy as np
import pandas as pd

#df = pd.DataFrame(np.random.normal(1,0.1,(1000, 5)), columns=['a', 'b', 'c', 'd', 'e'])
df = pd.DataFrame()
n = int(50818468/100)
df['Chr'] = [22 for i in range(n)]
df['Start'] = [ 100 * i + 1 for i in range(n)]
df['End'] = [ 100 * (i + 1) + 1 for i in range(n)]
#df = df[['Chr','Start','End','a', 'b', 'c', 'd', 'e']]
#df.to_csv('/home/wxq/ftp/files/cnview.test.bed', index=False, sep='\t')
df.to_csv('/home/wxq/ftp/files/chr22.bin100.bed', index=False, sep='\t')
