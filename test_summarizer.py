import pytest
from summarizer import summarize_text_to_bullets, process_bullets
import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)

@pytest.fixture
def long_text():
    return " ".join(["This is a comprehensive test sentence that contains enough detail for summarization."] * 100)

def test_process_bullets():
    """Test bullet point processing"""
    test_sentences = [
        "first sentence",
        "second sentence",
        "",
        "third sentence",
        "fourth sentence"
    ]
    bullets = process_bullets(test_sentences)
    assert len(bullets) == 3
    assert bullets[0] == "First sentence."
    assert bullets[1] == "Second sentence."
    assert bullets[2] == "Third sentence."

def test_summarizer_output_format(long_text):
    """Test that output is exactly 3 bullet points"""
    bullets = summarize_text_to_bullets(long_text)
    assert isinstance(bullets, list)
    assert len(bullets) == 3
    for bullet in bullets:
        assert bullet.endswith('.')
        assert bullet[0].isupper()

def test_short_text():
    """Test with shorter text"""
    text = "The cat sat. The dog barked. The bird flew. The fish swam."
    bullets = summarize_text_to_bullets(text)
    assert len(bullets) == 3

def test_error_handling(monkeypatch):
    """Test error handling when model fails"""
    def mock_summarizer(*args, **kwargs):
        raise Exception("Mock error")
    
    monkeypatch.setattr("summarizer.summarizer", mock_summarizer)
    with pytest.raises(RuntimeError):
        summarize_text_to_bullets("test text")