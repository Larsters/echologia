import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = OpenAI()

def extract_speaker_names_with_llm(conversation_segments, personas):
    """
    Use LLM to analyze conversation and extract speaker names
    Returns updated personas with names
    """
    # Build conversation text
    conversation_text = ""
    for seg in conversation_segments:
        speaker = seg["speaker_id"]
        text = seg["text"]
        conversation_text += f"{speaker}: {text}\n"
    
    # Create prompt
    prompt = f"""
Analyze this conversation and identify the names of the speakers.
Return ONLY a JSON object mapping speaker_id to name.
If a speaker's name is not mentioned or unclear, use "Unknown".

Conversation:
{conversation_text}

Example output: {{"spk_01": "John", "spk_02": "Alex"}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=200
        )
        
        # Parse the response
        result_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON
        try:
            # Find JSON in the response (in case there's extra text)
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            json_str = result_text[start:end]
            name_mapping = json.loads(json_str)
        except:
            print("⚠️  Could not parse LLM response as JSON")
            name_mapping = {}
        
        # Update personas with names
        updated_personas = []
        for persona in personas:
            speaker_id = persona["speaker_id"]
            name = name_mapping.get(speaker_id, "Unknown")
            persona_copy = persona.copy()
            persona_copy["name"] = name
            updated_personas.append(persona_copy)
        
        print("✅ LLM name extraction complete")
        return updated_personas
        
    except Exception as e:
        print(f"⚠️  LLM name extraction failed: {e}")
        # Return personas with "Unknown" names
        for persona in personas:
            persona["name"] = "Unknown"
        return personas