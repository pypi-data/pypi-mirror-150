from cProfile import label
from freqle import cluster
import freqle as fr
import matplotlib.pyplot as plt
import numpy as np
import sys

Nbh = int(sys.argv[1])
cluster_eta = float(sys.argv[2])
Tfft = float(sys.argv[3])
binsize = 1/Tfft
mu = float(sys.argv[4])

pal = cluster(Nbh = Nbh, n_mus = 300, cluster_eta = cluster_eta     )
pal.populate(v = True)
pal.build_mass_grid()
pal.emit_GW(v = True, maximum_det_freq = 2048)
pal.calc_freq_distr(remove_outliers = False, v = True, nbins = 64, norm_distr=False)


mu_index = np.argmin(np.abs(mu - pal.boson_grid))
freq = pal.get_freqs()[mu_index]
mu = pal.boson_grid[mu_index]


bins, counts, bin_size = fr.hist_by_row(freq, binsize=binsize, normalize=False)

cond = counts[0] > 10
bins = bins [0, :-1]
counts = counts [0]
bin_size = bin_size[0]

cond = counts > 10
sm = np.sum(counts[cond])

peakidx = np.argmin(counts.max())
plt.plot(bins[cond], counts[cond], label = f"Bhs at peak = {counts.max()/Nbh * 100:.2f} % ({int(counts.max())} BHs)\nTfft: {int(Tfft)} $s$\nPeak freq: {bins[peakidx] + binsize/2:.2f} $Hz$\nSomm 1s: {sm}")
plt.yscale('log')
plt.xscale('log')
plt.title(f"Distribuzione delle frequenze per {int(Nbh)} Buchi Neri\n Massa del bosone: {mu * 1e12:.2f} $10^{-12}eV$")
plt.xlabel("Frequenza misurata $[Hz]$")

plt.legend()
plt.axhline(y = 1)
plt.show()