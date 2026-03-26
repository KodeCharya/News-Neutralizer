import os
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
import json


class SupabaseDB:
    def __init__(self):
        url = os.getenv("VITE_SUPABASE_URL")
        key = os.getenv("VITE_SUPABASE_ANON_KEY")
        self.client: Client = create_client(url, key)

    def set_session_id(self, session_id: str):
        self.session_id = session_id

    def save_analysis(
        self,
        session_id: str,
        original_text: str,
        neutralized_text: str,
        llm_provider: str,
        bias_score: float,
        total_biases: int,
        source_url: Optional[str] = None
    ) -> str:
        """Save analysis and return analysis_id"""
        try:
            response = self.client.table("analyses").insert({
                "session_id": session_id,
                "original_text": original_text,
                "neutralized_text": neutralized_text,
                "llm_provider": llm_provider,
                "bias_score": bias_score,
                "total_biases_detected": total_biases,
                "source_url": source_url
            }).execute()

            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None

    def save_detected_biases(self, analysis_id: str, biases: List[Dict[str, Any]]):
        """Save detected biases for an analysis"""
        try:
            for bias in biases:
                self.client.table("detected_biases").insert({
                    "analysis_id": analysis_id,
                    "original_term": bias.get("term", ""),
                    "neutral_term": bias.get("replacement", ""),
                    "bias_category": bias.get("category", "general"),
                    "confidence": bias.get("confidence", 0.5),
                    "reasoning": bias.get("reasoning", "")
                }).execute()
        except Exception as e:
            print(f"Error saving biases: {e}")

    def save_perspective(self, analysis_id: str, perspective_type: str, generated_text: str):
        """Save a perspective variation"""
        try:
            self.client.table("perspective_variations").insert({
                "analysis_id": analysis_id,
                "perspective_type": perspective_type,
                "generated_text": generated_text
            }).execute()
        except Exception as e:
            print(f"Error saving perspective: {e}")

    def get_analysis_history(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get analysis history for a session"""
        try:
            response = self.client.table("analyses").select(
                "id, original_text, neutralized_text, llm_provider, bias_score, created_at, source_url"
            ).eq("session_id", session_id).order("created_at", desc=True).limit(limit).execute()

            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []

    def get_analysis_details(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed analysis including biases and perspectives"""
        try:
            analysis_response = self.client.table("analyses").select("*").eq("id", analysis_id).execute()
            if not analysis_response.data:
                return None

            analysis = analysis_response.data[0]

            biases_response = self.client.table("detected_biases").select("*").eq("analysis_id", analysis_id).execute()
            analysis["biases"] = biases_response.data if biases_response.data else []

            perspectives_response = self.client.table("perspective_variations").select("*").eq("analysis_id", analysis_id).execute()
            analysis["perspectives"] = perspectives_response.data if perspectives_response.data else []

            return analysis
        except Exception as e:
            print(f"Error fetching analysis details: {e}")
            return None

    def delete_analysis(self, analysis_id: str) -> bool:
        """Delete an analysis and related data"""
        try:
            self.client.table("analyses").delete().eq("id", analysis_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting analysis: {e}")
            return False

    def save_preference(self, session_id: str, llm_provider: str, temperature: float, theme: str):
        """Save user preferences"""
        try:
            existing = self.client.table("user_preferences").select("id").eq("session_id", session_id).execute()

            if existing.data:
                self.client.table("user_preferences").update({
                    "preferred_llm": llm_provider,
                    "temperature": temperature,
                    "theme": theme
                }).eq("session_id", session_id).execute()
            else:
                self.client.table("user_preferences").insert({
                    "session_id": session_id,
                    "preferred_llm": llm_provider,
                    "temperature": temperature,
                    "theme": theme
                }).execute()
        except Exception as e:
            print(f"Error saving preference: {e}")

    def get_preference(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        try:
            response = self.client.table("user_preferences").select("*").eq("session_id", session_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching preference: {e}")
            return None

    def get_statistics(self, session_id: str) -> Dict[str, Any]:
        """Get analysis statistics for a session"""
        try:
            analyses = self.client.table("analyses").select("llm_provider, bias_score").eq("session_id", session_id).execute()

            if not analyses.data:
                return {"total": 0, "by_provider": {}, "avg_bias": 0}

            total = len(analyses.data)
            by_provider = {}
            total_bias = 0

            for analysis in analyses.data:
                provider = analysis["llm_provider"]
                by_provider[provider] = by_provider.get(provider, 0) + 1
                total_bias += analysis["bias_score"]

            avg_bias = total_bias / total if total > 0 else 0

            return {
                "total": total,
                "by_provider": by_provider,
                "avg_bias": round(avg_bias, 2)
            }
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {"total": 0, "by_provider": {}, "avg_bias": 0}
