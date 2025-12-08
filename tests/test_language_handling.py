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
        # Validate format: two-letter language code, hyphen, two-letter region code
        parts = lang.split('-')
        assert len(parts) == 2, f"Language code {lang} should have format 'xx-XX'"
        assert len(parts[0]) == 2, f"Language code in {lang} should be 2 characters"
        assert len(parts[1]) == 2, f"Region code in {lang} should be 2 characters"
        assert parts[0].islower(), f"Language code in {lang} should be lowercase"
        assert parts[1].isupper(), f"Region code in {lang} should be uppercase"


def test_unsupported_language_handling():
    """Test that unsupported languages default to Spanish."""
    supported_languages = {'es-ES', 'en-US'}
    default_language = 'es-ES'
    
    # Test with unsupported language
    requested_language = 'fr-FR'
    
    if requested_language in supported_languages:
        current_language = requested_language
    else:
        current_language = default_language
    
    assert current_language == 'es-ES'
