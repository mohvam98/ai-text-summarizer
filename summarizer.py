from transformers import pipeline
from typing import List
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_summarizer():
    """Initialize the summarization pipeline with appropriate device settings."""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing summarizer on device: {device}")
        return pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            framework="pt",
            device=device
        )
    except Exception as e:
        logger.error(f"Failed to initialize summarizer: {str(e)}")
        raise

# Global summarizer instance
summarizer = initialize_summarizer()

def process_bullets(sentences: List[str]) -> List[str]:
    """Process sentences into properly formatted bullet points"""
    bullets = []
    for sentence in sentences:
        if len(bullets) >= 3:
            break
            
        # Clean up the sentence
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Ensure proper punctuation
        if not sentence.endswith('.'):
            sentence += '.'
            
        # Capitalize first letter
        sentence = sentence[0].upper() + sentence[1:]
        bullets.append(sentence)
    
    # Ensure we have exactly 3 bullets
    while len(bullets) < 3:
        bullets.append("Could not generate full summary.")
        
    return bullets[:3]

def summarize_text_to_bullets(text: str) -> List[str]:
    """
    Summarize text into 3 bullet points.
    
    Args:
        text: Input text to summarize (500+ words recommended)
        
    Returns:
        List of 3 bullet point summaries
        
    Raises:
        RuntimeError: If summarization fails
    """
    try:
        logger.info("Starting summarization...")
        
        # Generate initial summary
        result = summarizer(
            text,
            max_length=300,
            min_length=100,
            do_sample=False,
            truncation=True
        )
        
        # Split into sentences
        full_summary = result[0]["summary_text"]
        sentences = [s.strip() for s in full_summary.split(". ") if s.strip()]
        
        # Process into bullet points
        return process_bullets(sentences)
        
    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise RuntimeError("Failed to generate summary. Please try again.")