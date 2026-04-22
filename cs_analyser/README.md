# Control System Simulator

A professional, interactive web application built with Python and Streamlit to analyze linear time-invariant (LTI) systems. This tool serves as a mini engineering simulator, providing comprehensive time-domain and frequency-domain insights.

## Features

- **Transfer Function Input**: Easily enter numerator and denominator coefficients.
- **Stability Analysis**: Automatically computes poles, zeros, and determines system stability.
- **Performance Metrics**: Computes Rise Time, Settling Time, and Overshoot from the Step Response.
- **Frequency Response Margins**: Calculates and displays Gain Margin and Phase Margin.
- **Predefined Examples**: Quickly load examples like first-order, underdamped, and unstable systems to explore different behaviors.
- **Interactive Visualizations**: Generates high-quality plots for:
  - Step Response
  - Impulse Response
  - Bode Plot
  - Root Locus
- **Plot Downloads**: Download any generated plot as a high-resolution PNG image directly from the interface.

## Tech Stack

- **Python 3.8+**
- **Streamlit**: For the interactive web interface
- **NumPy**: For numerical computations
- **Matplotlib**: For generating plots and visual analysis
- **Python-Control (`control`)**: For core control system computations

## Installation

1. Clone the repository (or download the source code).
2. Ensure you have Python 3.8 or higher installed.
3. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application Locally

To start the Control System Simulator locally, run the following command in your terminal:
```bash
streamlit run app.py
```
This will launch the app in your default web browser (typically at `http://localhost:8501`).

## Deployment

This app is designed to be easily deployable on **Streamlit Cloud**:
1. Push your code (including `app.py`, `analyzer.py`, and `requirements.txt`) to a GitHub repository.
2. Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click "New app" and connect your GitHub account.
4. Select the repository, branch, and set the main file path to `app.py`.
5. Click "Deploy"!

## Project Structure

- `app.py`: Contains the Streamlit user interface and application logic.
- `analyzer.py`: Contains the core control system logic and plotting functions, keeping the UI separate from computations.
- `requirements.txt`: Lists all Python dependencies required to run the app.
