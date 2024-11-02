import numpy as np
import pandas as pd
import random
import streamlit as st
from matplotlib import pyplot as plt

class Concept:
    def __init__(self, name, probability, phase=0, color='b'):
        if probability < 0:
            raise ValueError("Probability must be non-negative")
        if probability > 1:
            raise ValueError("Probability must be less than or equal to 1")
            
        self.name = name
        self.amplitude = np.sqrt(probability) * np.exp(1j * phase)
        self.color = color
        self._probability = probability

    @property
    def probability(self):
        return self._probability

class CompositeConcept(Concept):
    def __init__(self, name, concepts, interference_phases=None, color='b'):
        self.name = name
        self.concepts = concepts
        self.interference_phases = interference_phases or [0]*len(concepts)
        self.color = color
        self.amplitude = self.calculate_combined_amplitude()
        self._probability = np.abs(self.amplitude) ** 2

    def calculate_combined_amplitude(self):
        total_prob = sum(concept.probability for concept in self.concepts)
        if total_prob == 0:
            return 0
        
        normalization_factor = np.sqrt(1 / total_prob)
        
        combined_amplitude = 0
        for concept, phase_shift in zip(self.concepts, self.interference_phases):
            normalized_amplitude = concept.amplitude * normalization_factor
            shifted_amplitude = normalized_amplitude * np.exp(1j * phase_shift)
            combined_amplitude += shifted_amplitude
            
        return combined_amplitude

class ConceptManager:
    def __init__(self):
        self.concepts = {}
        self.relations = []

    def add_concept(self, concept):
        self.concepts[concept.name] = concept

    def remove_concept(self, name):
        if name in self.concepts:
            dependent_concepts = []
            for concept_name, concept in self.concepts.items():
                if isinstance(concept, CompositeConcept):
                    if any(c.name == name for c in concept.concepts):
                        dependent_concepts.append(concept_name)
        
            for concept_name in dependent_concepts:
                del self.concepts[concept_name]
                self.relations = [r for r in self.relations if r[1] != concept_name]
            
            del self.concepts[name]

    def add_relation(self, concept_names, new_name, interference_phases=None, color='b'):
        if not all(name in self.concepts for name in concept_names):
            missing = [name for name in concept_names if name not in self.concepts]
            raise ValueError(f"Concepts not found: {missing}")
            
        concepts = [self.concepts[name] for name in concept_names]
        composite_concept = CompositeConcept(new_name, concepts, interference_phases, color=color)
        self.add_concept(composite_concept)
        self.relations.append((concept_names, new_name, interference_phases))
        return composite_concept
    
def calculate_individual_probabilities(concepts):
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

def plot_complex_plane(concepts):
    """
    Plot quantum concepts on the complex plane with normalized amplitudes, combined state,
    and individual probabilities for each concept. Labels are positioned to avoid overlap.
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw unit circle
    circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--', alpha=0.5)
    ax.add_artist(circle)

    xlim, ylim = 1.2, 1.2

    def calculate_label_position(amplitude, fixed_distance=0.3):
        """
        Calculate label position based on vector angle and a fixed distance.
        Uses the angle of the amplitude but places label at fixed distance.
        """
        if amplitude == 0:
            return fixed_distance, fixed_distance
        
        angle = np.angle(amplitude)
        
        label_x = fixed_distance * np.cos(angle)
        label_y = fixed_distance * np.sin(angle)
        
        min_spacing = 0.05
        if abs(label_x) < min_spacing:
            label_x = min_spacing if label_x >= 0 else -min_spacing
        if abs(label_y) < min_spacing:
            label_y = min_spacing if label_y >= 0 else -min_spacing
            
        label_x += amplitude.real
        label_y += amplitude.imag
        
        label_x = np.clip(label_x, -xlim + 0.2, xlim - 0.2)
        label_y = np.clip(label_y, -ylim + 0.2, ylim - 0.2)
        
        return label_x, label_y

    individual_probs = calculate_individual_probabilities(concepts)
    combined_prob, interference_term = calculate_combined_probability(concepts)
    
    total_prob = sum(concept.probability for concept in concepts)
    normalization_factor = np.sqrt(1 / total_prob) if total_prob > 0 else 1
    
    for concept in concepts:
        normalized_amplitude = concept.amplitude * normalization_factor
        
        ax.quiver(0, 0, normalized_amplitude.real, normalized_amplitude.imag,
                  color=concept.color, angles='xy', scale_units='xy', scale=1,
                  label=f"{concept.name} (P={individual_probs[concept.name]:.2f})", 
                  width=0.008)
        
        label_x, label_y = calculate_label_position(normalized_amplitude)
        
        ax.plot([normalized_amplitude.real, label_x], 
                [normalized_amplitude.imag, label_y],
                color=concept.color, linestyle=':', alpha=0.5)
        
        label_text = f"{concept.name}\n|ψ|={np.abs(normalized_amplitude):.2f}\n"\
                     f"φ={np.angle(normalized_amplitude):.2f}\n"\
                     f"P={individual_probs[concept.name]:.2f}"
        
        bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec=concept.color, alpha=0.8)
        ax.text(label_x, label_y, label_text,
                color=concept.color, fontsize=9, ha='center', va='center',
                bbox=bbox_props)

    combined_amplitude = sum(concept.amplitude * normalization_factor for concept in concepts)
    
    ax.quiver(0, 0, combined_amplitude.real, combined_amplitude.imag,
              color='red', angles='xy', scale_units='xy', scale=1,
              label=f"Combined (P={combined_prob:.2f})", width=0.008)

    label_x, label_y = calculate_label_position(combined_amplitude)
    
    ax.plot([combined_amplitude.real, label_x],
            [combined_amplitude.imag, label_y],
            color='red', linestyle=':', alpha=0.5)
    
    combined_text = f"Combined\n|ψ|={np.abs(combined_amplitude):.2f}\n"\
                    f"φ={np.angle(combined_amplitude):.2f}\n"\
                    f"P={combined_prob:.2f}\n"\
                    f"Int={interference_term:.2f}"
    
    bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec='red', alpha=0.8)
    ax.text(label_x, label_y, combined_text,
            color='red', fontsize=9, ha='center', va='center',
            bbox=bbox_props)

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_aspect('equal', 'box')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Normalized Probability Amplitudes in Complex Plane")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    st.set_page_config(page_title="Quantum Concept Manager", layout="wide")

    st.title("Quantum Concept Manager")

    if 'manager' not in st.session_state:
        st.session_state.manager = ConceptManager()
    if 'interference_term' not in st.session_state:
        st.session_state.interference_term = None
    if 'show_visualization' not in st.session_state:
        st.session_state.show_visualization = False
    if 'probabilities_dataframe' not in st.session_state:
        st.session_state.probabilities_dataframe = pd.DataFrame()

    tabs = st.tabs(["Add Concept", "Create Composite Concept", "Visualization"])

    # Concept Tab
    with tabs[0]:
        st.header("Add Concept")
        if 'new_concept_color' not in st.session_state:
            st.session_state.new_concept_color = random_color()
        with st.form("add_concept_form"):
            name = st.text_input("Name")
            magnitude = st.number_input("Probability", min_value=0.0, max_value=1.0, value=1.0)
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
                    del st.session_state.new_composite_color
                    st.rerun()
                else:
                    st.error("Please enter a name for the composite concept.")
            elif submitted:
                st.error("Please select at least one concept to combine.")

    # Visualization Tab
    with tabs[2]:
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
                st.markdown(f"- Probability: {concept.probability:.2f}")
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
