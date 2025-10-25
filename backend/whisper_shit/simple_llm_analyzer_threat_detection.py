import json
import os
from openai import OpenAI

def analyze_military_threats(json_file_path: str):
    """
    Reads a meeting JSON file and analyzes military threats, intentions, and predicted events using an LLM.
    
    Args:
        json_file_path: Path to the JSON file containing meeting data
    
    Returns:
        dict: Analysis results from the LLM
    """
    
    # Initialize OpenAI client
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
    system_prompt = """You are an expert military intelligence analyst specializing in conversation analysis, threat assessment, and operational intent recognition. Your task is to analyze meeting transcripts and identify potential military events, threats, and strategic intentions.

## Your Analysis Framework:

### 1. THREAT IDENTIFICATION
Analyze the conversation for:
- **Direct threats**: Explicit mentions of hostile actions, attacks, or aggression
- **Indirect threats**: Veiled language, metaphors, or coded references to hostile intent
- **Threat level**: Rate each identified threat as LOW / MEDIUM / HIGH / CRITICAL
- **Threat targets**: Who or what is being threatened (persons, locations, infrastructure, organizations)
- **Threat timeline**: Immediate, short-term (days/weeks), medium-term (months), or long-term

### 2. OPERATIONAL INTENT DETECTION
Identify signs of:
- **Planned military operations**: Deployments, strikes, maneuvers, exercises
- **Resource mobilization**: Equipment, personnel, supplies being prepared or moved
- **Strategic positioning**: Changes in troop placement, base activities, or territorial movements
- **Coordination activities**: Multi-unit operations, inter-agency cooperation, alliance actions
- **Operational timeline**: When events are likely to occur (specific dates, time windows, or triggering conditions)

### 3. TACTICAL INDICATORS
Look for:
- **Mission terminology**: Code names, operation names, target designations
- **Military jargon**: Specific terms indicating operational planning (RDV points, ROE, CONOPS, etc.)
- **Logistical references**: Supply chains, transport, fuel, ammunition, medical preparations
- **Communication patterns**: Use of secure channels, radio silence orders, frequency changes
- **Personnel movements**: Rotations, deployments, recalls, leave cancellations

### 4. BEHAVIORAL & PSYCHOLOGICAL INDICATORS
Assess:
- **Urgency levels**: Time pressure, accelerated planning, deadline mentions
- **Stress markers**: Emotional tension, anxiety, aggression in speech patterns
- **Deception indicators**: Contradictions, evasiveness, deliberate misdirection
- **Confidence levels**: Certainty about outcomes, preparedness, morale
- **Authority dynamics**: Who makes decisions, who questions, who follows orders

### 5. GEOPOLITICAL CONTEXT
Consider:
- **Location references**: Specific regions, bases, borders, cities mentioned
- **Allied/enemy mentions**: References to other nations, groups, or organizations
- **Political events**: Elections, summits, sanctions, treaties referenced as triggers
- **Historical parallels**: References to past conflicts or operations as models

## ANALYSIS PRINCIPLES

1. **Be Precise**: Cite specific segments, timestamps, or phrases from the conversation
2. **Be Conservative**: Don't overinterpret; clearly distinguish between facts and inferences
3. **Consider Context**: Military jargon might be used metaphorically in non-military contexts
4. **Flag Ambiguity**: Explicitly note when evidence is weak or interpretations uncertain
5. **Prioritize Actionability**: Focus on intelligence that enables decision-making
6. **Cross-reference**: Look for corroborating patterns across multiple speakers or segments
7. **Cultural Awareness**: Consider regional military cultures and communication styles"""

    user_prompt = f"""MEETING DATA TO ANALYZE:
{json.dumps(meeting_data, indent=2)}

Analyze this conversation for threats, military events, and operational intent. Provide your analysis in the following JSON format:

{{
  "summary": {{
    "overall_threat_level": "LOW | MEDIUM | HIGH | CRITICAL",
    "confidence_score": 0-100,
    "primary_concern": "Brief description of main threat or event",
    "recommended_action": "What should be done based on this intelligence"
  }},
  
  "identified_threats": [
    {{
      "threat_id": "T001",
      "type": "Direct/Indirect/Implicit",
      "severity": "LOW/MEDIUM/HIGH/CRITICAL",
      "description": "Detailed description of the threat",
      "target": "Who/what is threatened",
      "timeline": "When this might occur",
      "indicators": ["List of specific phrases or patterns that indicate this threat"],
      "confidence": 0-100
    }}
  ],
  
  "predicted_events": [
    {{
      "event_id": "E001",
      "event_type": "Military operation/Deployment/Strike/Exercise/Other",
      "description": "What is likely to happen",
      "location": "Where this will occur (if mentioned)",
      "timeline": "Estimated timeframe",
      "probability": 0-100,
      "scale": "Small/Medium/Large/Strategic",
      "supporting_evidence": ["Specific conversation excerpts or patterns"],
      "prerequisites": ["What needs to happen before this event"]
    }}
  ],
  
  "tactical_intelligence": {{
    "operation_names": ["List of operation or code names mentioned"],
    "key_locations": ["Geographic references"],
    "personnel_involved": ["Ranks, units, or individuals mentioned"],
    "resources_mentioned": ["Equipment, supplies, capabilities discussed"],
    "coordination_indicators": ["Signs of multi-party coordination"]
  }},
  
  "behavioral_assessment": {{
    "urgency_level": "LOW/MEDIUM/HIGH",
    "deception_likelihood": 0-100,
    "morale_indicators": "HIGH/MEDIUM/LOW",
    "decision_authority": "Who appears to be in command",
    "stress_markers": ["Observable tension or pressure points"]
  }},
  
  "timeline_analysis": {{
    "immediate_actions": ["Events likely within 24-72 hours"],
    "short_term": ["Events likely within 1-4 weeks"],
    "medium_term": ["Events likely within 1-6 months"],
    "conditional_events": ["Events dependent on triggers or conditions"]
  }},
  
  "red_flags": [
    "Critical warning signs that require immediate attention"
  ],
  
  "uncertainties": [
    "Ambiguous elements that need clarification or further intelligence"
  ],
  
  "intelligence_gaps": [
    "Missing information that would improve assessment accuracy"
  ]
}}"""

    # Call the LLM
    print("🤖 Analyzing with LLM for Threats & Intent...")
    print("-" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4o-mini for cost-effective analysis
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,  # Low temperature for consistent analysis
        response_format={"type": "json_object"}  # Force JSON output
    )
    
    # Parse the response
    analysis = json.loads(response.choices[0].message.content)
    
    # Display results
    print("\n🎯 MILITARY THREAT & INTENT ANALYSIS")
    print("=" * 60)
    
    # Summary
    summary = analysis.get("summary", {})
    print(f"\n📊 SUMMARY")
    print(f"   Threat Level: {summary.get('overall_threat_level', 'N/A')}")
    print(f"   Confidence: {summary.get('confidence_score', 'N/A')}%")
    print(f"   Primary Concern: {summary.get('primary_concern', 'N/A')}")
    print(f"   Recommended Action: {summary.get('recommended_action', 'N/A')}")
    
    # Identified Threats
    threats = analysis.get("identified_threats", [])
    if threats:
        print(f"\n⚠️  IDENTIFIED THREATS ({len(threats)})")
        for threat in threats:
            print(f"\n   [{threat.get('threat_id', 'N/A')}] {threat.get('type', 'N/A')} - {threat.get('severity', 'N/A')}")
            print(f"   Description: {threat.get('description', 'N/A')}")
            print(f"   Target: {threat.get('target', 'N/A')}")
            print(f"   Timeline: {threat.get('timeline', 'N/A')}")
            print(f"   Confidence: {threat.get('confidence', 'N/A')}%")
            if threat.get('indicators'):
                print(f"   Indicators: {', '.join(threat['indicators'])}")
    
    # Predicted Events
    events = analysis.get("predicted_events", [])
    if events:
        print(f"\n🔮 PREDICTED EVENTS ({len(events)})")
        for event in events:
            print(f"\n   [{event.get('event_id', 'N/A')}] {event.get('event_type', 'N/A')}")
            print(f"   Description: {event.get('description', 'N/A')}")
            print(f"   Location: {event.get('location', 'Unknown')}")
            print(f"   Timeline: {event.get('timeline', 'N/A')}")
            print(f"   Probability: {event.get('probability', 'N/A')}%")
            print(f"   Scale: {event.get('scale', 'N/A')}")
    
    # Tactical Intelligence
    tactical = analysis

if __name__ == "__main__":
    # Example usage
    input_path = "data/alex_jordan_conversation.json"  # Input: JSON to analyze
    result_path = "hierarchy_analysis/simple_personas_output.json"  # Output: Where to save results
    
    # Choose your LLM provider:
    
    # Option 1: OpenAI (GPT-4)
    try:
        # Analyze the INPUT file (not result_path)
        result = analyze_military_threats(input_path)
        
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