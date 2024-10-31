import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class Concept:
    def __init__(self, name, magnitude, phase=0, color='b'):
        """
        Initialize a concept with a name, magnitude, phase, and color.
        
        Parameters:
        - name (str): Name of the concept (e.g., "Pet" or "Fish").
        - magnitude (float): The magnitude of the probability amplitude for the concept.
        - phase (float): The phase of the concept in radians (default is 0).
        - color (str): Color for the concept vector.
        """
        if magnitude < 0:
            raise ValueError("Magnitude must be non-negative")
            
        self.name = name
        self.amplitude = magnitude * np.exp(1j * phase)
        self.color = color
        
    @property
    def probability(self):
        """Calculate the probability for this concept."""
        return np.abs(self.amplitude) ** 2

def calculate_individual_probabilities(concepts):
    """Calculate individual probabilities for each concept."""
    return {concept.name: concept.probability for concept in concepts}

def calculate_combined_probability(concepts):
    """
    Calculate the combined probability using quantum interference effects.
    Includes proper normalization and interference terms.
    """
    combined_amplitude = sum(concept.amplitude for concept in concepts)
    
    individual_prob_sum = sum(concept.probability for concept in concepts)
    
    interference_term = 0
    for i, c1 in enumerate(concepts):
        for j, c2 in enumerate(concepts):
            if i != j:
                interference_term += np.real(c1.amplitude * np.conj(c2.amplitude))
    
    if individual_prob_sum > 0:
        combined_prob = (np.abs(combined_amplitude) ** 2) / individual_prob_sum
        combined_prob = np.clip(combined_prob, 0, 1)
    else:
        combined_prob = 0
        
    return combined_prob, interference_term

st.title("Quantum-Inspired Categorization Model")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pet Concept")
    magnitude_pet = float(st.text_input("Magnitude", "0.316", key="magnitude_pet"))
    phase_pet = float(st.text_input("Phase (radians)", "0.0", key="phase_pet"))

with col2:
    st.subheader("Fish Concept")
    magnitude_fish = float(st.text_input("Magnitude", "0.316", key="magnitude_fish"))
    phase_fish = float(st.text_input("Phase (radians)", "0.0", key="phase_fish"))

try:
    pet = Concept("Pet", magnitude=magnitude_pet, phase=phase_pet, color='blue')
    fish = Concept("Fish", magnitude=magnitude_fish, phase=phase_fish, color='green')
    concepts = [pet, fish]

    individual_probs = calculate_individual_probabilities(concepts)
    combined_prob, interference = calculate_combined_probability(concepts)

    st.subheader("Individual Probabilities")
    for name, prob in individual_probs.items():
        st.write(f"{name}: {prob:.3f}")

    st.subheader("Combined Probability (Pet Fish)")
    st.write(f"Combined Probability: {combined_prob:.3f}")
    st.write(f"Interference Term: {interference:.3f}")

    fig, ax = plt.subplots(figsize=(8, 8))
    
    circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--', alpha=0.5)
    ax.add_artist(circle)
    
    for concept in concepts:
        ax.quiver(0, 0, concept.amplitude.real, concept.amplitude.imag,
                 color=concept.color, angles='xy', scale_units='xy', scale=1,
                 label=concept.name, width=0.008)
        ax.text(concept.amplitude.real * 1.1, concept.amplitude.imag * 1.1,
                f"{concept.name}\n|ψ|={np.abs(concept.amplitude):.2f}\nφ={np.angle(concept.amplitude):.2f}",
                color=concept.color, fontsize=10)

    combined_amplitude = sum(concept.amplitude for concept in concepts)
    ax.quiver(0, 0, combined_amplitude.real, combined_amplitude.imag,
             color='red', angles='xy', scale_units='xy', scale=1,
             label="Combined", width=0.008)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Probability Amplitudes in Complex Plane")
    ax.legend()
    
    st.pyplot(fig)

except ValueError as e:
    st.error(f"Error: {str(e)}")
