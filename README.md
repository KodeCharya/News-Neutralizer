# News Neutralizer - AI-Powered Bias Detection

A Streamlit application that uses AI to analyze news articles for bias, neutralize them into fact-only content, and show how the same story could be presented from different political perspectives.

## Features

- **Bias Detection**: Identifies biased language, emotional triggers, and subjective framing using AI
- **Neutralization**: Automatically rewrites articles in objective, fact-only tone
- **Multi-Perspective View**: Shows how the same article would be written from left, neutral, and right perspectives
- **Multi-LLM Support**: Works with Claude, OpenAI GPT, and Google Gemini APIs
- **Analysis History**: Saves all analyses to Supabase for later review
- **Detailed Analytics**: Shows bias score, categories of bias, and confidence levels for each detection

## Project Structure

```
├── app.py                 # Main Streamlit application
├── llm_handlers.py       # Multi-LLM provider handlers
├── database.py           # Supabase database integration
├── utils.py              # Utility functions for text processing
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (Supabase config)
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Installation

### Prerequisites
- Python 3.8+
- API key from at least one LLM provider:
  - Claude: https://console.anthropic.com
  - OpenAI: https://platform.openai.com/api-keys
  - Google Gemini: https://ai.google.dev

### Setup

1. Clone or download this project

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
The `.env` file already contains Supabase credentials. You just need to add your LLM API keys in the app itself.

5. Run the app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## How to Use

1. **Configure LLM Provider**: In the left sidebar, select your LLM provider and enter your API key
2. **Test Connection**: Click "Test Selected Provider" to verify your API key works
3. **Input Article**: Choose to paste article text directly or provide a URL for automatic extraction
4. **Analyze**: Click "Analyze Article" to start the analysis
5. **Review Results**:
   - View the original vs neutralized versions
   - See all detected biases with categories and confidence scores
   - Explore the left, right, and neutral perspective versions
6. **View History**: Access previously analyzed articles in the History tab

## Supported LLM Providers

### Claude (Anthropic)
- Latest model: claude-3-5-sonnet
- Best for: High-quality bias detection and perspective generation
- Get API key: https://console.anthropic.com

### OpenAI (GPT)
- Latest model: gpt-4-turbo
- Best for: Reliable analysis and fast processing
- Get API key: https://platform.openai.com/api-keys

### Gemini (Google)
- Model: gemini-pro
- Best for: Cost-effective analysis
- Get API key: https://ai.google.dev

## How It Works

### Bias Detection
1. Analyzes article text for biased language
2. Identifies emotional language, loaded adjectives, and subjective framing
3. Categorizes biases (emotional, political, cultural, economic)
4. Assigns confidence scores to each detected bias
5. Calculates overall bias score

### Neutralization
1. Removes emotional language and subjective framing
2. Replaces loaded words with objective alternatives
3. Eliminates political/cultural bias indicators
4. Maintains factual accuracy while removing bias

### Perspective Generation
1. **Left Perspective**: Reframes facts emphasizing social equity and systemic issues
2. **Neutral Perspective**: Pure fact-based presentation (same as neutralized version)
3. **Right Perspective**: Reframes facts emphasizing individual responsibility and traditional values

### Data Storage
- All analyses are saved to Supabase database
- Session-based access control ensures privacy
- Full analysis history with bias scores and timestamps
- Detailed bias records for each article

## Bias Categories

- **Emotional**: Loaded adjectives, emotional language, inflammatory words
- **Political**: Political framing, partisan language, ideological bias
- **Cultural**: Cultural bias, stereotypes, cultural assumptions
- **Economic**: Economic bias, class-based language
- **Other**: Other forms of bias not fitting above categories

## Temperature Settings

- **0.0**: Most deterministic, consistent results
- **0.7**: Balanced (default), good mix of consistency and creativity
- **1.5+**: Most creative, more varied responses

Lower temperatures work better for consistent bias detection. Higher temperatures can generate more varied perspective versions.

## API Costs

Different providers have different pricing structures. Check their documentation:
- Claude: https://www.anthropic.com/pricing
- OpenAI: https://openai.com/pricing
- Gemini: https://ai.google.dev/pricing

## Limitations

- Very long articles (>50,000 characters) are not supported
- Very short articles (<100 characters) are rejected
- LLM analysis quality depends on the model and provider
- Perspective generation uses the same model for consistency

## Privacy & Security

- Your API keys are only used for requests to the respective LLM providers
- API keys are not stored in the database, only in session memory
- All article analyses are stored in Supabase with session-based access control
- Each user session has isolated data access via RLS policies

## Troubleshooting

**Connection error to LLM provider**
- Verify your API key is correct
- Check that you have available API quota
- Ensure your account has permissions to access the API

**Supabase connection error**
- Check that the `.env` file has correct Supabase credentials
- Verify you have internet connection

**Article extraction failed**
- The URL might not contain readable article content
- Try pasting the article text directly instead

**Analysis quality seems poor**
- Try adjusting the temperature setting
- The article might contain primarily opinion content
- Different providers may give better results for your use case

## Future Enhancements

- Browser extension for one-click article analysis
- Support for multiple languages
- Custom bias detection rules
- Comparison mode for multiple articles
- Sharing and collaboration features
- Export analyses to PDF with detailed reports

## Contributing

Feel free to improve the project by:
- Adding support for additional LLM providers
- Enhancing bias detection prompts
- Improving UI/UX
- Adding new analysis features

## License

This project is open source and available for educational and research purposes.
