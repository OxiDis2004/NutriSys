import numpy as np

if not hasattr(np, "int"):
    np.int = int
if not hasattr(np, "float"):
    np.float = float
if not hasattr(np, "bool"):
    np.bool = bool
if not hasattr(np, "complex"):
    np.complex = complex
if not hasattr(np, "trapz") or hasattr(np, "trapezoid"):
    np.trapz = np.trapezoid