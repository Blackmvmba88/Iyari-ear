"""
Tests for VLC plugin generator
"""
import pytest
import os
import tempfile
from vlc_plugin_generator import VLCPluginGenerator


def test_vlc_plugin_generator_init():
    """Test initializing VLC plugin generator"""
    generator = VLCPluginGenerator(
        api_url="http://localhost:8000"
    )
    
    assert generator.api_url == "http://localhost:8000"
    assert generator.version == "1.0.0"
    assert generator.cache_dir is not None


def test_generate_plugin():
    """Test generating VLC plugin"""
    generator = VLCPluginGenerator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        tmp_path = f.name
    
    try:
        plugin_path = generator.generate_plugin(output_path=tmp_path)
        
        assert os.path.exists(plugin_path)
        assert plugin_path == tmp_path
        
        # Verify plugin content
        with open(plugin_path, 'r') as f:
            content = f.read()
            assert "Iyari-ear Subtitle Optimizer" in content
            assert "function descriptor()" in content
            assert "function activate()" in content
            assert generator.api_url in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_generate_plugin_with_custom_settings():
    """Test generating plugin with custom settings"""
    generator = VLCPluginGenerator(api_url="http://192.168.1.100:9000")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        tmp_path = f.name
    
    try:
        plugin_path = generator.generate_plugin(
            output_path=tmp_path,
            auto_optimize=False,
            max_cache_size=200
        )
        
        with open(plugin_path, 'r') as f:
            content = f.read()
            assert "http://192.168.1.100:9000" in content
            assert "auto_optimize = false" in content
            assert "max_cache_size_mb = 200" in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_generate_readme():
    """Test generating README"""
    generator = VLCPluginGenerator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        tmp_path = f.name
    
    try:
        readme_path = generator.generate_readme(output_path=tmp_path)
        
        assert os.path.exists(readme_path)
        
        with open(readme_path, 'r') as f:
            content = f.read()
            assert "Plugin de Optimización de Subtítulos para VLC" in content
            assert "Instalación" in content
            assert "Windows" in content
            assert "macOS" in content
            assert "Linux" in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_get_vlc_plugin_dir():
    """Test getting VLC plugin directory"""
    generator = VLCPluginGenerator()
    
    plugin_dir = generator._get_vlc_plugin_dir()
    
    # Should return a path (may not exist yet)
    assert plugin_dir is not None
    assert isinstance(plugin_dir, str)
    assert len(plugin_dir) > 0
