#!/usr/bin/env python3
"""
ASL Translator - Main Entry Point
Fast launcher with optimized imports
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from asl_translator import ASLTranslator

if __name__ == "__main__":
    try:
        translator = ASLTranslator()
        translator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
