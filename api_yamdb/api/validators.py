from django.core.exceptions import ValidationError

def validate_username(value):
    invalid_characters = set(value) - set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.@+-_')
    if invalid_characters:
        raise ValidationError(f"Недопустимые символы в нике: {' '.join(invalid_characters)}")
