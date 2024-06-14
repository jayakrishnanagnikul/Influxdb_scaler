import numpy as np
import matplotlib.pyplot as plt
import time

# Define parameters
amplitude = 1      # Amplitude of the sine wave
frequency = 1      # Frequency in Hz
phase = 0          # Phase in radians
sampling_rate = 1000  # Sampling rate in samples per second
duration = 2       # Duration in seconds


def sine_with_time():
# Initialize a list to store the sine wave data
    sine_wave_data = []

    # Get the start time
    start_time = time.time()

    # Run the loop for the specified duration
    while time.time() - start_time < duration:
        # Get the current time
        current_time = time.time()

        # Calculate the sine wave value
        sine_value = amplitude * np.sin(2 * np.pi * frequency * current_time + phase)

        # Store the time and sine value in the list
        sine_wave_data.append((current_time, sine_value))

        # Sleep for the appropriate amount of time to maintain the sampling rate
        time.sleep(1.0 / sampling_rate)

    # Convert the data to a numpy array for further processing or analysis
    sine_wave_data = np.array(sine_wave_data)

    # Print the generated data
    # print(sine_wave_data)
    
    time_values = sine_wave_data[:, 0]
    sine_values = sine_wave_data[:, 1]
    print(time_values)


    plt.figure(figsize=(10, 4))
    plt.plot(time_values, sine_values)
    plt.title('Sine Wave with time')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()


sine_with_time()
exit()


# Generate time values
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate sine wave values
y = amplitude * np.sin(2 * np.pi * frequency * t + phase)
# Plot the sine wave
plt.figure(figsize=(10, 4))
plt.plot(t, y)
plt.title('Sine Wave')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
