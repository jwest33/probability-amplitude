import numpy as np
import pandas as pd
import random
import streamlit as st
from matplotlib import pyplot as plt

class Concept:
    def __init__(self, name, magnitude, phase=0, color='b'):
        if magnitude < 0:
            raise ValueError("Magnitude must be non-negative")
        self.name = name
        self.amplitude = magnitude * np.exp(1j * phase)
        self.color = color

    @property
    def probability(self):
        return np.abs(self.amplitude) ** 2

class CompositeConcept(Concept):
    def __init__(self, name, concepts, interference_phases=None, color='b'):
        self.name = name
        self.concepts = concepts
        self.interference_phases = interference_phases or [0]*len(concepts)
        self.color = color
        self.amplitude = self.calculate_combined_amplitude()

    def calculate_combined_amplitude(self):
        combined_amplitude = 0
        for concept, phase_shift in zip(self.concepts, self.interference_phases):
            amplitude = np.abs(concept.amplitude) * np.exp(1j * (np.angle(concept.amplitude) + phase_shift))
            combined_amplitude += amplitude
        return combined_amplitude

class ConceptManager:
    def __init__(self):
        self.concepts = {}
        self.relations = []

    def add_concept(self, concept):
        self.concepts[concept.name] = concept

    def remove_concept(self, name):
        if name in self.concepts:
            del self.concepts[name]

    def add_relation(self, concept_names, new_name, interference_phases=None, color='b'):
        concepts = [self.concepts[name] for name in concept_names]
        composite_concept = CompositeConcept(new_name, concepts, interference_phases, color=color)
        self.add_concept(composite_concept)
        self.relations.append((concept_names, new_name, interference_phases))
        return composite_concept

def calculate_individual_probabilities(concepts):
    return {concept.name: concept.probability for concept in concepts}

def calculate_combined_probability(concepts):
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

def plot_complex_plane(concepts):
    fig, ax = plt.subplots(figsize=(10, 10))

    circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--', alpha=0.5)
    ax.add_artist(circle)

    xlim, ylim = 1.2, 1.2

    def get_offset_position(x, y):
        x = min(max(x, -xlim), xlim)
        y = min(max(y, -ylim), ylim)
        return x, y
    
    for concept in concepts:
        ax.quiver(0, 0, concept.amplitude.real, concept.amplitude.imag,
                  color=concept.color, angles='xy', scale_units='xy', scale=1,
                  label=concept.name, width=0.008)
        
        label_x, label_y = concept.amplitude.real * 1.1, concept.amplitude.imag * 1.1
        label_x, label_y = get_offset_position(label_x, label_y)
        
        ax.text(label_x, label_y,
                f"{concept.name}\n|ψ|={np.abs(concept.amplitude):.2f}\nφ={np.angle(concept.amplitude):.2f}",
                color=concept.color, fontsize=10, ha='center', va='center')

    combined_amplitude = sum(concept.amplitude for concept in concepts)
    ax.quiver(0, 0, combined_amplitude.real, combined_amplitude.imag,
              color='red', angles='xy', scale_units='xy', scale=1,
              label="Combined", width=0.008)
    
    label_x, label_y = combined_amplitude.real * 1.1, combined_amplitude.imag * 1.1
    label_x, label_y = get_offset_position(label_x, label_y)
    
    ax.text(label_x, label_y,
            f"Combined\n|ψ|={np.abs(combined_amplitude):.2f}\nφ={np.angle(combined_amplitude):.2f}",
            color='red', fontsize=10, ha='center', va='center')

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_aspect('equal', 'box')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Probability Amplitudes in Complex Plane")
    ax.legend()

    st.pyplot(fig)

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    st.set_page_config(page_title="Quantum Concept Manager", layout="wide")

    st.title("Quantum Concept Manager")

    if 'manager' not in st.session_state:
        st.session_state.manager = ConceptManager()
    if 'probabilities' not in st.session_state:
        st.session_state.probabilities = None
    if 'combined_probability' not in st.session_state:
        st.session_state.combined_probability = None
    if 'interference_term' not in st.session_state:
        st.session_state.interference_term = None
    if 'show_visualization' not in st.session_state:
        st.session_state.show_visualization = False
    if 'probabilities_dataframe' not in st.session_state:
        st.session_state.probabilities_dataframe = pd.DataFrame()

    tabs = st.tabs(["Add Concept", "Create Composite Concept", "Probabilities", "Visualization"])

    # Concept Tab
    with tabs[0]:
        st.header("Add Concept")
        if 'new_concept_color' not in st.session_state:
            st.session_state.new_concept_color = random_color()
        with st.form("add_concept_form"):
            name = st.text_input("Name")
            magnitude = st.number_input("Magnitude", min_value=0.0, value=1.0)
            phase = st.number_input("Phase (radians)", value=0.0)
            color = st.color_picker("Color", st.session_state.new_concept_color)
            submitted = st.form_submit_button("Add Concept")
            if submitted:
                if name:
                    concept = Concept(name, magnitude, phase, color)
                    st.session_state.manager.add_concept(concept)
                    st.success(f"Concept '{name}' added.")
                    del st.session_state.new_concept_color
                    st.rerun()
                else:
                    st.error("Please enter a name for the concept.")

    # Composite Concept Tab
    with tabs[1]:
        st.header("Create Composite Concept")
        if 'new_composite_color' not in st.session_state:
            st.session_state.new_composite_color = random_color()
        with st.form("create_composite_form"):
            composite_name = st.text_input("Composite Concept Name")
            selected_concepts = st.multiselect("Select Concepts", st.session_state.manager.concepts.keys())
            interference_phases = []
            if selected_concepts:
                st.subheader("Interference Phase Shifts")
                for concept_name in selected_concepts:
                    phase_shift = st.number_input(f"Phase Shift for '{concept_name}'", value=0.0, key=f"phase_{concept_name}")
                    interference_phases.append(phase_shift)
            else:
                st.write("Select concepts to combine.")
            composite_color = st.color_picker("Composite Color", st.session_state.new_composite_color)
            submitted = st.form_submit_button("Create Composite Concept")
            if submitted and selected_concepts:
                if composite_name:
                    st.session_state.manager.add_relation(
                        selected_concepts,
                        composite_name,
                        interference_phases,
                        color=composite_color
                    )
                    st.success(f"Composite Concept '{composite_name}' created.")
                    # Reset the random color for the next composite concept
                    del st.session_state.new_composite_color
                    st.rerun()
                else:
                    st.error("Please enter a name for the composite concept.")
            elif submitted:
                st.error("Please select at least one concept to combine.")

    # Probabilities Tab
    with tabs[2]:
        st.header("Calculate Probabilities")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Calculate Individual Probabilities"):
                st.session_state.probabilities = calculate_individual_probabilities(st.session_state.manager.concepts.values())
                st.success("Calculated individual probabilities.")
            if st.session_state.probabilities is not None:
                st.subheader("Individual Probabilities")
                st.session_state.probabilities_dataframe = pd.DataFrame(list(st.session_state.probabilities.items()), columns=["Concept", "Probability"])
                st.dataframe(st.session_state.probabilities_dataframe, hide_index=True)

        with col2:
            if st.button("Calculate Combined Probability"):
                combined_prob, interference_term = calculate_combined_probability(st.session_state.manager.concepts.values())
                st.session_state.combined_probability = combined_prob
                st.session_state.interference_term = interference_term
                st.success("Calculated combined probability.")
            if st.session_state.combined_probability is not None:
                st.subheader("Combined Probability")
                combined_data = {
                    "Metric": ["Combined Probability", "Interference Term"],
                    "Value": [st.session_state.combined_probability, st.session_state.interference_term]
                }
                st.dataframe(combined_data)

    # Visualization Tab
    with tabs[3]:
        st.header("Visualization")
        col1, col2 = st.columns([3,1])
        with col1:
            if st.button("Visualize Concepts in Complex Plane"):
                st.session_state.show_visualization = True
            if st.session_state.show_visualization:
                if st.session_state.manager.concepts:
                    plot_complex_plane(st.session_state.manager.concepts.values())
                else:
                    st.warning("No concepts available to visualize.")

    # Sidebar for Current Concepts
    with st.sidebar:
        st.header("Current Concepts")
        if st.session_state.manager.concepts:
            concepts_list = list(st.session_state.manager.concepts.keys())
            for name in concepts_list:
                concept = st.session_state.manager.concepts[name]
                st.markdown(f"**{name}**")
                st.markdown(f"- Magnitude: {np.abs(concept.amplitude):.2f}")
                st.markdown(f"- Phase: {np.angle(concept.amplitude):.2f} rad")
                st.markdown(
                    f"<div style='width:20px;height:20px;background-color:{concept.color};border:1px solid #000;'></div>",
                    unsafe_allow_html=True)
                st.markdown("---")
            remove_name = st.selectbox("Select Concept to Remove", [""] + concepts_list, key="remove_concept")
            if st.button("Remove Concept", key="remove_button"):
                if remove_name:
                    st.session_state.manager.remove_concept(remove_name)
                    st.success(f"Concept '{remove_name}' removed.")
                    st.rerun()
        else:
            st.write("No concepts available.")

if __name__ == "__main__":
    main()
