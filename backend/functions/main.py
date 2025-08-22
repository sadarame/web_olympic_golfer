import firebase_admin

# Ensure the default Firebase app is initialized only once
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

# Example function using Firebase services
# In actual deployment, this would expose an HTTPS function or another trigger.

def example_usage():
    """Placeholder function demonstrating Firebase initialization."""
    return "Firebase app initialized: {}".format(firebase_admin.get_app().name)
