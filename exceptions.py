class RateLimitExceededError(Exception):
    """Exception raised when the rate limit is exceeded."""
    def __init__(self, status_code):
        self.message = f"{status_code}: Rate limit exceeded. Please try again later."
        super().__init__(self.message)

class BINLookupError(Exception):
    """Exception raised for errors in the BIN lookup."""
    def __init__(self, bin, status_code):
        self.message = f"Error fetching data for BIN {bin}: {status_code}"
        super().__init__(self.message)