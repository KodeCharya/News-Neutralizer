/*
  # Create News Neutralizer Tables

  1. New Tables
    - `analyses` - Store article analyses with neutralized versions
    - `perspective_variations` - Store left/right/neutral perspectives
    - `user_preferences` - Store user settings and API key info
    - `detected_biases` - Store individual bias detections per analysis

  2. Tables Description
    - `analyses`:
      - `id` (uuid, primary key)
      - `session_id` (text) - Session identifier
      - `original_text` (text) - Original article text
      - `source_url` (text, nullable) - Source URL if provided
      - `neutralized_text` (text) - AI-neutralized version
      - `llm_provider` (text) - Which LLM was used (claude, openai, gemini)
      - `bias_score` (float) - Overall bias score 0-100
      - `total_biases_detected` (int) - Count of detected biases
      - `created_at` (timestamptz) - Timestamp of analysis

    - `perspective_variations`:
      - `id` (uuid, primary key)
      - `analysis_id` (uuid, foreign key) - Reference to analysis
      - `perspective_type` (text) - 'left', 'neutral', or 'right'
      - `generated_text` (text) - Perspective-specific version
      - `created_at` (timestamptz)

    - `detected_biases`:
      - `id` (uuid, primary key)
      - `analysis_id` (uuid, foreign key) - Reference to analysis
      - `original_term` (text) - Biased term from original
      - `neutral_term` (text) - Suggested replacement
      - `bias_category` (text) - Type of bias (emotional, political, cultural)
      - `confidence` (float) - Confidence score 0-1
      - `reasoning` (text) - Why it was flagged

    - `user_preferences`:
      - `id` (uuid, primary key)
      - `session_id` (text, unique) - Session identifier
      - `preferred_llm` (text) - Preferred LLM provider
      - `temperature` (float) - Temperature setting 0-2
      - `theme` (text) - 'light' or 'dark'
      - `updated_at` (timestamptz)

  3. Security
    - Enable RLS on all tables
    - Create policies for session-based access (all users can access their session data)
*/

CREATE TABLE IF NOT EXISTS analyses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL,
  original_text text NOT NULL,
  source_url text,
  neutralized_text text NOT NULL,
  llm_provider text NOT NULL,
  bias_score float DEFAULT 0,
  total_biases_detected int DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS perspective_variations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_id uuid NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
  perspective_type text NOT NULL CHECK (perspective_type IN ('left', 'neutral', 'right')),
  generated_text text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS detected_biases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_id uuid NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
  original_term text NOT NULL,
  neutral_term text NOT NULL,
  bias_category text NOT NULL,
  confidence float NOT NULL,
  reasoning text NOT NULL
);

CREATE TABLE IF NOT EXISTS user_preferences (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text UNIQUE NOT NULL,
  preferred_llm text DEFAULT 'claude',
  temperature float DEFAULT 0.7,
  theme text DEFAULT 'light',
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE perspective_variations ENABLE ROW LEVEL SECURITY;
ALTER TABLE detected_biases ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can access their own session analyses"
  ON analyses FOR SELECT
  USING (session_id = current_setting('app.session_id', true));

CREATE POLICY "Users can insert their own analyses"
  ON analyses FOR INSERT
  WITH CHECK (session_id = current_setting('app.session_id', true));

CREATE POLICY "Users can access variations of their analyses"
  ON perspective_variations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM analyses
      WHERE analyses.id = perspective_variations.analysis_id
      AND analyses.session_id = current_setting('app.session_id', true)
    )
  );

CREATE POLICY "Users can insert variations for their analyses"
  ON perspective_variations FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM analyses
      WHERE analyses.id = perspective_variations.analysis_id
      AND analyses.session_id = current_setting('app.session_id', true)
    )
  );

CREATE POLICY "Users can access biases from their analyses"
  ON detected_biases FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM analyses
      WHERE analyses.id = detected_biases.analysis_id
      AND analyses.session_id = current_setting('app.session_id', true)
    )
  );

CREATE POLICY "Users can insert biases for their analyses"
  ON detected_biases FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM analyses
      WHERE analyses.id = detected_biases.analysis_id
      AND analyses.session_id = current_setting('app.session_id', true)
    )
  );

CREATE POLICY "Users can access their preferences"
  ON user_preferences FOR SELECT
  USING (session_id = current_setting('app.session_id', true));

CREATE POLICY "Users can insert their preferences"
  ON user_preferences FOR INSERT
  WITH CHECK (session_id = current_setting('app.session_id', true));

CREATE POLICY "Users can update their preferences"
  ON user_preferences FOR UPDATE
  USING (session_id = current_setting('app.session_id', true))
  WITH CHECK (session_id = current_setting('app.session_id', true));

CREATE INDEX idx_analyses_session ON analyses(session_id);
CREATE INDEX idx_perspective_analysis ON perspective_variations(analysis_id);
CREATE INDEX idx_biases_analysis ON detected_biases(analysis_id);
CREATE INDEX idx_preferences_session ON user_preferences(session_id);
