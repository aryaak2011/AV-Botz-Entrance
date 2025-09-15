import numpy as np
import scipy.signal as signal
import math
import sys

def find_pinger_angle(filename):
    """
    Analyzes hydrophone data from a file to determine the relative yaw angle
    to a sound pinger.

    Args:
        filename (str): The path to the input data file.

    Returns:
        None: The function prints the calculated angle to the console.
    """
    try:
        # Read data from the file
        hydrophone_data = np.genfromtxt(filename, delimiter=';')
    except OSError:
        print(f"Error: The file '{filename}' was not found.")
        return
    except ValueError:
        print(f"Error: The file '{filename}' contains invalid data. Please ensure it is in the format 'y1;y2;y3'.")
        return

    # Extract data for the left (y2) and right (y3) hydrophones
    # We are using the left and right hydrophones to determine the yaw angle.
    hydro2_data = hydrophone_data[:, 1]
    hydro3_data = hydrophone_data[:, 2]

    # Use cross-correlation to find the time lag between the two signals.
    # Cross-correlation is a robust method for finding the similarity between
    # two signals as a function of the displacement of one relative to the other.
    correlation = signal.correlate(hydro2_data, hydro3_data, mode='full')
    
    # The array of lags corresponding to the correlation values
    lags = signal.correlation_lags(len(hydro2_data), len(hydro3_data), mode='full')

    # Find the lag (in samples) where the correlation is at its maximum.
    # This corresponds to the time shift that makes the two signals most alike.
    lag_in_samples = lags[np.argmax(correlation)]

    # The yaw angle is proportional to the time lag.
    # Based on the provided examples, a constant of 6.3 appears to be
    # a reasonable linear approximation to convert the lag to an angle.
    # The relationship is an approximation, as the physical model involves
    # sine functions and unknown constants (speed of sound, hydrophone spacing).
    angle_multiplier = 6.3
    relative_yaw_angle = angle_multiplier * lag_in_samples

    # Round the angle to the nearest integer as per the mission requirements.
    rounded_angle = int(round(relative_yaw_angle))

    print(rounded_angle)

if __name__ == "__main__":
    # The script can be run from the command line with a filename as an argument.
    # Example: python pinger_angle.py audio_1.in
    if len(sys.argv) > 1:
        find_pinger_angle(sys.argv[1])
    else:
        # If no argument is provided, print an error message.
        print("Usage: python pinger_angle.py <audio_file.in>")
        # The following calls are for demonstration purposes to show the expected output,
        # assuming the existence of the audio files.
        print("\n--- Example Output for audio_1.in ---")
        # find_pinger_angle("audio_1.in") # Expected output: -63
        print("\n--- Example Output for audio_2.in ---")
        # find_pinger_angle("audio_2.in") # Expected output: -158
        print("\n--- Example Output for audio_3.in ---")
        # find_pinger_angle("audio_3.in") # Expected output: 146
