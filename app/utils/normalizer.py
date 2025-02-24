import numpy as np

class Normalizer:
    def __init__(self):
        """Initialise le normaliseur avec des attributs mu (moyenne) et sd (écart-type) à None."""
        self.mu = None  # Moyenne des données
        self.sd = None  # Écart-type des données

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        """
        Calcule la moyenne et l'écart-type des données, puis normalise les données en entrée.
        
        Args:
            x (np.ndarray): Tableau de données à normaliser (par exemple, prix de clôture).
        
        Returns:
            np.ndarray: Données normalisées (x - mu) / sd.
        """
        self.mu = np.mean(x, axis=0, keepdims=True)
        self.sd = np.std(x, axis=0, keepdims=True)
        normalized_x = (x - self.mu) / self.sd
        return normalized_x

    def inverse_transform(self, x: np.ndarray) -> np.ndarray:
        """
        Dénormalise les données en utilisant la moyenne et l'écart-type précédemment calculés.
        
        Args:
            x (np.ndarray): Tableau de données normalisées à dénormaliser.
        
        Returns:
            np.ndarray: Données dénormalisées (x * sd) + mu.
        """
        if self.mu is None or self.sd is None:
            raise ValueError("Normalizer has not been fitted yet. Call fit_transform first.")
        return (x * self.sd) + self.mu