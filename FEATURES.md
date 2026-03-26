# News Neutralizer - Complete Features List

## Core Functionality

### 1. Bias Detection Engine
- **Automatic Bias Identification**: Analyzes text for loaded language, emotional triggers, and subjective framing
- **Confidence Scoring**: Each detected bias receives 0-1 confidence score
- **Categorization**: Biases categorized into 5 types:
  - Emotional (loaded adjectives, inflammatory language)
  - Political (partisan framing, ideological bias)
  - Cultural (stereotypes, cultural assumptions)
  - Economic (class-based language, economic framing)
  - Other (uncategorized biases)
- **Overall Bias Score**: Aggregated 0-100 score showing article's total bias level
- **Reasoning Provided**: Each bias includes explanation of why it was flagged

### 2. Article Neutralization
- **Objective Rewriting**: Converts biased articles to fact-only tone
- **Intelligent Replacement**: Suggests neutral alternatives for biased terms
- **Fact Preservation**: Maintains all factual content while removing bias
- **Emotional Language Removal**: Eliminates loaded adjectives and inflammatory words
- **Structure Maintenance**: Keeps original article organization and flow

### 3. Multi-Perspective Generation
- **Left Perspective**: Progressive framing emphasizing:
  - Social equity and fairness
  - Systemic issues and structures
  - Community and collective solutions
  - Environmental and social justice

- **Right Perspective**: Conservative framing emphasizing:
  - Individual responsibility
  - Market-based solutions
  - Traditional values
  - Limited government role

- **Neutral Perspective**: Fact-only version
  - Pure factual presentation
  - No political framing
  - Objective language
  - Same as neutralized version

- **Comparison Mode**: View all three perspectives side-by-side

### 4. Multi-LLM Provider Support

#### Claude (Anthropic)
- Model: claude-3-5-sonnet
- Best for: Nuanced bias detection, high-quality perspective generation
- Speed: Moderate
- Cost: Standard

#### OpenAI (GPT)
- Model: gpt-4-turbo
- Best for: Reliable, consistent results
- Speed: Fast
- Cost: Standard

#### Google Gemini
- Model: gemini-pro
- Best for: Cost-effective analysis
- Speed: Fast
- Cost: Lower

**Features:**
- One-click provider switching
- API key configuration in app
- Connection testing before use
- Provider performance comparison
- Track which provider was used for each analysis

### 5. Article Input Methods

#### Direct Text Input
- Paste article text directly into app
- Support for long articles (up to 50,000 characters)
- Real-time character counting
- Input validation with helpful error messages

#### URL Extraction
- Paste any news article URL
- Automatic content extraction using web scraping
- HTML parsing and cleaning
- Removes ads, scripts, and irrelevant content
- Automatic title extraction
- Fallback support for extraction failures

#### Supported Sources
- News websites (CNN, BBC, Reuters, AP, etc.)
- Blog posts and personal articles
- Opinion pieces and editorials
- Technical articles
- Any web-based text content

### 6. Results Display

#### Original Article View
- Full original text display
- Non-editable preview
- Character count
- Source URL (if provided)

#### Neutralized Article View
- Full neutralized text display
- Side-by-side comparison option
- Download button for .txt file
- Copy to clipboard functionality
- Shows transformation from original

#### Detailed Bias Analysis
- Expandable sections by bias category
- For each bias shows:
  - Original biased term
  - Suggested neutral replacement
  - Confidence score (as percentage)
  - Category
  - Reasoning/explanation
- Summary statistics:
  - Total biases detected
  - Breakdown by category
  - Overall bias score

#### Perspective Display
- Three-column layout showing:
  - Left perspective
  - Neutral perspective
  - Right perspective
- Each in separate text area
- Side-by-side comparison
- Easy to switch between perspectives

### 7. Configuration & Settings

#### API Key Management
- Secure password fields for API keys
- Support for multiple providers simultaneously
- Key validation before use
- "Test Connection" button
- Status indicators for configured providers
- No keys stored in database (session memory only)

#### Temperature Control
- Slider from 0.0 to 2.0
- Controls model creativity/determinism:
  - 0.0: Most deterministic, consistent
  - 0.7: Default, balanced
  - 1.5+: Most creative, varied responses
- Applied to all LLM calls
- Affects both analysis and perspective generation

#### Provider Selection
- Radio button to choose active provider
- Instant switching between providers
- Independent settings per session
- Test each provider separately

#### Theme Selection
- Light mode
- Dark mode
- Persisted across sessions
- Applied to all Streamlit components

#### Preference Saving
- Automatically saves:
  - Preferred LLM provider
  - Temperature setting
  - Theme choice
- Retrieved on next session for same user
- Session-based storage

### 8. Analysis History

#### History Storage
- Automatic save of all analyses
- Stored in Supabase database
- Accessible from History tab
- 20 most recent analyses displayed by default

#### History Display
- Article preview (truncated)
- Bias score
- LLM provider used
- Creation timestamp
- View button for each

#### History Management
- Click "View" to reload analysis details
- Delete individual analyses
- Search/filter functionality (in extended version)
- Statistics tracking

#### Reloading Analysis
- Instantly loads saved analysis
- No re-analysis needed
- Displays all original results
- Can generate new perspectives if desired

### 9. Export & Sharing

#### Download Options
- Download neutralized article as .txt file
- Plain text format (no formatting)
- Automatic filename generation
- Direct browser download

#### Copy to Clipboard
- One-click copy of neutralized text
- Success confirmation message
- Paste anywhere (Word, email, etc.)

#### Data Export (Future)
- Export to Markdown
- Export to PDF with formatting
- Batch export multiple analyses
- CSV export of analysis data

### 10. Analytics & Statistics

#### Session Statistics
- Total analyses performed
- Average bias score across all analyses
- Breakdown by provider
- Provider usage comparison

#### Per-Analysis Metrics
- Bias score (0-100)
- Number of biases detected
- Bias categories present
- Average confidence score
- Provider used
- Analysis timestamp

#### Trend Tracking
- Bias scores over time
- Provider performance comparison
- Category distribution
- Source effectiveness analysis

### 11. User Interface

#### Sidebar Navigation
- **API Keys Section**: Configure providers
- **Analysis Settings**: Temperature, provider selection
- **Test Connection**: Validate API keys
- **Statistics**: Session analytics
- Clean, organized layout

#### Main Tabs
- **Analyze Article**: Input and analysis interface
- **History**: View past analyses

#### Results Tabs
- **Original**: Original article text
- **Neutralized**: Neutralized version
- **Bias Analysis**: Detailed bias breakdown
- **Perspectives**: Left/neutral/right versions

#### Visual Indicators
- Loading spinners with status messages
- Success/error notifications
- Progress indicators
- Color-coded status (green=success, red=error)

#### Responsiveness
- Mobile-friendly design
- Adapts to different screen sizes
- Works on desktop, tablet, mobile
- Optimized text sizes and buttons

### 12. Data Management

#### Supabase Integration
- Cloud database storage
- Session-based organization
- Automatic timestamp tracking
- Relational data structure

#### Data Stored
- Original article text
- Neutralized version
- Detected biases with details
- Generated perspectives
- User preferences
- Session metadata

#### Data Security
- Row Level Security (RLS) policies
- Session-based access control
- No cross-user data access
- Secure connection to Supabase

#### Data Retrieval
- Fast history loading
- Indexed database queries
- Efficient relationship loading
- Cached results where possible

### 13. Error Handling

#### Input Validation
- Article length constraints (100-50,000 chars)
- Empty content rejection
- Invalid URL detection
- Format validation

#### API Error Handling
- Invalid API key detection
- Rate limit notifications
- Connection failure messages
- Graceful fallback suggestions

#### Database Error Handling
- Connection error messages
- Data retrieval failures
- Save operation errors
- Recovery suggestions

#### User-Friendly Messages
- Clear error explanations
- Suggested solutions
- Recovery options
- No technical jargon

### 14. Performance Features

#### Caching
- Cached LLM responses
- Perspective caching to avoid regeneration
- History caching for quick loading
- Session-based cache management

#### Optimization
- Lazy loading of components
- Efficient database queries
- Streamlit cache decorators
- Minimized API calls

#### Loading States
- Visual feedback during processing
- Status messages showing progress
- Estimated wait times
- Abort capability for long operations

### 15. Advanced Features

#### Chain-of-Thought Prompting
- Multi-stage analysis process
- First: Identify biases
- Second: Categorize and score
- Third: Suggest replacements
- Results in more accurate analysis

#### Confidence Scoring
- Per-bias confidence (0-1 scale)
- Aggregate scoring
- Weighted calculations
- Normalized to 0-100 scale

#### Bias Categorization
- Automatic category assignment
- 5-category system
- Customizable categories (in extended version)
- Category-based filtering

#### Provider Comparison
- Test multiple providers on same article
- Compare results quality
- Evaluate performance differences
- Track provider-specific strengths

### 16. Scalability

#### Expandability
- Easy to add new LLM providers
- New bias categories easily added
- Customizable perspective types
- Extendable bias detection rules

#### Maintenance
- Clean, modular code architecture
- Separate concerns (handlers, database, utils)
- Well-documented functions
- Easy debugging and testing

#### Future Enhancements
- Batch processing capabilities
- API endpoint development
- Browser extension
- Mobile app
- Advanced filtering
- Collaboration features

## Summary of Capabilities

✅ **Bias Detection**: Identify 5+ types of bias with confidence scoring
✅ **Neutralization**: Convert biased to objective text automatically
✅ **Perspectives**: Show left, neutral, and right versions
✅ **Multi-LLM**: Support Claude, OpenAI, Gemini with one-click switching
✅ **URL Extraction**: Parse news articles automatically
✅ **History**: Persistent storage of all analyses
✅ **Export**: Download neutralized articles
✅ **Analytics**: Track bias scores and provider performance
✅ **Security**: Session-based access control, no API key storage
✅ **UI**: Clean, responsive Streamlit interface
✅ **Error Handling**: Comprehensive validation and user guidance
✅ **Performance**: Sub-minute analysis times, instant history retrieval

The News Neutralizer combines sophisticated AI analysis with a user-friendly interface to help identify bias in news articles and understand how different perspectives frame the same facts.
