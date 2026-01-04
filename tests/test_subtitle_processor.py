"""
Tests for subtitle processor module
"""
import pytest
import os
import tempfile
from datetime import timedelta
from subtitle_processor import (
    SubtitleEntry,
    SubtitleProcessor,
    process_subtitle_file
)


def test_subtitle_entry_creation():
    """Test creating a valid subtitle entry"""
    entry = SubtitleEntry(
        index=1,
        start_time=timedelta(seconds=0),
        end_time=timedelta(seconds=2),
        text="Hola mundo"
    )
    
    assert entry.index == 1
    assert entry.duration == timedelta(seconds=2)
    assert entry.text == "Hola mundo"


def test_subtitle_entry_invalid_timing():
    """Test that invalid timing raises error"""
    with pytest.raises(ValueError):
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=2),
            end_time=timedelta(seconds=1),  # End before start
            text="Test"
        )


def test_subtitle_entry_empty_text():
    """Test that empty text raises error"""
    with pytest.raises(ValueError):
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text="   "  # Only whitespace
        )


def test_subtitle_entry_to_srt():
    """Test conversion to SRT format"""
    entry = SubtitleEntry(
        index=1,
        start_time=timedelta(seconds=0, milliseconds=0),
        end_time=timedelta(seconds=2, milliseconds=500),
        text="Texto de prueba"
    )
    
    srt = entry.to_srt()
    assert "1\n" in srt
    assert "00:00:00,000 --> 00:00:02,500" in srt
    assert "Texto de prueba" in srt


def test_subtitle_entry_to_vtt():
    """Test conversion to VTT format"""
    entry = SubtitleEntry(
        index=1,
        start_time=timedelta(seconds=0, milliseconds=0),
        end_time=timedelta(seconds=2, milliseconds=500),
        text="Texto de prueba"
    )
    
    vtt = entry.to_vtt()
    assert "00:00:00.000 --> 00:00:02.500" in vtt
    assert "Texto de prueba" in vtt


def test_parse_srt_time():
    """Test SRT time parsing"""
    time_str = "00:01:23,456"
    td = SubtitleProcessor._parse_srt_time(time_str)
    
    assert td.seconds == 83  # 1 minute 23 seconds
    assert td.microseconds == 456000  # 456 milliseconds


def test_parse_vtt_time():
    """Test VTT time parsing"""
    time_str = "00:01:23.456"
    td = SubtitleProcessor._parse_vtt_time(time_str)
    
    assert td.seconds == 83
    assert td.microseconds == 456000


def test_parse_ass_time():
    """Test ASS time parsing"""
    time_str = "0:01:23.45"
    td = SubtitleProcessor._parse_ass_time(time_str)
    
    assert td.seconds == 83
    assert td.microseconds == 450000  # 45 centiseconds = 450 ms


def test_clean_ass_text():
    """Test cleaning ASS formatting tags"""
    text = "{\\i1}Texto en cursiva{\\i0}\\NNueva línea"
    cleaned = SubtitleProcessor._clean_ass_text(text)
    
    assert "{\\i1}" not in cleaned
    assert "Texto en cursiva" in cleaned
    assert "\n" in cleaned


def test_subtitle_processor_parse_srt():
    """Test parsing a simple SRT file"""
    srt_content = """1
00:00:00,000 --> 00:00:02,000
Primera línea

2
00:00:02,500 --> 00:00:05,000
Segunda línea
"""
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        f.write(srt_content)
        tmp_path = f.name
    
    try:
        processor = SubtitleProcessor()
        success = processor.load_from_file(tmp_path)
        
        assert success
        assert len(processor.subtitles) == 2
        assert processor.subtitles[0].text == "Primera línea"
        assert processor.subtitles[1].text == "Segunda línea"
    finally:
        os.unlink(tmp_path)


def test_subtitle_processor_parse_vtt():
    """Test parsing a simple VTT file"""
    vtt_content = """WEBVTT

00:00:00.000 --> 00:00:02.000
Primera línea

00:00:02.500 --> 00:00:05.000
Segunda línea
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False) as f:
        f.write(vtt_content)
        tmp_path = f.name
    
    try:
        processor = SubtitleProcessor()
        success = processor.load_from_file(tmp_path)
        
        assert success
        assert len(processor.subtitles) == 2
    finally:
        os.unlink(tmp_path)


def test_validate_duration_too_short():
    """Test validation detects subtitles that are too short"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(milliseconds=300),  # Too short
            text="Test"
        )
    ]
    
    issues = processor.validate()
    
    assert len(issues) > 0
    assert any(i['type'] == 'duration_too_short' for i in issues)


def test_validate_duration_too_long():
    """Test validation detects subtitles that are too long"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=10),  # Too long
            text="Test"
        )
    ]
    
    issues = processor.validate()
    
    assert len(issues) > 0
    assert any(i['type'] == 'duration_too_long' for i in issues)


def test_validate_overlap():
    """Test validation detects overlapping subtitles"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=3),
            text="First"
        ),
        SubtitleEntry(
            index=2,
            start_time=timedelta(seconds=2),  # Overlaps with first
            end_time=timedelta(seconds=4),
            text="Second"
        )
    ]
    
    issues = processor.validate()
    
    assert len(issues) > 0
    assert any(i['type'] == 'overlap' for i in issues)


def test_validate_too_many_lines():
    """Test validation detects too many lines"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text="Línea 1\nLínea 2\nLínea 3"  # Too many lines
        )
    ]
    
    issues = processor.validate()
    
    assert len(issues) > 0
    assert any(i['type'] == 'too_many_lines' for i in issues)


def test_validate_line_too_long():
    """Test validation detects lines that are too long"""
    processor = SubtitleProcessor()
    long_text = "A" * 50  # More than MAX_CHARS_PER_LINE
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text=long_text
        )
    ]
    
    issues = processor.validate()
    
    assert len(issues) > 0
    assert any(i['type'] == 'line_too_long' for i in issues)


def test_optimize_fix_overlaps():
    """Test optimization fixes overlaps"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=3),
            text="First"
        ),
        SubtitleEntry(
            index=2,
            start_time=timedelta(seconds=2),
            end_time=timedelta(seconds=4),
            text="Second"
        )
    ]
    
    changes = processor.optimize(fix_overlaps=True)
    
    assert changes > 0
    # After optimization, first subtitle should end before second starts
    assert processor.subtitles[0].end_time <= processor.subtitles[1].start_time


def test_optimize_fix_short_durations():
    """Test optimization extends short durations"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(milliseconds=300),  # Too short
            text="Test"
        )
    ]
    
    changes = processor.optimize(fix_durations=True)
    
    assert changes > 0
    duration_ms = processor.subtitles[0].duration.total_seconds() * 1000
    assert duration_ms >= processor.MIN_DURATION_MS


def test_optimize_split_long_lines():
    """Test optimization splits long lines"""
    processor = SubtitleProcessor()
    long_text = "Esta es una línea muy larga que debería ser dividida en múltiples líneas más cortas"
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=3),
            text=long_text
        )
    ]
    
    changes = processor.optimize(split_long_lines=True)
    
    # Should have been split into multiple lines
    lines = processor.subtitles[0].text.split('\n')
    assert len(lines) > 1
    # Each line should be under the limit
    for line in lines:
        assert len(line) <= processor.MAX_CHARS_PER_LINE


def test_get_stats():
    """Test getting statistics from subtitles"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text="First"
        ),
        SubtitleEntry(
            index=2,
            start_time=timedelta(seconds=3),
            end_time=timedelta(seconds=5),
            text="Second"
        )
    ]
    
    stats = processor.get_stats()
    
    assert stats['total'] == 2
    assert stats['avg_duration'] == 2000  # 2 seconds in ms
    assert stats['min_duration'] == 2000
    assert stats['max_duration'] == 2000


def test_save_to_srt():
    """Test saving subtitles to SRT format"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text="Texto de prueba"
        )
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        tmp_path = f.name
    
    try:
        success = processor.save_to_file(tmp_path, format='srt')
        assert success
        
        # Verify file exists and has content
        assert os.path.exists(tmp_path)
        with open(tmp_path, 'r') as f:
            content = f.read()
            assert "1\n" in content
            assert "Texto de prueba" in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_save_to_vtt():
    """Test saving subtitles to VTT format"""
    processor = SubtitleProcessor()
    processor.subtitles = [
        SubtitleEntry(
            index=1,
            start_time=timedelta(seconds=0),
            end_time=timedelta(seconds=2),
            text="Texto de prueba"
        )
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False) as f:
        tmp_path = f.name
    
    try:
        success = processor.save_to_file(tmp_path, format='vtt')
        assert success
        
        with open(tmp_path, 'r') as f:
            content = f.read()
            assert "WEBVTT" in content
            assert "Texto de prueba" in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_process_subtitle_file_convenience_function():
    """Test the convenience function for processing files"""
    srt_content = """1
00:00:00,000 --> 00:00:00,300
Muy corto

2
00:00:01,000 --> 00:00:03,000
Normal
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        f.write(srt_content)
        input_path = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
        output_path = f.name
    
    try:
        success, results = process_subtitle_file(
            input_path,
            output_path,
            validate=True,
            optimize=True
        )
        
        assert success
        assert results['loaded']
        assert len(results['validation_issues']) > 0  # Should detect short duration
        assert results['optimization_changes'] > 0  # Should fix it
        assert results['saved']
    finally:
        if os.path.exists(input_path):
            os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
