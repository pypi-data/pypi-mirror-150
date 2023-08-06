import freqle as fr
from freqle import cluster as cl
import matplotlib.pyplot as plt
import numpy as np
from scipy import special

nbhs = 10000
palomar = cl(cluster_eta=1e9, Nbh = nbhs, n_mus = 300, mu_min=1e-13, mu_max=1.3e-12)
palomar.populate(v = True)
palomar.build_mass_grid()
palomar.emit_GW(v = True)
palomar.calc_freq_distr(v = True, remove_outliers = False, norm_distr=False)
freqs = palomar.get_freqs()
freqs_peaks = palomar.saved_top_bins

#palomar.plot_freq_distr(.4e-12)

print("Cluster setted")
print("Calculating occupancy")

amp = 70 # In Hz

tfft_min = 60
tfft_max = 2500
steps = 10
tffts = np.linspace( tfft_min, tfft_max, steps)
deltas = 1 / tffts

max_occup = []
temp = []

run = 0
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
    print(f"{run / steps * 100: .2f}%")
    max_occup.append(temp)
    temp = []


'''fig = plt.figure(figsize=(12, 9))

for i, tfft in enumerate(tffts):
    plt.plot(palomar.boson_grid, max_occup[i], label = f'tfft duration: {tfft:.0f} s' )


plt.hlines([1e1, 1e2, 1e3], xmin = palomar.boson_grid.min(), xmax = palomar.boson_grid.max())

plt.yscale('log')
plt.title(f"Occupancy of most common bin for {nbhs} emitting BHs")
plt.xlabel("Boson Mass")
plt.legend()
#plt.savefig(f"script_plots\Occupancy-min{tfft_min}secs")
plt.show()'''


print("Calculating lambda min")

theta = 2.5
Gamma = .95
CR = 4
obs_time = 60 * 60 * 24 * 365

N = np.ceil(obs_time / tffts)

p1 = np.exp(-theta) - 2 * np.exp(-2*theta) + np.exp(-3 * theta)
p0 = np.exp(-theta) - np.exp(-2*theta) + 1/3 * np.exp(-3 * theta)

lambda_min = 2 / theta * np.sqrt(p0 * (1- p0) / (N * p1 * p1)) * (CR - np.sqrt(2) * special.erfcinv(2 * Gamma))
s_lam_min = []

for k, _ in enumerate(lambda_min):
    s_lam_min.append( np.array(max_occup[k]) * _)

'''fig = plt.figure(figsize=(12, 9))

for i, tfft in enumerate(tffts):
    plt.plot(palomar.boson_grid, s_lam_min[i], label = f'tfft duration: {tfft:.0f} s' )

plt.yscale('log')
plt.title("$\lambda_{min}$" f" of most common bin for {nbhs} emitting BHs")
plt.xlabel("Boson Mass")
plt.hlines([1e1, 1e2, 1e3], xmin = palomar.boson_grid.min(), xmax = palomar.boson_grid.max())
#plt.grid()
plt.legend()
#plt.savefig(f"script_plots\lambda-min{tfft_min}secs - {steps} iterations")
plt.show()'''

print("Calculating standard fft bins")

std_max_occup = []
std_lambda_min = []
for _, freq in enumerate(freqs):
    min = freqs_peaks[_] - amp/2
    max = freqs_peaks[_] + amp/2

    f = freqs_peaks[_]
    if f > 500:
        f0 = np.ceil(freqs_peaks[_]/10) * 10 # Get closest multiple of 10
        tfft = 7.159133e+04/np.sqrt(f0)
    else:
        tfft = 1.01159145e+03*np.exp(-1.60025453e-02*(f-8.08627007e+01))+6.31273230
    delta = 1/tfft
    #print(tfft)
    N = np.ceil(obs_time / tfft)

    mask = (freq > min) & (freq < max)
    sel_freqs = freq[mask]

    edges = np.arange(min, max, delta)
    counts, bins = np.histogram(sel_freqs, edges)

    max_count = counts.max()

    std_lam_tmp = 2 / theta * np.sqrt(p0 * (1- p0) / (N * p1 * p1)) * (CR - np.sqrt(2) * special.erfcinv(2 * Gamma))

    std_max_occup.append(max_count)
    std_lambda_min.append(std_lam_tmp * max_count)


fig, ax = plt.subplots(figsize=(12, 9))

#ax.plot(palomar.boson_grid, std_lambda_min,  label = f'standard tfft duration', c = 'black' )
for i, tfft in enumerate(tffts):
    ax.plot(palomar.boson_grid, s_lam_min[i], label = f'tfft duration: {tfft:.0f} s' )

ax.set_xlim((palomar.boson_grid.min(), palomar.boson_grid.max()))


ax2 = ax.twiny()
ax2.set_xlabel("Frequency [Hz]")
ax2.plot(palomar.saved_top_bins, std_lambda_min, label = f'standard tfft duration', c = 'black' )
ax2.set_xlim((palomar.saved_top_bins.min(), palomar.saved_top_bins.max()))

ax.set_title("$\lambda_{min}$" f" of most common bin for {nbhs} emitting BHs")
ax.set_xlabel("Boson Mass")

plt.hlines([1e1, 1e2, 1e3], xmin = palomar.boson_grid.min(), xmax = palomar.boson_grid.max())
#plt.grid()
plt.yscale('log')
plt.legend()
plt.savefig(f"script_plots\Plot of optimal tfft duration in function of bin frequency")
plt.show()
