# Import AppConfig for configuring the Django app
from django.apps import AppConfig

# Configuration class for the learninghub app
class LearninghubConfig(AppConfig):
    # Set the default auto field type for primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    # Name of the app
    name = 'learninghub'
