import cProfile
from threshold_elgamal import run_tc_scheme
from pstats import Stats, SortKey

cProfile.run('run_tc_scheme(3, 5, 10)', filename='stats.txt')
p = Stats('stats.txt')
p.strip_dirs().sort_stats(SortKey.CALLS).print_stats()
