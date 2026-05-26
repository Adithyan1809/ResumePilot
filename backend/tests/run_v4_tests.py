"""
Automated custom test runner for the ResumePilot v4 AI Employability Operating System.
Executes all V4 unit and integration tests and prints a premium console report.
"""

import sys
import os
import asyncio

# Setup sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import test functions
import test_v4_engine

async def main():
    print("=" * 70)
    print("RESUMEPILOT V4 - TECHNICAL TEST RUNNER")
    print("=" * 70)
    
    test_functions = [
        ("Application Tracking Engine", test_v4_engine.test_application_tracking_engine),
        ("Market Intelligence Engine", test_v4_engine.test_market_intelligence_engine),
        ("Career Timeline Engine", test_v4_engine.test_career_timeline_engine),
        ("Interview Simulation Engine", test_v4_engine.test_interview_simulation_engine),
        ("Portfolio Generation Engine", test_v4_engine.test_portfolio_generation_engine),
        ("Employability Score Engine", test_v4_engine.test_employability_score_engine),
        ("Resume Strategy Engine", test_v4_engine.test_resume_strategy_engine),
        ("Branding Engine", test_v4_engine.test_branding_engine),
        ("Explainability Engine", test_v4_engine.test_explainability_engine),
        ("Orchestration Pipeline", test_v4_engine.test_orchestrator_integration)
    ]
    
    passed = 0
    failed = 0
    
    for name, func in test_functions:
        print(f"Running {name:.<45} ", end="", flush=True)
        try:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
            print("\033[92mPASS\033[0m")
            passed += 1
        except Exception as exc:
            print("\033[91mFAIL\033[0m")
            import traceback
            traceback.print_exc()
            failed += 1
            
    print("=" * 70)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
