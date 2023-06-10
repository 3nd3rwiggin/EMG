## EMG Signal Simulator

This program simulates the generation of Electromyography (EMG) signals based on a given muscle force. The EMG signal is the electrical signal produced by muscle cells when they are neurologically activated. The simulation follows a process that mimics the physiological process of muscle activation.


### Prerequisites

The simulator requires Python 3 and the following Python libraries:

<ul>
    <li>NumPy</li>
    <li>Matplotlib</li>
    <li>SciPy</li>
</ul>

These libraries are necessary for the following reasons:


<ul>
    <li><strong> NumPy </strong> is used for numerical computations and array manipulations.</li>
    <li> <strong>Matplotlib </strong> is used for creating plots to visualize the simulation results.</li>
    <li> <strong> SciPy </strong> is used for various scientific computations, including generation of random numbers following specific distributions (e.g., Poisson distribution), and for saving the results in a MATLAB-compatible <strong><code>.mat</code></strong> file.</li>
</ul>

If the required libraries are not installed, you can install them using pip:


```
  pip install numpy matplotlib scipy
```


### Usage 

To use the simulator, instantiate the <strong><code>EMGSimulator</code></strong> class with a desired force level (in Newton), then call the <strong><code>run_simulation</code></strong> method. Here is an example:

```python
 simulator = EMGSimulator(force=55)
 simulator.run_simulation()
```

This command initiates the simulation with a force of 55 Newton, generates the EMG signal, exports the signal to a <strong><code>.mat</code></strong> file, and plots the force profile, firing rates, spike trains, MUAPs, and the EMG signal.


### Functions and Explanation

The <strong><code>EMGSimulator</code></strong> class has several methods that correspond to different stages of the simulation:


<ul>
    <li><strong><code>__init__(self, force)</code></strong>: This is the constructor of the simulator class. This method initializes the simulator with the desired force, along with other related parameters like the force slope, duration, sampling rate, force thresholds for different motor units, maximum firing rates, and the parameters for generating Motor Unit Action Potentials (MUAPs).
	<ul>
	<li><strong><code>force_slope</code></strong>: The force slope is simply the rate at which the force applied by the muscle changes. It's calculated by dividing the total force by the duration.</li>
	<li><strong><code>force_thresholds</code></strong>: Different motor units are activated at different force levels. These thresholds are set based on the motor unit number. Smaller motor units are recruited first and larger motor units are recruited as more force is required.</li>
	<li><strong><code>max_firing_rates</code></strong>: The maximum rate at which each motor unit can fire. Smaller motor units have a slower firing rate, while larger motor units have a faster firing rate.</li>
	</ul></li>
    <li><strong><code>generate_biphasic_muap(t, muap_params, force_level)</code></strong>:  Generates a biphasic (two-phase) Motor Unit Action Potential (MUAP) template. The shape of MUAPs is typically modeled as a Gaussian function due to their similarity to the natural shape of MUAPs. This function generates the MUAP template based on the given parameters and force level.</li>
    <li><strong><code>calculate_firing_rates(self)</code></strong>:  Generates a biphasic (two-phase) Motor Unit Action Potential (MUAP) template. The shape of MUAPs is typically modeled as a Gaussian function due to their similarity to the natural shape of MUAPs. This function generates the MUAP template based on the given parameters and force level.</li>
    <li><strong><code>generate_spike_trains(self, firing_rates)</code></strong>: Generates spike trains for each motor unit based on their firing rates. A spike train is a series of action potentials from a single neuron. Spike generation can be modeled as a Poisson process, especially when the firing rate is relatively low. This function uses the Poisson distribution to generate the spike trains.</li>
    <li><strong><code>generate_emg(self, spike_trains)</code></strong>: Generates the final EMG signal by summing all the individual MUAPs that are activated due to the firing of action potentials in the motor units.</li>
    <li><strong><code>export_to_mat(self, emg)</code></strong>: Exports the generated EMG signal and the time vector into a MATLAB compatible <strong><code>.mat</code></strong> file.</li>
  <li><strong><code>plot_all(self, firing_rates, spike_trains, emg, muaps)</code></strong>: Generates several plots to help visualize the process of generating an EMG signal. The plots include the force profile, firing rates, spike trains, individual MUAPs, and the final EMG signal.</li>
    <li><strong><code>run_simulation(self)</code></strong>: Runs the entire simulation process by calling the above methods in the correct sequence. </li>
</ul>

### Physiology of Muscle Contraction

<ol>
<li><strong> Motor Unit Recruitment </strong>: When a muscle contracts, not all motor units are activated at the same time. Smaller motor units, which control fewer muscle fibers and generate less force, are recruited first. As more force is required, larger motor units are recruited. This pattern of motor unit recruitment is known as the size principle and is modeled in the simulator by defining different force thresholds for different motor units.</li>
<li><strong>Rate Coding </strong>: As the force produced by a muscle increases, the firing rate of its motor units also increases. This process, known as rate coding, is a key mechanism by which the nervous system controls the force of muscle contractions.</li>
</ol>
Through these processes, the EMGSimulator class models the generation of an EMG signal due to the contraction of a muscle under a certain level of force.

### Output

The simulator produces:

<ul>
    <li>A <strong><code>.mat</code></strong> file named <strong><code>emg.mat</code></strong> containing the generated EMG signal and the corresponding time vector.</li>
  <li>Plots of the <strong>force profile</strong>, <strong>firing rates</strong>, <strong>spike trains</strong>, <strong>MUAPs</strong>, and the generated <strong>EMG signal</strong>.</li>
</ul>

![Alt text](https://i.ibb.co/H7HhnNY/download.png)

### Customization

The simulator can be customized by modifying parameters such as force



