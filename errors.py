# errors.py
class VoidError(Exception):
    pass

class ModelLoadError(VoidError):
    pass

class GenerationError(VoidError):
    pass

class MemoryErrorVoid(VoidError):
    pass