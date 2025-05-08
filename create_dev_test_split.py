import csv
import os

"""
Splits exemplars in data/full_set.csv into a dev_set and test_set of equal
sizes and writes them to data/dev_set.tsv and data/test_set.csv.
"""

os.chdir('C:\\Users\\Julie\\Documents\\OneDrive\\Documents\\python for final')

with open('dataset.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    all_ips = list(reader)
legit_ips = [d for d in all_ips if d[7] == 'x']
all_ips_sorted = sorted(all_ips[1:], key = lambda k : (k[6],k[2],k[4],k[3]))
dev = open('data/dev_set.tsv', 'w')
test = open('data/test_set.tsv', 'w')
dev.write('%s\n' % '\t'.join(all_ips[0]))
test.write('%s\n' % '\t'.join(all_ips[0]))
problem_line = ""

for ai,a in enumerate(all_ips_sorted):
    try:
        if ai % 2 == 0:
            problem_line = '%s\n' % '\t'.join(a)
            dev.write('%s\n' % '\t'.join(a))
        else:
            problem_line = '%s\n' % '\t'.join(a)
            test.write('%s\n' % '\t'.join(a))
    except UnicodeEncodeError:
        print(problem_line)
        pass
dev.close()
test.close()
