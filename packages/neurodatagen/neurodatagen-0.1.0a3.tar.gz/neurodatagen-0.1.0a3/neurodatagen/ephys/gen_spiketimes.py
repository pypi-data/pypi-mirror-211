import numpy as np
import pandas as pd


def sim_spikes(num_neurons: int, firing_rate: float, duration: float) -> pd.DataFrame:
    """
    Simulates spike times for a given number of neurons, firing rate, and duration.

    Parameters
    ----------
    num_neurons (int):
        Number of neurons to simulate.
    firing_rate (float):
        Firing rate of each neuron in Hz.
    duration (float):
        Duration of the spike trains in seconds.

    Returns
    -------
    pandas DataFrame:
        Spiking data
    """

    # Calculate the expected number of spikes for each neuron
    expected_num_spikes = np.random.poisson(firing_rate * duration, size=num_neurons)

    # Generate spike times for all neurons at once using a uniform distribution
    spike_times = np.random.uniform(0, duration, size=sum(expected_num_spikes))

    # Assign spike times to each neuron based on their expected number of spikes
    neuron_ids = np.repeat(np.arange(1, num_neurons + 1), expected_num_spikes)

    # Create a DataFrame of time and neuron cols, sorted by spike times
    spikes_df = pd.DataFrame(
        {"time": spike_times, "neuron": pd.Categorical(neuron_ids)}
    )
    spikes_df.sort_values("time", inplace=True, ignore_index=True)

    return spikes_df


def assign_groups(times: np.ndarray, num_groups: int, sigma: float = 1) -> np.ndarray:
    """
    Bin an array of times into a number of groups controlled by num_groups parameter.

    Parameters
    ----------
    times (numpy.ndarray):
        An array of times to be binned into groups.
    num_groups (int):
        The number of groups to bin the times into.
    sigma (float, optional):
        The standard deviation of the normal distribution used to assign times to groups
        probabilistically. Default is 1.

    Returns
    -------
    numpy.ndarray:
        An equally sized array of groups labeled with integers.
    """
    # Sort the array of times
    sorted_times = np.sort(times)

    # Calculate the bin width based on the number of groups
    bin_width = (sorted_times[-1] - sorted_times[0]) / num_groups

    # Calculate the center of each bin
    bin_centers = np.linspace(
        sorted_times[0] + bin_width / 2, sorted_times[-1] - bin_width / 2, num_groups
    )

    # Assign each time to a group probabilistically
    groups = np.zeros_like(sorted_times)
    for i, time in enumerate(sorted_times):
        # Calculate the distance to each bin center
        distances = np.abs(time - bin_centers)

        # Calculate the probability of assigning the time to each group
        probabilities = np.exp(-(distances**2) / (2 * sigma**2))

        # Normalize the probabilities so they sum to 1
        probabilities /= np.sum(probabilities)

        # Assign the time to a group based on the probabilities
        groups[i] = np.random.choice(range(num_groups), p=probabilities)

    # Sort the groups based on the original order of the times
    return groups[np.argsort(times)]
