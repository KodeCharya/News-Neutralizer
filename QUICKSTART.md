# Quick Start Guide - News Neutralizer

Get the News Neutralizer up and running in 5 minutes!

## Step 1: Get an API Key (Choose One)

Pick your preferred LLM provider:

### Option A: Claude (Recommended)
1. Go to https://console.anthropic.com
2. Click "API Keys" in the sidebar
3. Click "Create Key"
4. Copy the key

### Option B: OpenAI
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key

### Option C: Google Gemini
1. Go to https://ai.google.dev
2. Click "Get API Key"
3. Create a new API key in Google Cloud Console
4. Copy the key

## Step 2: Install & Run

```bash
# Clone/download the project
cd news-neutralizer

# Install Python dependencies (requires Python 3.8+)
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at: http://localhost:8501

## Step 3: Configure in App

1. In the **left sidebar**, find "API Keys"
2. Paste your API key in the appropriate field
3. Click the **"Test Selected Provider"** button
4. You should see: ✅ Connection successful!

## Step 4: Analyze Your First Article

1. Choose **"Paste Text"** or **"URL"** in the main area
2. Either:
   - Paste article text directly, OR
   - Paste a URL and click "Extract from URL"
3. Click **"Analyze Article"** (blue button)
4. Wait 30-60 seconds for analysis
5. View results in the tabs:
   - 📰 **Original** - See the original article
   - ✅ **Neutralized** - See the AI-neutralized version
   - 🔍 **Bias Analysis** - See detected biased words
   - 🔄 **Perspectives** - See left/neutral/right versions

## Common Issues & Fixes

### "API Key Invalid"
- Copy the key again carefully (no extra spaces)
- Make sure you're on the right provider's page
- Check that the API key hasn't expired

### "Article extraction failed"
- Website might block automated access
- Try pasting the text directly instead
- Ensure article has at least 100 characters

### "Analysis is taking too long"
- Large articles take longer (normal)
- Check your internet connection
- Ensure API provider isn't rate-limited

## Tips

- **Temperature Setting**: Keep at 0.7 (default) for consistent bias detection
- **Longer Articles**: Work better for accurate bias detection
- **URL vs Paste**: Pasting directly is always more reliable
- **History Tab**: View all your past analyses anytime

## What to Try

### Example 1: News Article
Paste a news article about a political topic and see:
- What words are flagged as biased
- How a neutral version differs
- How the same story could be told from different angles

### Example 2: Opinion Piece
Try an opinion column to see how the app handles highly subjective content

### Example 3: Technical Article
Use a technical article to see how the app preserves facts while removing bias

## Next Steps

- Read the full README.md for advanced features
- Try different LLM providers to compare results
- Adjust temperature (0.0-2.0) to see different results
- View your analysis history anytime in the History tab
- Download neutralized articles for later use

## Need Help?

Check README.md for:
- Detailed feature explanations
- How bias detection works
- Understanding perspective variations
- Privacy and security info
- Troubleshooting guide
