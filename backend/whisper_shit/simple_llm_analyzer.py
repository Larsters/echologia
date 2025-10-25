import json
import os
from openai import OpenAI

def analyze_military_hierarchy(json_file_path: str):
    """
    Reads a meeting JSON file and analyzes military hierarchy using an LLM.
    
    Args:
        json_file_path: Path to the JSON file containing meeting data
    
    Returns:
        dict: Analysis results from the LLM
    """
    
    # Initialize OpenAI client
    # Make sure to set: export OPENAI_API_KEY="your-key-here"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Read the JSON file
    print(f"📂 Reading file: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        meeting_data = json.load(f)
    
    print(f"✅ Loaded meeting: {meeting_data.get('session_id', 'Unknown')}")
    print(f"   Speakers: {len(meeting_data.get('personas', []))}")
    print(f"   Segments: {len(meeting_data.get('segments', []))}")
    print(f"   Duration: {meeting_data.get('meta', {}).get('duration_sec', 0):.1f} seconds\n")
    
    # Prepare the analysis prompt
    system_prompt = """You are a military analyst expert specializing in organizational hierarchy analysis. 
You analyze meeting transcripts to identify military ranks and chain of command based on:
- Speaking patterns and authority
- Language used (commands vs. requests)
- Decision-making authority
- Deference patterns from other speakers
- Speaking time and interruption patterns
- Age and demographic data
You ONLY assign concrete military titles when you above 80 percent confidence for both speakers, otherwise assign a rank like highest rank, second highest rank, etc.
"""
#last line which was added above
#You ONLY assign military titles when you have HIGH confidence. If uncertain, explain why.

    user_prompt = f"""Analyze this meeting data and determine the military hierarchy:

MEETING DATA:
{json.dumps(meeting_data, indent=2)}

QUESTION: What's the hierarchy of these people speaking in a military sense? Only specify military titles for speakers if you are very sure. Also give the probability of how confident you are about this hierarchy.

Provide your analysis in the following JSON format:
{{
  "hierarchy_analysis": [
    {{
      "speaker_id": "spk_XX",
      "rank": "Military Rank or 'Unknown'",
      "confidence_percent": 0-100,
      "reasoning": "Brief explanation"
    }}
  ],
  "overall_confidence": 0-100,
  "key_indicators": ["list of behavioral patterns observed"],
  "uncertainties": ["list of factors that make determination difficult"]
}}"""

    # Call the LLM
    print("🤖 Analyzing with LLM...")
    print("-" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4 mini for better analysis
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,  # Lower temperature for more consistent analysis
        response_format={"type": "json_object"}  # Force JSON output
    )
    
    # Parse the response
    analysis = json.loads(response.choices[0].message.content)
    
    # Display results
    print("\n📊 MILITARY HIERARCHY ANALYSIS")
    print("=" * 60)
    
    for speaker in analysis.get("hierarchy_analysis", []):
        print(f"\n🎖️  {speaker['speaker_id']}")
        print(f"   Rank: {speaker['rank']}")
        print(f"   Confidence: {speaker['confidence_percent']}%")
        print(f"   Reasoning: {speaker['reasoning']}")
    
    print(f"\n\n📈 Overall Confidence: {analysis.get('overall_confidence', 'N/A')}%")
    
    print("\n🔍 Key Indicators:")
    for indicator in analysis.get("key_indicators", []):
        print(f"   • {indicator}")
    
    if analysis.get("uncertainties"):
        print("\n⚠️  Uncertainties:")
        for uncertainty in analysis.get("uncertainties", []):
            print(f"   • {uncertainty}")
    
    print("\n" + "=" * 60)
    print(f"💬 Tokens used: {response.usage.total_tokens}")
    
    return analysis


def analyze_military_hierarchy_anthropic(json_file_path: str):
    """
    Alternative version using Anthropic Claude instead of OpenAI.
    
    Args:
        json_file_path: Path to the JSON file containing meeting data
    
    Returns:
        dict: Analysis results from Claude
    """
    import anthropic
    
    # Initialize Anthropic client
    # Make sure to set: export ANTHROPIC_API_KEY="your-key-here"
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Read the JSON file
    print(f"📂 Reading file: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        meeting_data = json.load(f)
    
    print(f"✅ Loaded meeting: {meeting_data.get('session_id', 'Unknown')}")
    print(f"   Speakers: {len(meeting_data.get('personas', []))}")
    print(f"   Segments: {len(meeting_data.get('segments', []))}")
    print(f"   Duration: {meeting_data.get('meta', {}).get('duration_sec', 0):.1f} seconds\n")
    
    # Prepare the analysis prompt
    prompt = f"""You are a military analyst expert. Analyze this meeting data and determine the military hierarchy.

MEETING DATA:
{json.dumps(meeting_data, indent=2)}

QUESTION: What's the hierarchy of these people speaking in a military sense? Only specify military titles for speakers if you are very sure. Also give the probability of how confident you are about this hierarchy.

Provide your analysis in the following JSON format:
{{
  "hierarchy_analysis": [
    {{
      "speaker_id": "spk_XX",
      "rank": "Military Rank or 'Unknown'",
      "confidence_percent": 0-100,
      "reasoning": "Brief explanation"
    }}
  ],
  "overall_confidence": 0-100,
  "key_indicators": ["list of behavioral patterns observed"],
  "uncertainties": ["list of factors that make determination difficult"]
}}

Respond ONLY with valid JSON."""

    # Call Claude
    print("🤖 Analyzing with Claude...")
    print("-" * 60)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response
    response_text = response.content[0].text
    
    # Extract JSON from response (Claude might wrap it in markdown)
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    analysis = json.loads(response_text)
    
    # Display results (same format as OpenAI version)
    print("\n📊 MILITARY HIERARCHY ANALYSIS")
    print("=" * 60)
    
    for speaker in analysis.get("hierarchy_analysis", []):
        print(f"\n🎖️  {speaker['speaker_id']}")
        print(f"   Rank: {speaker['rank']}")
        print(f"   Confidence: {speaker['confidence_percent']}%")
        print(f"   Reasoning: {speaker['reasoning']}")
    
    print(f"\n\n📈 Overall Confidence: {analysis.get('overall_confidence', 'N/A')}%")
    
    print("\n🔍 Key Indicators:")
    for indicator in analysis.get("key_indicators", []):
        print(f"   • {indicator}")
    
    if analysis.get("uncertainties"):
        print("\n⚠️  Uncertainties:")
        for uncertainty in analysis.get("uncertainties", []):
            print(f"   • {uncertainty}")
    
    print("\n" + "=" * 60)
    print(f"💬 Input tokens: {response.usage.input_tokens}")
    print(f"💬 Output tokens: {response.usage.output_tokens}")
    
    return analysis



    
if __name__ == "__main__":
    # Example usage
    input_path = "data/alex_jordan_conversation.json"  # Input: JSON to analyze
    result_path = "hierarchy_analysis/simple_personas_output.json"  # Output: Where to save results
    
    # Choose your LLM provider:
    
    # Option 1: OpenAI (GPT-4)
    try:
        # Analyze the INPUT file (not result_path)
        result = analyze_military_hierarchy(input_path)
        
        # Save results to OUTPUT file
        with open(result_path, "w") as f:
            json.dump(result, f, indent=2)
        print("\n💾 Results saved to: " + result_path)
        
    except Exception as e:
        print(f"❌ Error: {e}")

    # Option 2: Anthropic Claude (uncomment to use)
    # try:
    #     result = analyze_military_hierarchy_anthropic(json_file)
    #     with open("hierarchy_analysis_result.json", "w") as f:
    #         json.dump(result, f, indent=2)
    #     print("\n💾 Results saved to: hierarchy_analysis_result.json")
    # except Exception as e:
    #     print(f"❌ Error: {e}")