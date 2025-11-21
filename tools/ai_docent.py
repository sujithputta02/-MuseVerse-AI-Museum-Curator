"""AI Docent - Conversational guide that answers questions about exhibitions."""
import google.generativeai as genai
import config

class AIDocent:
    """Interactive AI guide for exhibitions."""
    
    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
        self.conversation_history = []
    
    def ask_question(self, question: str, exhibition: dict) -> str:
        """Ask the AI docent a question about the exhibition."""
        # Build context from exhibition
        context = self._build_context(exhibition)
        
        # Create prompt
        prompt = f"""You are an expert museum docent guiding visitors through an exhibition about {exhibition.get('topic', 'this topic')}.

Exhibition Context:
{context}

Visitor Question: {question}

Provide a helpful, engaging, and educational answer. Be conversational and enthusiastic.
If the question is outside the exhibition scope, gently redirect to exhibition content.

Answer:"""

        try:
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # Store in history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            return answer
        except Exception as e:
            return f"I apologize, but I'm having trouble answering that question right now. Could you rephrase it?"
    
    def _build_context(self, exhibition: dict) -> str:
        """Build context string from exhibition."""
        context_parts = []
        
        # Add overview
        if exhibition.get("overview"):
            context_parts.append(f"Overview: {exhibition['overview']}")
        
        # Add curator notes
        if exhibition.get("curator_notes"):
            context_parts.append(f"Curator's Notes: {exhibition['curator_notes'][:500]}...")
        
        # Add room summaries
        for i, room in enumerate(exhibition.get("rooms", [])[:3], 1):
            context_parts.append(f"Room {i} - {room.get('title')}: {room.get('description', '')[:200]}")
        
        return "\n\n".join(context_parts)
    
    def get_conversation_history(self) -> list:
        """Get conversation history."""
        return self.conversation_history
    
    def suggest_questions(self, exhibition: dict) -> list:
        """Suggest interesting questions visitors might ask."""
        topic = exhibition.get("topic", "this exhibition")
        
        return [
            f"What's the most surprising thing about {topic}?",
            f"How does {topic} connect to modern life?",
            f"What should I look at first?",
            f"Can you tell me more about the timeline?",
            f"What's the significance of this topic?"
        ]
