import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from analyzer import (
    parse_coefficients, 
    create_system, 
    get_system_info, 
    get_step_info,
    get_margins,
    plot_step_response, 
    plot_impulse_response, 
    plot_bode, 
    plot_root_locus
)

st.set_page_config(page_title="Control System Simulator", page_icon="📈", layout="wide")

st.title("📈 Control System Simulator")
st.markdown("""
Analyze linear time-invariant (LTI) systems using transfer functions. 
Input your numerator and denominator coefficients to generate various system responses and stability analysis.
""")

# Predefined Examples
examples = {
    "Custom": {"num": "", "den": ""},
    "First-order (Low pass)": {"num": "1", "den": "1, 1"},
    "Second-order (Underdamped)": {"num": "1", "den": "1, 0.5, 1"},
    "Second-order (Critically Damped)": {"num": "1", "den": "1, 2, 1"},
    "Second-order (Overdamped)": {"num": "1", "den": "1, 3, 1"},
    "Unstable System": {"num": "1", "den": "1, -1, 1"}
}

st.sidebar.header("System Parameters")
selected_example = st.sidebar.selectbox("Choose an Example", list(examples.keys()))

default_num = examples[selected_example]["num"]
default_den = examples[selected_example]["den"]

# Provide inputs if custom or prefill if example selected
num_input = st.sidebar.text_input("Numerator Coefficients (e.g., 1 or 1, 2)", value=default_num)
den_input = st.sidebar.text_input("Denominator Coefficients (e.g., 1, 2, 1)", value=default_den)

if st.sidebar.button("Analyze System", type="primary"):
    st.session_state.analyze = True
    st.session_state.num_input = num_input
    st.session_state.den_input = den_input
elif "analyze" not in st.session_state:
    # Auto-analyze if an example is selected and it's not custom
    if selected_example != "Custom":
        st.session_state.analyze = True
        st.session_state.num_input = num_input
        st.session_state.den_input = den_input
    else:
        st.session_state.analyze = False

if st.session_state.get("analyze", False):
    try:
        # Parse inputs
        num_coeffs = parse_coefficients(st.session_state.num_input)
        den_coeffs = parse_coefficients(st.session_state.den_input)
        
        # Create system
        sys = create_system(num_coeffs, den_coeffs)
        sys_info = get_system_info(sys)
        step_metrics = get_step_info(sys)
        margin_metrics = get_margins(sys)
        
        # Display System Equation
        st.subheader("System Transfer Function")
        st.code(sys_info["equation"], language="text")
        
        # Display System Properties
        st.subheader("System Properties")
        col1, col2, col3 = st.columns(3)
        col1.metric("Stability", sys_info["stability"])
        
        with col2:
            st.markdown("**Poles:**")
            if len(sys_info["poles"]) > 0:
                for p in sys_info["poles"]:
                    st.write(f"- `{p}`")
            else:
                st.write("None")
                
        with col3:
            st.markdown("**Zeros:**")
            if len(sys_info["zeros"]) > 0:
                for z in sys_info["zeros"]:
                    st.write(f"- `{z}`")
            else:
                st.write("None")
                
        # Display Performance Metrics
        st.subheader("Performance Metrics (Step Response)")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Rise Time (s)", f"{step_metrics['RiseTime']:.4f}" if not np.isnan(step_metrics['RiseTime']) else "N/A")
        col_m2.metric("Settling Time (s)", f"{step_metrics['SettlingTime']:.4f}" if not np.isnan(step_metrics['SettlingTime']) else "N/A")
        col_m3.metric("Overshoot (%)", f"{step_metrics['Overshoot']:.2f}%" if not np.isnan(step_metrics['Overshoot']) else "N/A")

        # Display Margins
        st.subheader("Frequency Response Margins")
        col_g1, col_g2 = st.columns(2)
        gm_val = margin_metrics['GainMargin']
        pm_val = margin_metrics['PhaseMargin']
        col_g1.metric("Gain Margin (dB)", f"{gm_val:.2f}" if not np.isnan(gm_val) and not np.isinf(gm_val) else ("∞" if np.isinf(gm_val) else "N/A"))
        col_g2.metric("Phase Margin (°)", f"{pm_val:.2f}" if not np.isnan(pm_val) else "N/A")

        st.divider()
        
        # Tabs for plots
        tab1, tab2, tab3, tab4 = st.tabs([
            "Step Response", 
            "Impulse Response", 
            "Bode Plot", 
            "Root Locus"
        ])
        
        with tab1:
            st.markdown("**Step Response:** Shows how the system reacts to a sudden, constant input. It indicates stability, speed of response, and steady-state error.")
            fig_step = plot_step_response(sys)
            st.pyplot(fig_step)
            buf_step = io.BytesIO()
            fig_step.savefig(buf_step, format="png")
            st.download_button(label="Download Plot", data=buf_step.getvalue(), file_name="step_response.png", mime="image/png", key="dl_step")
            plt.close(fig_step)
            
        with tab2:
            st.markdown("**Impulse Response:** Shows the system's output when presented with a brief input signal. It characterizes the system's transient behavior.")
            fig_impulse = plot_impulse_response(sys)
            st.pyplot(fig_impulse)
            buf_imp = io.BytesIO()
            fig_impulse.savefig(buf_imp, format="png")
            st.download_button(label="Download Plot", data=buf_imp.getvalue(), file_name="impulse_response.png", mime="image/png", key="dl_imp")
            plt.close(fig_impulse)
            
        with tab3:
            st.markdown("**Bode Plot:** Displays the frequency response of the system, showing magnitude (in dB) and phase (in degrees) across a range of frequencies.")
            fig_bode = plot_bode(sys)
            st.pyplot(fig_bode)
            buf_bode = io.BytesIO()
            fig_bode.savefig(buf_bode, format="png")
            st.download_button(label="Download Plot", data=buf_bode.getvalue(), file_name="bode_plot.png", mime="image/png", key="dl_bode")
            plt.close(fig_bode)
            
        with tab4:
            st.markdown("**Root Locus:** Shows the paths of the closed-loop poles as a system parameter (typically gain) is varied. It helps in assessing stability.")
            fig_rlocus = plot_root_locus(sys)
            st.pyplot(fig_rlocus)
            buf_rl = io.BytesIO()
            fig_rlocus.savefig(buf_rl, format="png")
            st.download_button(label="Download Plot", data=buf_rl.getvalue(), file_name="root_locus.png", mime="image/png", key="dl_rl")
            plt.close(fig_rlocus)
            
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Please verify that your coefficients are valid numbers separated by spaces or commas.")
else:
    if selected_example == "Custom":
        st.info("Please enter the numerator and denominator coefficients and click 'Analyze System'.")
