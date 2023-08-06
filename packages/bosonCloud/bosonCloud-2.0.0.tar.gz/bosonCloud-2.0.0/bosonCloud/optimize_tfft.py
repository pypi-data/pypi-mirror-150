from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
import freqle as fr
from freqle import cluster as cl
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from time import time


from scipy.optimize import curve_fit

def func(x, a, b, c, d):
    return a*np.exp(-c*(x-b))+d

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

nbhs = 10000
palomar = cl(cluster_eta=1e9, Nbh = nbhs, n_mus = 300, mu_min=1e-13, mu_max=1.3e-12)
palomar.populate(v = True)
palomar.build_mass_grid()
palomar.emit_GW(v = True)
palomar.calc_freq_distr(v = True, remove_outliers = False, norm_distr=False)
freqs = palomar.get_freqs()
freqs_peaks = palomar.saved_top_bins

print("Setting constants")
amp = 70 # In Hz
tfft_min = 5
tfft_max = 2500
steps = 100
tffts = np.geomspace(tfft_min, tfft_max, steps)
deltas = 1 / tffts

theta = 2.5
Gamma = .95
CR = 4
obs_time = 60 * 60 * 24 * 365

N = np.ceil(obs_time / tffts)

p1 = np.exp(-theta) - 2 * np.exp(-2*theta) + np.exp(-3 * theta)
p0 = np.exp(-theta) - np.exp(-2*theta) + 1/3 * np.exp(-3 * theta)

lambda_min = 2 / theta * np.sqrt(p0 * (1- p0) / (N * p1 * p1)) * (CR - np.sqrt(2) * special.erfcinv(2 * Gamma))

max_occup = []
temp = []

run = 0
print("Rebinning...")
start = time()
for delta in deltas:
    for _, freq in enumerate(freqs):
        min = freqs_peaks[_] - amp/2
        max = freqs_peaks[_] + amp/2

        mask = (freq > min) & (freq < max)
        sel_freqs = freq[mask]

        edges = np.arange(min, max, delta)
        counts, bins = np.histogram(sel_freqs, edges)

        temp.append(counts.max())
    run += 1
    print(f"Done: {run / steps * 100: .2f}%")
    temp = moving_average(temp, 6)
    max_occup.append(temp)
    temp = []
print(f"Done in {time() - start:.2f} s")
s_lam_min = []
print("Calculating lambda...")
for k, _ in enumerate(lambda_min):
    s_lam_min.append( np.array(max_occup[k]) * _)
s_lam_min = np.array(s_lam_min)


fig, ax = plt.subplots(figsize=(12, 9))

for i, tfft in enumerate(tffts):
    ax.plot(palomar.boson_grid, s_lam_min[i], label = f'tfft duration: {tfft:.0f} s' )
ax.set_title("$\lambda_{min}$" f" of most common bin for {nbhs} emitting BHs")
ax.set_xlabel("Boson Mass")
ax.set_xlim((palomar.boson_grid.min(), palomar.boson_grid.max()))


ax2 = ax.twiny()
ax2.set_xlabel("Frequency [Hz]")
ax2.plot(palomar.saved_top_bins, s_lam_min[0], label = f'standard tfft duration')
ax2.set_xlim((palomar.saved_top_bins.min(), palomar.saved_top_bins.max()))

plt.yscale('log')
plt.hlines([1e1, 1e2, 1e3], xmin = palomar.boson_grid.min(), xmax = palomar.boson_grid.max())
plt.legend()
#plt.savefig(f"script_plots\lambda-min{tfft_min}secs - {steps} iterations")
plt.show()

print("Finding best Fft duration...")

best_lambda_idx = np.argmax(s_lam_min, axis = 0)
best_lambda = s_lam_min.max(axis = 0)

fig, ax = plt.subplots(figsize=(12, 9))

for i, tfft in enumerate(tffts):
    ax.plot(palomar.boson_grid, s_lam_min[i], label = f'tfft duration: {tfft:.0f} s' )
ax.set_title("$\lambda_{min}$" f" of most common bin for {nbhs} emitting BHs")
ax.set_xlabel("Boson Mass")
ax.set_xlim((palomar.boson_grid.min(), palomar.boson_grid.max()))


ax2 = ax.twiny()
ax2.set_xlabel("Frequency [Hz]")
ax2.plot(palomar.saved_top_bins, best_lambda, label = f'standard tfft duration', c = 'black')
ax2.set_xlim((palomar.saved_top_bins.min(), palomar.saved_top_bins.max()))

plt.yscale('log')
plt.hlines([1e1, 1e2, 1e3], xmin = palomar.boson_grid.min(), xmax = palomar.boson_grid.max())
plt.legend()
#plt.savefig(f"script_plots\lambda-min{tfft_min}secs - {steps} iterations")
plt.show()

best_tffts = []
for idx in best_lambda_idx:
    best_tffts.append(tffts[idx])

popt, pcov = curve_fit(func, freqs_peaks, best_tffts, [328, 120, 0.013, 5])
print(popt)

plt.title("$\lambda_{min}$ vs peak frequency")
plt.plot(freqs_peaks, best_tffts)
plt.plot(freqs_peaks,func(freqs_peaks,*popt))
plt.ylabel("$\lambda_{min}$")
plt.xlabel("Frequency $[Hz]$")
plt.yscale('log')
#plt.xlim((0, 400))
plt.savefig(f"script_plots\lambda_min - vs - frequency bin {steps} points")
plt.show()