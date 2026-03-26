import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from llm_handlers import get_llm_handler
from database import SupabaseDB
from utils import (
    extract_article_from_url,
    validate_article_text,
    calculate_bias_score,
    categorize_biases,
    truncate_text
)

load_dotenv()

st.set_page_config(
    page_title="News Neutralizer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.db = SupabaseDB()
    st.session_state.api_keys = {
        "claude": "",
        "openai": "",
        "gemini": ""
    }

db = st.session_state.db

def setup_sidebar():
    """Setup sidebar with API keys and settings"""
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.subheader("API Keys")
        api_keys = {}
        providers = ["Claude", "OpenAI", "Gemini"]
        for provider in providers:
            provider_key = provider.lower()
            api_keys[provider_key] = st.text_input(
                f"{provider} API Key",
                value=st.session_state.api_keys.get(provider_key, ""),
                type="password",
                key=f"key_{provider_key}"
            )
            st.session_state.api_keys[provider_key] = api_keys[provider_key]

        st.divider()

        st.subheader("Analysis Settings")
        selected_provider = st.radio(
            "Select LLM Provider",
            options=["claude", "openai", "gemini"],
            format_func=lambda x: x.capitalize()
        )

        temperature = st.slider(
            "Temperature (Creativity)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Lower = more deterministic, Higher = more creative"
        )

        theme = st.radio("Theme", options=["Light", "Dark"], index=0)

        st.session_state.preferred_llm = selected_provider
        st.session_state.temperature = temperature
        st.session_state.theme = theme.lower()

        db.save_preference(
            st.session_state.session_id,
            selected_provider,
            temperature,
            theme.lower()
        )

        st.divider()

        st.subheader("Test Connection")
        if st.button("🔗 Test Selected Provider"):
            api_key = api_keys.get(selected_provider, "")
            if not api_key:
                st.warning(f"Please enter {selected_provider.upper()} API key first")
            else:
                with st.spinner(f"Testing {selected_provider.upper()} connection..."):
                    handler = get_llm_handler(selected_provider, api_key)
                    if handler and handler.test_connection():
                        st.success(f"✅ {selected_provider.upper()} connection successful!")
                    else:
                        st.error(f"❌ Failed to connect to {selected_provider.upper()}")

        st.divider()

        st.subheader("Statistics")
        stats = db.get_statistics(st.session_state.session_id)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Analyses", stats["total"])
        with col2:
            st.metric("Avg Bias Score", f"{stats['avg_bias']:.1f}")

        if stats["by_provider"]:
            st.write("**By Provider:**")
            for provider, count in stats["by_provider"].items():
                st.write(f"- {provider.capitalize()}: {count}")


def analyze_article(text: str, provider: str, api_key: str):
    """Perform bias analysis on article"""
    is_valid, error_msg = validate_article_text(text)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        return None

    with st.spinner("🔄 Analyzing article..."):
        handler = get_llm_handler(provider, api_key)
        if not handler:
            st.error(f"❌ Invalid provider: {provider}")
            return None

        try:
            biases_data = handler.detect_biases(text, st.session_state.temperature)

            if "error" in biases_data:
                st.error(f"❌ Analysis error: {biases_data['error']}")
                return None

            biases = biases_data.get("biases", [])
            bias_score = biases_data.get("overall_score", calculate_bias_score(biases))

            with st.spinner("⚙️ Neutralizing article..."):
                neutralized = handler.neutralize_article(text, st.session_state.temperature)

            analysis_id = db.save_analysis(
                session_id=st.session_state.session_id,
                original_text=text,
                neutralized_text=neutralized,
                llm_provider=provider,
                bias_score=bias_score,
                total_biases=len(biases)
            )

            if analysis_id and biases:
                db.save_detected_biases(analysis_id, biases)

            return {
                "id": analysis_id,
                "original": text,
                "neutralized": neutralized,
                "biases": biases,
                "bias_score": bias_score,
                "provider": provider
            }

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            return None


def display_analysis_results(analysis: dict):
    """Display analysis results"""
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bias Score", f"{analysis['bias_score']:.1f}/100")
    with col2:
        st.metric("Biases Found", len(analysis["biases"]))
    with col3:
        st.metric("Provider", analysis["provider"].upper())

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📰 Original",
        "✅ Neutralized",
        "🔍 Bias Analysis",
        "🔄 Perspectives"
    ])

    with tab1:
        st.write("### Original Article")
        st.text_area("Original Text", value=analysis["original"], height=300, disabled=True)

    with tab2:
        st.write("### Neutralized Article")
        st.text_area("Neutralized Text", value=analysis["neutralized"], height=300, disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Neutralized",
                data=analysis["neutralized"],
                file_name="neutralized_article.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.success("Copied to clipboard!")

    with tab3:
        st.write("### Detected Biases")

        if not analysis["biases"]:
            st.info("✅ No significant biases detected in this article.")
        else:
            categorized = categorize_biases(analysis["biases"])

            for category, biases in categorized.items():
                with st.expander(f"**{category.capitalize()}** ({len(biases)} found)"):
                    for i, bias in enumerate(biases, 1):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**{i}. Original Term:**")
                            st.code(bias.get("term", ""), language="text")
                        with col2:
                            st.write(f"**Neutral Alternative:**")
                            st.code(bias.get("replacement", ""), language="text")

                        st.write(f"**Confidence:** {bias.get('confidence', 0.5):.1%}")
                        st.write(f"**Reasoning:** {bias.get('reasoning', 'N/A')}")
                        st.divider()

    with tab4:
        st.write("### Perspective Variations")

        perspective_col1, perspective_col2, perspective_col3 = st.columns(3)

        perspectives_data = {}

        with perspective_col1:
            st.write("### 🔴 Left Perspective")
            with st.spinner("Generating left perspective..."):
                handler = get_llm_handler(analysis["provider"], st.session_state.api_keys.get(analysis["provider"], ""))
                if handler:
                    left_text = handler.generate_perspective(analysis["original"], "left", st.session_state.temperature)
                    perspectives_data["left"] = left_text

                    if analysis["id"]:
                        db.save_perspective(analysis["id"], "left", left_text)

                    st.text_area("Left Perspective", value=left_text, height=200, disabled=True, key="left_per")

        with perspective_col2:
            st.write("### ⚪ Neutral Perspective")
            st.text_area("Neutral Perspective", value=analysis["neutralized"], height=200, disabled=True, key="neutral_per")

        with perspective_col3:
            st.write("### 🔵 Right Perspective")
            with st.spinner("Generating right perspective..."):
                handler = get_llm_handler(analysis["provider"], st.session_state.api_keys.get(analysis["provider"], ""))
                if handler:
                    right_text = handler.generate_perspective(analysis["original"], "right", st.session_state.temperature)
                    perspectives_data["right"] = right_text

                    if analysis["id"]:
                        db.save_perspective(analysis["id"], "right", right_text)

                    st.text_area("Right Perspective", value=right_text, height=200, disabled=True, key="right_per")


def main():
    st.title("⚖️ News Neutralizer")
    st.markdown("Transform biased news articles into neutral, fact-based content using AI")

    setup_sidebar()

    main_tab1, main_tab2 = st.tabs(["📝 Analyze Article", "📚 History"])

    with main_tab1:
        st.header("Article Input")

        input_method = st.radio("Choose input method:", ["Paste Text", "URL"])

        article_text = None
        source_url = None

        if input_method == "Paste Text":
            article_text = st.text_area(
                "Paste article text here:",
                height=300,
                placeholder="Enter the article you want to neutralize..."
            )
        else:
            source_url = st.text_input(
                "Enter article URL:",
                placeholder="https://example.com/article"
            )

            if st.button("🔗 Extract from URL"):
                if source_url:
                    with st.spinner("Extracting article..."):
                        extracted_text, title = extract_article_from_url(source_url)
                        if extracted_text:
                            st.success(f"✅ Extracted: {truncate_text(title, 50)}")
                            article_text = extracted_text
                            st.session_state.extracted_text = extracted_text
                        else:
                            st.error("❌ Failed to extract article. Try pasting directly.")

            if "extracted_text" in st.session_state:
                article_text = st.text_area(
                    "Extracted content:",
                    value=st.session_state.extracted_text,
                    height=300
                )

        if st.button("🚀 Analyze Article", type="primary"):
            provider = st.session_state.preferred_llm
            api_key = st.session_state.api_keys.get(provider, "")

            if not api_key:
                st.error(f"❌ Please enter {provider.upper()} API key in settings")
            elif not article_text:
                st.error("❌ Please enter or extract article text")
            else:
                analysis = analyze_article(article_text, provider, api_key)
                if analysis:
                    st.session_state.current_analysis = analysis
                    st.success("✅ Analysis complete!")

        if "current_analysis" in st.session_state:
            display_analysis_results(st.session_state.current_analysis)

    with main_tab2:
        st.header("Analysis History")

        history = db.get_analysis_history(st.session_state.session_id)

        if not history:
            st.info("No analyses yet. Start by analyzing an article!")
        else:
            for analysis in history:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    preview = truncate_text(analysis["original_text"], 100)
                    st.write(f"**{preview}**")

                with col2:
                    st.write(f"📊 {analysis['bias_score']:.0f}")

                with col3:
                    st.write(f"🤖 {analysis['llm_provider'].upper()}")

                with col4:
                    if st.button("🔍 View", key=f"view_{analysis['id']}"):
                        details = db.get_analysis_details(analysis["id"])
                        if details:
                            st.session_state.current_analysis = {
                                "id": details["id"],
                                "original": details["original_text"],
                                "neutralized": details["neutralized_text"],
                                "biases": details["biases"],
                                "bias_score": details["bias_score"],
                                "provider": details["llm_provider"]
                            }
                            st.rerun()

                st.divider()


if __name__ == "__main__":
    main()
