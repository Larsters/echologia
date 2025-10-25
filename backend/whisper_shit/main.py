#!/usr/bin/env python3
"""
Main entry point for the audio processing pipeline.
Imports and runs the processor module.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path so we can import processor
sys.path.insert(0, os.path.dirname(__file__))

from processor import process_audio_to_personas

def main():
    """Main entry point for the audio processing application"""
    print("🎬 Audio Processing Pipeline")
    print("=" * 50)

    # Default audio file
    audio_file = "test-audio2.mp3"

    # Check if audio file exists
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found!")
        print("Please ensure your audio file is in the current directory.")
        return 1

    try:
        # Run the processing pipeline
        result = process_audio_to_personas(audio_file)

        # Save to JSON
        output_file = "personas_output.json"
        import json
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print("\n" + "=" * 50)
        print("✅ Processing complete!")
        print("=" * 50)
        print(f"📊 Session ID: {result['session_id']}")
        print(f"⏱️  Duration: {result['meta']['duration_sec']} seconds")
        print(f"👥 Found {len(result['personas'])} speakers")
        print(f"📝 Generated {len(result['segments'])} segments")
        print(f"💾 Output saved to: {output_file}")

        # Print personas summary
        print("\n📋 Personas Summary:")
        for persona in result['personas']:
            print(f"  {persona['speaker_id']}: {persona['speaking_percent']}% speaking time")

        print("\n🎯 Pipeline completed successfully!")
        return 0

    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)