import re
import sys
import pandas as pd
import os
import glob
import datetime
import matplotlib.pylab as plt
import seaborn as sn

#plt.xticks(rotation=45)

case = 'cohort151'

#rundir = os.environ['CYLC_WORKFLOW_RUN_DIR']
rundir = f'/home/pletzera/cylc-run/{case}'
out_files = glob.glob(rundir + '/runN/log/job/1/run*_m*/NN/job.out')

elapsed_times = []
speedups = []
speedup_ideals = []
for fname in out_files:
  print(fname)
  elapsed_time = float('inf')
  speedup = float('inf')
  speedup_ideal = float('inf')
  for line in open(fname).readlines():
    m = re.search(r'Elapsed time\:\s*(\d*\.\d+)', line)
    if m:
      elapsed_time = float(m.group(1))
    m = re.search(r'Speedup: (\d*\.\d+)x [^\d]*(\d+)', line)
    if m:
      speedup = float(m.group(1))
      speedup_ideal = int(m.group(2))
  elapsed_times.append(elapsed_time)
  speedups.append(speedup)
  speedup_ideals.append(speedup_ideal)

df = pd.DataFrame({'elapsed_time': elapsed_times, 
                   'speedup': speedups,
                   'num_workers': speedup_ideals})
df['parallel_eff'] = df['speedup'] / df['num_workers']
df.to_csv(f'{case}.csv')

print(df)

x = df.num_workers.unique()
x.sort()
print(x)
print(df[df.num_workers == 10])
print(df[df.num_workers == 10].speedup)
print(df[df.num_workers == 10].speedup.mean())
y = [df[df.num_workers == n].speedup.mean() for n in x]
print(y)
e = [df[df.num_workers == n].speedup.std() for n in x]

plt.errorbar(x, y, yerr=e, marker='o', mfc='r', mec='k') 
plt.plot(x, x, 'k--')

plt.ylabel('speedup')
plt.xlabel('num workers')
plt.title(f'na= 151 nt = 302')
plt.savefig(f'{case}.png', bbox_inches="tight")


