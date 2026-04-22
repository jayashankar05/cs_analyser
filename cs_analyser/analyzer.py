import numpy as np
import matplotlib.pyplot as plt
import control as ct

def parse_coefficients(coeff_str):
    """Parses a string of coefficients into a list of floats."""
    if not coeff_str or not str(coeff_str).strip():
        raise ValueError("Input cannot be empty.")
    
    # Remove brackets if user typed them
    clean_str = str(coeff_str).replace('[', '').replace(']', '').strip()
    
    # Split by comma if present, else by space
    if ',' in clean_str:
        parts = clean_str.split(',')
    else:
        parts = clean_str.split()
        
    try:
        return [float(p.strip()) for p in parts if p.strip()]
    except ValueError:
        raise ValueError("Invalid format. Please enter numbers separated by spaces or commas.")

def create_system(num, den):
    """Creates a control TransferFunction."""
    if not num or not den:
         raise ValueError("Numerator and denominator must have at least one coefficient.")
    if all(n == 0 for n in num):
         raise ValueError("Numerator cannot be all zeros.")
    if all(d == 0 for d in den):
         raise ValueError("Denominator cannot be all zeros.")
    return ct.TransferFunction(num, den)

def get_system_info(sys):
    """Returns poles, zeros, and stability information."""
    poles = ct.poles(sys)
    zeros = ct.zeros(sys)
    
    # Basic stability check for continuous LTI systems
    if len(poles) > 0:
        real_parts = np.real(poles)
        is_strictly_stable = np.all(real_parts < -1e-10)
        has_rhp = np.any(real_parts > 1e-10)
        
        if is_strictly_stable:
            stability = "Stable"
        elif has_rhp:
            stability = "Unstable"
        else:
            stability = "Marginally Stable"
    else:
        stability = "Stable (No poles)"
        
    return {
        "poles": np.round(poles, 4),
        "zeros": np.round(zeros, 4),
        "stability": stability,
        "equation": str(sys)
    }

def get_step_info(sys):
    """Computes step response performance metrics."""
    try:
        info = ct.step_info(sys)
        return {
            "RiseTime": info.get("RiseTime", np.nan),
            "SettlingTime": info.get("SettlingTime", np.nan),
            "Overshoot": info.get("Overshoot", np.nan)
        }
    except Exception:
        return {"RiseTime": np.nan, "SettlingTime": np.nan, "Overshoot": np.nan}

def get_margins(sys):
    """Computes gain and phase margins."""
    try:
        gm, pm, wg, wp = ct.margin(sys)
        # ct.margin might return infinity for gm
        if gm == np.inf:
            gm_db = np.inf
        elif gm > 0:
            gm_db = 20 * np.log10(gm)
        else:
            gm_db = np.nan
        return {
            "GainMargin": gm_db,
            "PhaseMargin": pm
        }
    except Exception:
        return {"GainMargin": np.nan, "PhaseMargin": np.nan}


def plot_step_response(sys):
    """Generates a step response plot."""
    time, response = ct.step_response(sys)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(time, response, color='#1f77b4', linewidth=2)
    ax.set_title('Step Response', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel('Amplitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig

def plot_impulse_response(sys):
    """Generates an impulse response plot."""
    time, response = ct.impulse_response(sys)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(time, response, color='#d62728', linewidth=2)
    ax.set_title('Impulse Response', fontsize=14, fontweight='bold')
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel('Amplitude', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig

def plot_bode(sys):
    """Generates a Bode plot."""
    fig = plt.figure(figsize=(10, 7))
    try:
        # Some versions of control use margins=True, others might not support it directly in bode_plot
        ct.bode_plot(sys, dB=True, margins=True, grid=True)
    except TypeError:
        ct.bode_plot(sys, dB=True, grid=True)
    
    # Find the current figure
    fig = plt.gcf()
    fig.suptitle('Bode Plot', fontsize=14, fontweight='bold')
    fig.tight_layout()
    return fig

def plot_root_locus(sys):
    """Generates a Root Locus plot."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ct.root_locus(sys, plot=True, ax=ax, grid=True)
    ax.set_title('Root Locus', fontsize=14, fontweight='bold')
    ax.set_xlabel('Real Axis', fontsize=12)
    ax.set_ylabel('Imaginary Axis', fontsize=12)
    fig.tight_layout()
    return fig
