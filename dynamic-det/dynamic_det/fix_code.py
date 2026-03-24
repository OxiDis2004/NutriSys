import numpy as np

if not hasattr(np, "int"):
    np.int = int
if not hasattr(np, "float"):
    np.float = float
if not hasattr(np, "bool"):
    np.bool = bool
# if not hasattr(np, "object"):
#     np.object = object
# if not hasattr(np, "str"):
#     np.str = str
if not hasattr(np, "complex"):
    np.complex = complex