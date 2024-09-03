from random import choice

import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# System parameters
K = 1.0   # System gain
T = 1.0   # Time constant

# Transfer function of the system H(s) = K / (s(Ts + 1))
numerator = [K]
denominator = [T, 1]
system = ctl.TransferFunction(numerator, denominator)

# PID controller parameters
Kp = 2.0  # Proportional gain   2
Ki = 1.0  # Integral gain      1
Kd = 0.5  # Derivative gain    0.5

# Transfer function of PID controller C(s) = Kp + Ki/s + Kd*s
pid_controller = ctl.TransferFunction([Kd, Kp, Ki], [1, 0])

# Open-loop transfer function
open_loop_system = pid_controller * system

# Closed-loop transfer function (feedback system)
closed_loop_system = ctl.feedback(open_loop_system)

# Time range for simulation
time = np.linspace(0, 10, 1000)

# Compute step response
time, response = ctl.step_response(closed_loop_system, time)

# User input for selecting which graph to display
print("Which simulation graph would you like to see?")
print("1. Step Response")
print("2. Step Response with Rise Time Indicators")
print("3. Step Response with Overshoot Calculation")
print("4. Step Response with Settling Time Calculation")
choice = input("Enter the number corresponding to your choice: ")

# Plot the step response


# Calculate rise time
final_value = response[-1]  # Final value of the step response
t_10 = time[np.where(response >= 0.1 * final_value)[0][0]]  # Time at 10% of the final value
t_90 = time[np.where(response >= 0.9 * final_value)[0][0]]  # Time at 90% of the final value
rise_time = t_90 - t_10

# Print rise time
#print(f"Rise Time: {rise_time:.4f} seconds")

# Plot the step response

# Calculate overshoot
final_value = response[-1]  # Final value of the step response
peak_value = np.max(response)  # Maximum value of the response (peak value)
overshoot = (peak_value - final_value) / final_value * 100  # Overshoot in percentage

# Print overshoot
#print(f"Overshoot: {overshoot:.2f}%")

# Calculate settling time
final_value = response[-1]  # Final value of the step response
tolerance = 0.02 * final_value  # 2% tolerance band

# Find the last time the response is outside the tolerance band
outside_tolerance = np.where(np.abs(response - final_value) > tolerance)[0]

if len(outside_tolerance) > 0:
    settling_time = time[outside_tolerance[-1]]
else:
    settling_time = 0

# Print settling time
#print(f"Settling Time: {settling_time:.4f} seconds")

# Display the chosen graph
if choice == "1":
    plt.figure()
    plt.plot(time, response)
    plt.title("Step Response of the Closed-Loop System")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

elif choice == "2":
    plt.figure()
    plt.plot(time, response)
    plt.axvline(x=t_10, color='r', linestyle='--', label=f'10% ({t_10:.2f}s)')
    plt.axvline(x=t_90, color='g', linestyle='--', label=f'90% ({t_90:.2f}s)')
    plt.title("Step Response with Rise Time Indicators")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f"Rise Time: {rise_time:.4f} seconds")

elif choice == "3":
    plt.figure()
    plt.plot(time, response)
    plt.axhline(y=final_value, color='r', linestyle='--', label='Final Value')
    plt.plot(time[np.argmax(response)], peak_value, 'ro', label=f'Peak Value ({peak_value:.2f})')
    plt.title("Step Response with Overshoot Calculation")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f"Overshoot: {overshoot:.2f}%")

elif choice == "4":
    plt.figure()
    plt.plot(time, response)
    plt.axhline(y=final_value + tolerance, color='r', linestyle='--', label=f'Upper 2% Tolerance')
    plt.axhline(y=final_value - tolerance, color='g', linestyle='--', label=f'Lower 2% Tolerance')
    plt.title("Step Response with Settling Time Calculation")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f"Settling Time: {settling_time:.4f} seconds")

else:
    print("Invalid choice! Please run the program again and choose a valid option.")
