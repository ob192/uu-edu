import matplotlib.pyplot as plt
import numpy as np

def plot_test_signals(student_number):
    """
    Task 3: Plot test signals for wireless network amplifier

    Parameters:
    -----------
    student_number : int
        Student number (a) used in signal equations

    Signals (variant 6-10):
    - Signal 1: y(x) = (a × 0.1) * sin(x)
    - Signal 2: y(x) = (a × 0.1) * log10(x)
    - Signal 3: y(x) = (a × 0.1) * cot(x)
    """

    a = student_number
    amplitude = a * 0.1

    # X range for signals
    x1 = np.linspace(0, 4*np.pi, 1000)  # For sin
    x2 = np.linspace(0.1, 10, 1000)     # For log (avoid x=0)
    x3 = np.linspace(0.1, 2*np.pi, 1000)  # For cot (avoid multiples of π)

    # Avoid division by zero for cotangent
    x3_safe = x3[(x3 % np.pi) > 0.1]

    # Calculate signals
    y1 = amplitude * np.sin(x1)
    y2 = amplitude * np.log10(x2)
    y3 = amplitude * (1 / np.tan(x3_safe))

    # Clip cotangent for visualization
    y3 = np.clip(y3, -5*amplitude, 5*amplitude)

    # Create figure with subplots
    fig = plt.figure(figsize=(14, 10))

    # === Subplot 1: Signal 1 (Sine) ===
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(x1, y1, 'b-', linewidth=2, label=f'$y_1(x) = {amplitude:.1f} \sin(x)$')
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('x [rad]', fontsize=10)
    ax1.set_ylabel('y₁(x)', fontsize=10)
    ax1.set_title('Test Signal #1: Sinusoidal', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')

    # === Subplot 2: Signal 2 (Logarithm) ===
    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(x2, y2, 'g-', linewidth=2, label=f'$y_2(x) = {amplitude:.1f} \log_{{10}}(x)$')
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    ax2.axvline(x=1, color='r', linestyle=':', linewidth=0.5, alpha=0.5, label='x=1')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('x', fontsize=10)
    ax2.set_ylabel('y₂(x)', fontsize=10)
    ax2.set_title('Test Signal #2: Logarithmic', fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right')

    # === Subplot 3: Signal 3 (Cotangent) ===
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(x3_safe, y3, 'r-', linewidth=2, label=f'$y_3(x) = {amplitude:.1f} \cot(x)$')
    ax3.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    # Mark asymptotes
    for n in range(1, 3):
        ax3.axvline(x=n*np.pi, color='orange', linestyle=':',
                    linewidth=1, alpha=0.5)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('x [rad]', fontsize=10)
    ax3.set_ylabel('y₃(x)', fontsize=10)
    ax3.set_title('Test Signal #3: Cotangent', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper right')
    ax3.set_ylim(-3*amplitude, 3*amplitude)

    # === Subplot 4: Combined view ===
    ax4 = plt.subplot(2, 2, 4)

    # Normalize x-ranges for comparison
    x_common = np.linspace(0, 2*np.pi, 1000)
    y1_common = amplitude * np.sin(x_common)
    y2_common = amplitude * np.log10(x_common + 0.1)  # Shift to avoid log(0)

    x3_common_safe = x_common[(x_common % np.pi) > 0.1]
    y3_common = amplitude * (1 / np.tan(x3_common_safe))
    y3_common = np.clip(y3_common, -3*amplitude, 3*amplitude)

    ax4.plot(x_common, y1_common, 'b-', linewidth=2,
             label='Signal 1: sin(x)', alpha=0.7)
    ax4.plot(x_common, y2_common, 'g-', linewidth=2,
             label='Signal 2: log(x)', alpha=0.7)
    ax4.plot(x3_common_safe, y3_common, 'r-', linewidth=2,
             label='Signal 3: cot(x)', alpha=0.7)

    ax4.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlabel('x [rad]', fontsize=10)
    ax4.set_ylabel('y(x)', fontsize=10)
    ax4.set_title('Combined: All Test Signals', fontsize=12, fontweight='bold')
    ax4.legend(loc='upper right')
    ax4.set_ylim(-2*amplitude, 2*amplitude)

    # Main title
    fig.suptitle(f'Wireless Network Amplifier Test Signals (Student #{a})',
                 fontsize=14, fontweight='bold', y=0.995)

    plt.tight_layout()
    plt.savefig('task3_test_signals.png', dpi=300, bbox_inches='tight')
    plt.show()

    # === Technical Analysis ===
    print("\n" + "="*60)
    print(f"SIGNAL ANALYSIS FOR STUDENT #{a}")
    print("="*60)
    print(f"\nAmplitude coefficient: {amplitude:.2f}")
    print(f"\nSignal 1 (Sine):")
    print(f"  - Amplitude: {amplitude:.2f}")
    print(f"  - Period: {2*np.pi:.4f} rad")
    print(f"  - Frequency: {1/(2*np.pi):.4f} Hz")
    print(f"\nSignal 2 (Logarithm):")
    print(f"  - Max value at x=10: {amplitude * np.log10(10):.4f}")
    print(f"  - Zero crossing: x = 1")
    print(f"\nSignal 3 (Cotangent):")
    print(f"  - Asymptotes at: x = nπ (n = 0, 1, 2, ...)")
    print(f"  - Period: π = {np.pi:.4f} rad")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Replace with your actual student number
    STUDENT_NUMBER = 15  # Example: change this to your number
    plot_test_signals(STUDENT_NUMBER)