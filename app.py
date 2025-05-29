import streamlit as st
from summarizer import summarize_text_to_bullets
import time

def count_words(text: str) -> int:
    """Count words in a text string"""
    return len(text.split()) if text else 0

def display_summary(bullets: list, processing_time: float):
    """Display the summary results"""
    st.success("### 3-Point Summary")
    for point in bullets:
        st.markdown(f"- {point}")
    st.caption(f"Processing time: {processing_time:.2f} seconds")

def main():
    # App configuration
    st.set_page_config(
        page_title="📝 AI Summarizer App",
        page_icon="📝",
        layout="centered"
    )
    
    st.title("📝 AI Summarizer App")
    st.markdown("""
        Paste your text (500+ words minimum) and get a concise 3-point summary.
        The app uses Facebook's BART-large-cnn model for high-quality summarization.
    """)

    # Text input area
    input_text = st.text_area(
        "Enter your long text:",
        height=300,
        placeholder="Paste your article, report, or document here (minimum 500 words)...",
        key="text_input"
    )

    # Word count display
    word_count = count_words(input_text)
    st.caption(f"Word count: {word_count} (minimum 500 required)")

    # Summarize button
    if st.button("Summarize"):
        if word_count < 500:
            st.warning("Please enter at least 500 words to summarize.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    start_time = time.time()
                    bullets = summarize_text_to_bullets(input_text)
                    processing_time = time.time() - start_time
                    display_summary(bullets, processing_time)
                except Exception as e:
                    st.error(f"An error occurred during summarization: {str(e)}")
                    st.info("Please try again with a different text.")

if __name__ == "__main__":
    main()