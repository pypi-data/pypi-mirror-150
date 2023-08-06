"""BaseStringClass"""

class Base:
    """FastString class provide fast string operations."""
    def __init__(self, value):
        """Initilize BaseString

        Args:
            value (value): str
        """
        self.value = value


    def __eq__(self, value):
        return self.value == value

