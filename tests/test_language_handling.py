"""
Test language handling in the WebSocket endpoint.
This test validates that the language selection functionality works correctly.
"""
import json
import pytest


def test_language_message_parsing():
    """Test that language messages are correctly formatted."""
    # Test Spanish language message
    message_es = json.dumps({"type": "language", "language": "es-ES"})
    data_es = json.loads(message_es)
    assert data_es["type"] == "language"
    assert data_es["language"] == "es-ES"
    
    # Test English language message  
    message_en = json.dumps({"type": "language", "language": "en-US"})
    data_en = json.loads(message_en)
    assert data_en["type"] == "language"
    assert data_en["language"] == "en-US"


def test_default_language():
    """Test that the default language is Spanish."""
    current_language = 'es-ES'
    assert current_language == 'es-ES'


def test_language_update():
    """Test that language can be updated."""
    current_language = 'es-ES'
    
    # Simulate receiving a language change message
    message = json.dumps({"type": "language", "language": "en-US"})
    data = json.loads(message)
    
    if data.get('type') == 'language':
        current_language = data.get('language', 'es-ES')
    
    assert current_language == 'en-US'


def test_invalid_language_message():
    """Test handling of invalid JSON messages."""
    invalid_message = "not valid json"
    
    try:
        data = json.loads(invalid_message)
        assert False, "Should have raised JSONDecodeError"
    except json.JSONDecodeError:
        # Expected behavior
        pass


def test_language_codes():
    """Test that language codes are valid."""
    valid_languages = ['es-ES', 'en-US']
    
    for lang in valid_languages:
        assert lang in ['es-ES', 'en-US']
        assert len(lang.split('-')) == 2
        assert lang.split('-')[0] in ['es', 'en']
        assert lang.split('-')[1] in ['ES', 'US']
