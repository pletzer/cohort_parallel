import re
import sys
import pandas as pd
import os
import glob
import datetime
import matplotlib.pylab as plt
import seaborn as sn

plt.xticks(rotation=45)

case = 'cylc-cohort'

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
      speedup_ideal = float(m.group(2))
  elapsed_times.append(elapsed_time)
  speedups.append(speedup)
  speedup_ideals.append(speedup_ideal)

df = pd.DataFrame({'elapsed_time': elapsed_times, 
                   'speedup': speedups,
                   'speedup_ideal': speedup_ideals})
df.to_csv(f'{case}.csv')

print(df)
sn.lineplot(data=df, x='speedup_ideal', y='speedup', errorbar='sd')
plt.xlim([1, df.speedup_ideal.max()])
plt.ylim([0, df.speedup_ideal.max()])
plt.xlabel('na (= num workers)')
plt.title(f'cohort_parallel')
plt.savefig(f'{case}.png', bbox_inches="tight")


