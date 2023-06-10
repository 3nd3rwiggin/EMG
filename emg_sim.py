import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit
from scipy.stats import poisson
from scipy.io import savemat

class EMGSimulator:
    def __init__(self, force):
        self.force_slope = force/10
        self.duration = 10
        self.sampling_rate = 2000
        self.time = np.arange(0, self.duration, 1/self.sampling_rate)
        self.force_profile = self.force_slope * self.time
        self.force_value = self.force_slope * self.duration
        self.force_thresholds = {1: [0,20], 2: [20,40], 3: [40,60]}
        self.max_firing_rates = {1: 3, 2: 6, 3: 8}
        self.muap_params = {
            1: [0.2, 0.2, 0.1, 0.15, 0.02],
            2: [0.6, 0.6, 0.08, 0.12, 0.03],
            3: [0.8, 0.8, 0.06, 0.09, 0.04]
        }

    @staticmethod
    def generate_biphasic_muap(t, muap_params, force_level):
        A1, A2, T1, T2, std = muap_params
        return force_level * (A1 * np.exp(-((t - T1)**2) / (2 * std**2)) - A2 * np.exp(-((t - T2)**2) / (2 * std**2)))

    def calculate_firing_rates(self):
        firing_rates = {}
        for motor_unit in self.force_thresholds.keys():
            firing_rates[motor_unit] = np.zeros_like(self.time)
            min_force, max_force = self.force_thresholds[motor_unit]
            for i, force in enumerate(self.force_profile):
                if force <= min_force:
                    firing_rates[motor_unit][i] = 0
                elif force > max_force:
                    firing_rates[motor_unit][i:] = self.max_firing_rates[motor_unit]
                    break
                else:
                    firing_rates[motor_unit][i] = self.max_firing_rates[motor_unit] * (2 * expit(10 * (force - min_force) / (max_force - min_force)) - 1)
        return firing_rates

    def generate_spike_trains(self, firing_rates):
        spike_trains = {}
        for motor_unit in firing_rates.keys():
            spike_trains[motor_unit] = np.zeros_like(self.time)
            for i, rate in enumerate(firing_rates[motor_unit]):
                spike_trains[motor_unit][i] = poisson.rvs(rate/self.sampling_rate)  # convert rate from Hz to spikes per sample
        return spike_trains

    def generate_emg(self, spike_trains):
        # Generate MUAP templates
        muap_templates = {}
        for motor_unit, params in self.muap_params.items():
            muap_templates[motor_unit] = self.generate_biphasic_muap(self.time, params, force_level=1)

        # Generate motor unit action potentials
        muaps = {}
        for motor_unit, spike_train in spike_trains.items():
            muap = np.zeros_like(self.time)
            for i, spike in enumerate(spike_train):
                if spike:
                    start = i
                    end = start + len(muap_templates[motor_unit])
                    if end > len(muap):
                        end = len(muap)
                        muap[start:end] += muap_templates[motor_unit][:end-start]
                    else:
                        muap[start:end] += muap_templates[motor_unit]
            muaps[motor_unit] = muap

        # Initialize EMG signal as zero
        emg = np.zeros_like(self.time)

        # Add each MUAP to the EMG signal
        for muap in muaps.values():
            emg += muap

        return emg, muaps

    def export_to_mat(self, emg):
        data_to_export = {'emg': emg, 'time': self.time}
        savemat("emg.mat", data_to_export)

    def plot_all(self, firing_rates, spike_trains, emg, muaps):
        fig, axs = plt.subplots(5, 1, figsize=(10, 25))
        fig.subplots_adjust(hspace=0.5)

        # Plot force profile
        axs[0].plot(self.time, self.force_profile, label=f"Force {self.force_value}")
        axs[0].set(xlabel="Time (s)", ylabel="Force (N)")
        axs[0].legend()
        axs[0].set_title("Force Profile")
        axs[0].grid(True)

        # Plot firing rates
        for motor_unit, firing_rate in firing_rates.items():
            axs[1].plot(self.time, firing_rate, label=f"Motor Unit {motor_unit}")
        axs[1].set(xlabel="Time (s)", ylabel="Firing Rate (Hz)")
        axs[1].legend()
        axs[1].set_title("Firing Rate")
        axs[1].grid(True)

        # Plot spike trains
        for motor_unit, spike_train in spike_trains.items():
            axs[2].eventplot(np.where(spike_train)[0] / self.sampling_rate, lineoffsets=motor_unit, label=f"Motor Unit {motor_unit}")
        axs[2].set(xlabel="Time (s)", ylabel="Motor Unit")
        axs[2].set_yticks(list(spike_trains.keys()))
        axs[2].legend()
        axs[2].set_title("Spike Train")
        axs[2].grid(True)

        # Plot motor unit action potentials
        for motor_unit, muap in muaps.items():
            axs[3].plot(self.time, muap, label=f"Motor Unit {motor_unit}")
        axs[3].set(xlabel="Time (s)", ylabel="Potential")
        axs[3].legend()
        axs[3].set_title("Motor Unit Action Potential")
        axs[3].grid(True)

        # Plot EMG signal
        axs[4].plot(self.time, emg, label="EMG Signal")
        axs[4].set(xlabel="Time (s)", ylabel="EMG Signal")
        axs[4].set_title("EMG Signal")
        axs[4].grid(True)

        plt.show()

    def run_simulation(self):
        firing_rates = self.calculate_firing_rates()
        spike_trains = self.generate_spike_trains(firing_rates)
        emg, muaps = self.generate_emg(spike_trains)
        self.export_to_mat(emg)
        self.plot_all(firing_rates, spike_trains, emg, muaps)


if __name__ == "__main__":
    simulator = EMGSimulator(force=55)
    simulator.run_simulation()

