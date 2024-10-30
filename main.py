import numpy as np

class Concept:
    def __init__(self, name, magnitude, phase=0):
        """
        Initialize a concept with a name, magnitude, and phase.
        
        Parameters:
        - name (str): Name of the concept (e.g., "Pet" or "Fish").
        - magnitude (float): The magnitude of the probability amplitude for the concept.
        - phase (float): The phase of the concept in radians (default is 0).
        """
        self.name = name
        self.amplitude = magnitude * np.exp(1j * phase)

def calculate_individual_probabilities(concepts):
    """
    Calculate individual probabilities for each concept.
    
    Parameters:
    - concepts (list of Concept): List of Concept objects.
    
    Returns:
    - dict: Dictionary of probabilities for each concept individually.
    """
    probabilities = {}
    for concept in concepts:
        probabilities[concept.name] = np.abs(concept.amplitude) ** 2
    return probabilities

def calculate_combined_probability_with_normalization(concepts):
    """
    Calculate the probability amplitude for the combined concept and normalize it.
    
    Parameters:
    - concepts (list of Concept): List of Concept objects.
    
    Returns:
    - float: Normalized probability for the combined concept.
    """
    # Calculate the unnormalized combined amplitude
    combined_amplitude = sum(concept.amplitude for concept in concepts)
    combined_probability = np.abs(combined_amplitude) ** 2

    # Calculate total of individual probabilities
    individual_prob_sum = sum(np.abs(concept.amplitude) ** 2 for concept in concepts)

    # Normalize the combined probability based on individual probabilities
    if individual_prob_sum > 0:
        normalized_combined_probability = combined_probability / (combined_probability + individual_prob_sum)
    else:
        normalized_combined_probability = 0

    return normalized_combined_probability

# Example usage
if __name__ == "__main__":
    # Define the individual concepts "Pet" and "Fish" with their magnitudes and phases
    pet = Concept("Pet", magnitude=1/np.sqrt(3), phase=0)
    fish = Concept("Fish", magnitude=1/np.sqrt(2), phase=0)  # Adjust phase if needed

    # Combine into a list
    concepts = [pet, fish]

    # Calculate individual probabilities
    individual_probs = calculate_individual_probabilities(concepts)
    print("Individual Probabilities:")
    for name, prob in individual_probs.items():
        print(f"{name}: {prob:.2f}")

    # Calculate the normalized combined probability for the concept "Pet Fish"
    combined_prob = calculate_combined_probability_with_normalization(concepts)
    print("\nNormalized Combined Probability (Pet Fish):")
    print(f"Pet Fish: {combined_prob:.2f}")
