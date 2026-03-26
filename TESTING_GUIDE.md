# Testing Guide - News Neutralizer

Complete testing instructions for validating the News Neutralizer application.

## Pre-Testing Setup

1. **Get API Keys**
   - Claude: https://console.anthropic.com
   - OpenAI: https://platform.openai.com/api-keys
   - Gemini: https://ai.google.dev

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the App**
   ```bash
   streamlit run app.py
   ```

4. **Verify Supabase Connection**
   - Sidebar shows no errors
   - Database connectivity works on first analysis

## Test Scenarios

### Test 1: API Key Configuration

**Steps:**
1. Open app in browser
2. Look at sidebar "API Keys" section
3. Enter Claude API key
4. Click "Test Selected Provider"

**Expected Results:**
- ✅ "Connection successful" message appears
- ✅ API key is masked in input field
- ✅ No data is sent to server except test request

**Test Other Providers:**
- Repeat for OpenAI API key
- Repeat for Gemini API key

---

### Test 2: Text Article Input

**Test Case 2a: Valid Article**

**Input:**
```
Apple announced a revolutionary new iPhone with groundbreaking AI capabilities
that experts say will dominate the market. Competitors struggle to keep up
with Apple's blazing-fast innovation pace. The spectacular features include
advanced neural processing and game-changing design elements.
```

**Expected Results:**
- ✅ Article accepted (>100 characters)
- ✅ "Analyze Article" button clickable
- ✅ Analysis completes in 30-60 seconds
- ✅ Bias score > 40 (lots of adjectives)

**Test Case 2b: Too Short**

**Input:** "Apple is good."

**Expected Results:**
- ❌ Error: "Article must be at least 100 characters long"

**Test Case 2c: Empty**

**Input:** (blank)

**Expected Results:**
- ❌ Error: "Article text cannot be empty"

---

### Test 3: URL Extraction

**Test Case 3a: Valid News URL**

**URL:** Any news article (BBC, CNN, Reuters, etc.)

**Steps:**
1. Paste URL in URL field
2. Click "Extract from URL"
3. Wait 5-10 seconds

**Expected Results:**
- ✅ Article text appears in text area
- ✅ Confirms extraction with success message
- ✅ Extracted text > 100 characters

**Test Case 3b: Invalid URL**

**URL:** `https://invalid-domain-12345.com/article`

**Expected Results:**
- ❌ Error message explaining extraction failed
- ✅ Can still paste text directly

---

### Test 4: Bias Detection

**Steps:**
1. Input a biased political article
2. Click "Analyze Article"
3. Navigate to "Bias Analysis" tab
4. Examine detected biases

**Test Article (Use this for consistent results):**
```
The incompetent Democrats rammed through yet another wasteful spending bill,
ignoring the hard-working taxpayers who will suffer the devastating consequences.
The bleeding-heart liberals refuse to acknowledge the catastrophic government overreach.
Meanwhile, courageous Republicans continue fighting for our fundamental freedoms against
the relentless onslaught of socialist policies threatening our great nation.
```

**Expected Results:**
- ✅ Bias score: 75+ (very biased)
- ✅ >10 biases detected
- ✅ Categories include: emotional, political
- ✅ Examples detected:
  - "incompetent" → neutral term
  - "bleeding-heart liberals" → neutral term
  - "devastating" → neutral term
  - "courageous Republicans" → "Republicans"
- ✅ Confidence scores: 0.7-0.99 for most
- ✅ Each bias has reasoning

---

### Test 5: Neutralization Quality

**Steps:**
1. Use same biased article as Test 4
2. Go to "Neutralized" tab
3. Compare original vs neutralized

**Expected Neutralized Output (example):**
```
The Democrats passed a spending bill. The legislation generated debate among Republicans
and Democrats regarding government spending. Republicans opposed the bill citing concerns
about fiscal responsibility. The bill became law.
```

**Expected Results:**
- ✅ Removed adjectives: incompetent, wasteful, devastating, courageous
- ✅ Removed emotional language: bleeding-heart, relentless onslaught
- ✅ Preserved facts about the bill
- ✅ Maintained article structure
- ✅ Significantly lower bias score (10-20)

---

### Test 6: Perspective Generation

**Steps:**
1. Use same article from Test 4
2. Go to "Perspectives" tab
3. Wait for all three perspectives to generate

**Expected Results:**

**Left Perspective Should:**
- ✅ Emphasize social concerns
- ✅ Focus on equity and inclusion
- ✅ Mention helping vulnerable groups
- ✅ Support government programs

**Right Perspective Should:**
- ✅ Emphasize individual responsibility
- ✅ Focus on market solutions
- ✅ Mention fiscal restraint
- ✅ Critique government overreach

**Neutral Perspective Should:**
- ✅ Match the neutralized version
- ✅ Contain only facts
- ✅ No emotional language
- ✅ No political framing

---

### Test 7: History & Database Integration

**Steps:**
1. Analyze 3 different articles
2. Go to "History" tab
3. Verify all 3 appear

**Expected Results:**
- ✅ All 3 articles listed with preview
- ✅ Bias scores displayed
- ✅ Provider names shown (Claude/OpenAI/Gemini)
- ✅ Can click "View" to reload results
- ✅ Results load instantly from database

**Database Verification:**
- Check that data persists after refresh
- Close browser completely
- Reopen app
- History still shows

---

### Test 8: Provider Switching

**Steps:**
1. Analyze article with Claude
2. Switch to OpenAI in sidebar
3. Analyze same article
4. Switch to Gemini
5. Analyze same article

**Expected Results:**
- ✅ Each produces slightly different results
- ✅ All produce valid analysis
- ✅ Bias scores similar (±5-10%)
- ✅ Detected biases similar
- ✅ Perspectives show different emphasis
- ✅ History shows 3 entries, each with correct provider

---

### Test 9: Temperature Settings

**Steps:**
1. Set temperature to 0.0
2. Analyze article twice (perspectives)
3. Compare results (should be nearly identical)
4. Set temperature to 1.5
5. Analyze same article twice (perspectives)
6. Compare results (should differ more)

**Expected Results:**
- ✅ Low temp (0.0): Very consistent results
- ✅ Mid temp (0.7): Balanced consistency
- ✅ High temp (1.5): More variation in wording
- ✅ Bias detection consistent regardless of temp

---

### Test 10: Export Functionality

**Steps:**
1. Analyze an article
2. Go to "Neutralized" tab
3. Click "Download Neutralized"
4. Click "Copy to Clipboard"

**Expected Results:**
- ✅ File downloads as neutralized_article.txt
- ✅ File contains full neutralized text
- ✅ Copy button shows success message
- ✅ Text actually copies (test by pasting)

---

### Test 11: Statistics & Analytics

**Steps:**
1. Analyze 5 articles with different providers
2. Check sidebar "Statistics" section

**Expected Results:**
- ✅ Total Analyses: 5
- ✅ Average Bias Score: Calculated correctly
- ✅ By Provider breakdown:
   - Shows count for each provider used
   - Totals add up to 5
- ✅ Updates in real-time after new analysis

---

### Test 12: Error Handling

**Test Case 12a: Invalid API Key**
- Enter wrong Claude API key
- Try to analyze article
- Expected: Error message with explanation

**Test Case 12b: Network Interruption**
- Disconnect internet
- Try to analyze
- Expected: Clear error message

**Test Case 12c: Very Long Article**
- Use article with 51,000+ characters
- Try to analyze
- Expected: Error "Article is too long"

**Test Case 12d: Non-English Article**
- Use article in French/Spanish/other language
- Analyze
- Expected: Some results may vary, but should work

---

### Test 13: UI/UX Testing

**Steps:**
1. Check sidebar visibility
2. Test all tabs navigation
3. Verify button responsiveness
4. Check for loading spinners
5. Verify all text is readable

**Expected Results:**
- ✅ Sidebar always visible
- ✅ All buttons respond instantly
- ✅ Loading spinners show during processing
- ✅ All text readable (good contrast)
- ✅ Layout responsive (try resizing browser)

---

### Test 14: Session Management

**Steps:**
1. Analyze article in Tab A of browser
2. Open app in new Tab B
3. Analyze different article in Tab B
4. Return to Tab A
5. Refresh Tab A

**Expected Results:**
- ✅ Each tab has separate session ID
- ✅ Tab A shows original analysis after refresh
- ✅ Tab B shows different analysis
- ✅ No data leakage between sessions

---

### Test 15: Download & Export Quality

**Steps:**
1. Analyze article
2. Download neutralized version
3. Open downloaded file
4. Verify formatting and content

**Expected Results:**
- ✅ File opens correctly
- ✅ No HTML tags or formatting
- ✅ Plain text only
- ✅ All content readable
- ✅ Filename includes timestamp or identifier

---

## Automated Test Data

If you want to test without creating data, use these pre-made test articles:

**Test Article 1: Moderate Bias**
```
The government announced a new economic policy that supporters say will boost growth,
while critics argue it unfairly favors corporations. The initiative includes tax cuts
for businesses and reduced regulations. Proponents believe this will create jobs,
whereas opponents claim it will increase inequality.
```
Expected Bias Score: 30-40

**Test Article 2: High Bias (Conservative)**
```
Radical leftists are trying to destroy America with their extreme socialist agenda.
Their failed policies will bankrupt our nation and destroy jobs. We need patriots
to fight back against this assault on our fundamental freedoms and traditional values.
```
Expected Bias Score: 80+

**Test Article 3: High Bias (Liberal)**
```
The greedy corporations and their Republican enablers are gutting environmental protections
to fill their pockets. Their heartless policies devastate vulnerable communities and accelerate
climate catastrophe. We must resist this moral outrage and build a just, sustainable future.
```
Expected Bias Score: 80+

**Test Article 4: Low Bias**
```
A study by researchers at University X found that vitamin D supplementation may help
reduce the risk of certain infections. The research involved 5,000 participants over
two years. The findings support previous research suggesting vitamin D plays a role
in immune function.
```
Expected Bias Score: <20

---

## Success Criteria

The application passes testing if:

1. ✅ **Functionality**: All features work as described
2. ✅ **Accuracy**: Bias detection identifies 80%+ of obvious biases
3. ✅ **Performance**: Analysis completes in <90 seconds
4. ✅ **Reliability**: No crashes or unhandled errors
5. ✅ **Security**: API keys never exposed or logged
6. ✅ **Data Persistence**: History survives app restart
7. ✅ **UI/UX**: Intuitive and responsive interface
8. ✅ **Provider Support**: All three LLMs work correctly

---

## Troubleshooting During Testing

**App won't start:**
```bash
pip install -r requirements.txt --upgrade
streamlit run app.py --logger.level=debug
```

**Database error:**
- Check .env file has correct Supabase credentials
- Verify internet connection
- Check Supabase dashboard for errors

**LLM connection fails:**
- Verify API key is correct
- Check you have available API quota
- Try different provider

**Article extraction fails:**
- Website might block requests
- Try pasting text directly
- Use different URL

**Slow performance:**
- Large articles take longer (normal)
- Check internet connection
- Streamlit refresh might be slow (reload page)

---

## Performance Benchmarks

Target performance for this application:

| Operation | Target Time | Acceptable Range |
|-----------|------------|------------------|
| API key test | <5s | <10s |
| URL extraction | 5-10s | <20s |
| Bias detection | 20-40s | <60s |
| Neutralization | 15-30s | <60s |
| Left perspective | 15-30s | <60s |
| Right perspective | 15-30s | <60s |
| History load | <1s | <5s |
| Analysis details load | <1s | <5s |

---

## Test Coverage Summary

- ✅ Configuration & Settings (Test 1, 9)
- ✅ Input Validation (Test 2, 3)
- ✅ Core Analysis (Test 4, 5, 6)
- ✅ Provider Integration (Test 8)
- ✅ Data Persistence (Test 7, 14)
- ✅ Export & Download (Test 10, 15)
- ✅ Error Handling (Test 12)
- ✅ UI/UX (Test 13)
- ✅ Analytics (Test 11)

This comprehensive test suite validates all major features and edge cases of the News Neutralizer application.
