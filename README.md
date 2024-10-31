# Quantum-Inspired Categorization Model

A Streamlit application that visualizes probability amplitudes for concept categorization using quantum-inspired mathematics. This tool helps explore how concepts combine and interfere in human cognition, based on quantum probability theory.

## Overview

This application implements a quantum probability approach to modeling how humans combine concepts, inspired by cognitive science research suggesting that human categorization often violates classical probability rules. The model represents concepts as complex probability amplitudes and visualizes how they combine, including interference effects.

## Features

- Interactive setting of probability amplitudes for different concepts
- Real-time visualization of concept vectors in the complex plane
- Calculation of individual and combined probabilities
- Visualization of quantum interference effects
- Dynamic updating of probabilities and visualizations
- Error handling and input validation

## Dependencies

- streamlit
- numpy
- matplotlib
- Python 3.7+

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Adjust the parameters:
   - Set magnitude and phase for the "Pet" concept
   - Set magnitude and phase for the "Fish" concept
   - Observe how the combined "Pet Fish" concept emerges

## Mathematical Background

The application uses quantum probability theory principles:

1. **Probability Amplitudes**: Each concept is represented as a complex number ψ = r*e^(iθ), where:
   - r (magnitude) represents the concept's strength
   - θ (phase) represents the concept's context or perspective

2. **Individual Probabilities**: Calculated using Born's rule: P = |ψ|²

3. **Combined Probabilities**: Include interference terms:
   - P(A+B) = |ψₐ + ψᵦ|² = |ψₐ|² + |ψᵦ|² + 2|ψₐ||ψᵦ|cos(θₐ - θᵦ)

## Theory and Applications

This model is particularly useful for understanding:
- Concept combinations that violate classical probability rules
- Context-dependent categorization
- Interference effects in human decision-making
- Non-classical conjunction effects in cognition

## Example Use Cases

1. **Pet-Fish Problem**: Understanding why typical pet fish are rated as better examples of "pet fish" than they are of either "pet" or "fish" individually.

2. **Context Effects**: Exploring how the meaning of concepts changes based on context through phase relationships.

3. **Interference Patterns**: Visualizing how different concept combinations can interfere constructively or destructively.
