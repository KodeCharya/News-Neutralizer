import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import anthropic
import openai
import google.generativeai as genai


class LLMHandler(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def detect_biases(self, text: str, temperature: float = 0.7) -> Dict[str, Any]:
        pass

    @abstractmethod
    def neutralize_article(self, text: str, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def generate_perspective(self, text: str, perspective: str, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        pass


class ClaudeHandler(LLMHandler):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)

    def detect_biases(self, text: str, temperature: float = 0.7) -> Dict[str, Any]:
        prompt = f"""Analyze this article for biased language. Return a JSON object with:
- "biases": list of objects with "term", "replacement", "category", "confidence", "reasoning"
- "overall_score": 0-100 bias score
- "summary": brief summary of bias types found

Article:
{text}

Return ONLY valid JSON, no markdown formatting."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = message.content[0].text
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    return json.loads(result_text[start_idx:end_idx])
                raise
        except Exception as e:
            return {"error": str(e), "biases": [], "overall_score": 0}

    def neutralize_article(self, text: str, temperature: float = 0.7) -> str:
        prompt = f"""Rewrite this article in completely neutral, fact-only tone. Remove all:
- Emotional language
- Loaded adjectives
- Subjective opinions
- Political framing
- Cultural bias
- Inflammatory words

Keep only objective facts and observations.

Article:
{text}

Provide ONLY the neutralized article text, no explanations."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_perspective(self, text: str, perspective: str, temperature: float = 0.7) -> str:
        perspective_prompts = {
            "left": "Rewrite this article from a progressive/left-leaning perspective, emphasizing social equity and systemic issues",
            "right": "Rewrite this article from a conservative/right-leaning perspective, emphasizing individual responsibility and traditional values",
            "neutral": "Rewrite this article in completely neutral, fact-only tone"
        }

        prompt = f"""{perspective_prompts.get(perspective, perspective_prompts['neutral'])}

Keep the same factual content but adjust framing and emphasis.

Article:
{text}

Provide ONLY the rewritten article text."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception:
            return False


class OpenAIHandler(LLMHandler):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = openai.OpenAI(api_key=api_key)

    def detect_biases(self, text: str, temperature: float = 0.7) -> Dict[str, Any]:
        prompt = f"""Analyze this article for biased language. Return a JSON object with:
- "biases": list of objects with "term", "replacement", "category", "confidence", "reasoning"
- "overall_score": 0-100 bias score
- "summary": brief summary of bias types found

Article:
{text}

Return ONLY valid JSON, no markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.choices[0].message.content
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    return json.loads(result_text[start_idx:end_idx])
                raise
        except Exception as e:
            return {"error": str(e), "biases": [], "overall_score": 0}

    def neutralize_article(self, text: str, temperature: float = 0.7) -> str:
        prompt = f"""Rewrite this article in completely neutral, fact-only tone. Remove all:
- Emotional language
- Loaded adjectives
- Subjective opinions
- Political framing
- Cultural bias
- Inflammatory words

Keep only objective facts and observations.

Article:
{text}

Provide ONLY the neutralized article text, no explanations."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_perspective(self, text: str, perspective: str, temperature: float = 0.7) -> str:
        perspective_prompts = {
            "left": "Rewrite this article from a progressive/left-leaning perspective, emphasizing social equity and systemic issues",
            "right": "Rewrite this article from a conservative/right-leaning perspective, emphasizing individual responsibility and traditional values",
            "neutral": "Rewrite this article in completely neutral, fact-only tone"
        }

        prompt = f"""{perspective_prompts.get(perspective, perspective_prompts['neutral'])}

Keep the same factual content but adjust framing and emphasis.

Article:
{text}

Provide ONLY the rewritten article text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                max_tokens=2000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        try:
            self.client.chat.completions.create(
                model="gpt-4-turbo",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception:
            return False


class GeminiHandler(LLMHandler):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def detect_biases(self, text: str, temperature: float = 0.7) -> Dict[str, Any]:
        prompt = f"""Analyze this article for biased language. Return a JSON object with:
- "biases": list of objects with "term", "replacement", "category", "confidence", "reasoning"
- "overall_score": 0-100 bias score
- "summary": brief summary of bias types found

Article:
{text}

Return ONLY valid JSON, no markdown formatting."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2000
                )
            )

            result_text = response.text
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    return json.loads(result_text[start_idx:end_idx])
                raise
        except Exception as e:
            return {"error": str(e), "biases": [], "overall_score": 0}

    def neutralize_article(self, text: str, temperature: float = 0.7) -> str:
        prompt = f"""Rewrite this article in completely neutral, fact-only tone. Remove all:
- Emotional language
- Loaded adjectives
- Subjective opinions
- Political framing
- Cultural bias
- Inflammatory words

Keep only objective facts and observations.

Article:
{text}

Provide ONLY the neutralized article text, no explanations."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2000
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_perspective(self, text: str, perspective: str, temperature: float = 0.7) -> str:
        perspective_prompts = {
            "left": "Rewrite this article from a progressive/left-leaning perspective, emphasizing social equity and systemic issues",
            "right": "Rewrite this article from a conservative/right-leaning perspective, emphasizing individual responsibility and traditional values",
            "neutral": "Rewrite this article in completely neutral, fact-only tone"
        }

        prompt = f"""{perspective_prompts.get(perspective, perspective_prompts['neutral'])}

Keep the same factual content but adjust framing and emphasis.

Article:
{text}

Provide ONLY the rewritten article text."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2000
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        try:
            self.model.generate_content("Hi", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
            return True
        except Exception:
            return False


def get_llm_handler(provider: str, api_key: str) -> Optional[LLMHandler]:
    handlers = {
        "claude": ClaudeHandler,
        "openai": OpenAIHandler,
        "gemini": GeminiHandler
    }

    handler_class = handlers.get(provider.lower())
    if handler_class:
        return handler_class(api_key)
    return None
