"""
Automated custom test runner for the ResumePilot v3 Employability Infrastructure.
Executes unit and integration tests and prints a premium colored console report.
"""

import sys
import os
import asyncio

# Setup sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import test functions
import test_v3_engine

async def main():
    print("=" * 70)
    print("RESUMEPILOT V3 - TECHNICAL TEST RUNNER")
    print("=" * 70)
    
    test_functions = [
        ("Tech Extractions", test_v3_engine.test_metric_and_tech_extractions),
        ("Evidence Structures", test_v3_engine.test_evidence_structure_parsing),
        ("Fallback Scraping", test_v3_engine.test_fallback_scraping_utility),
        ("Fallback Cosine Similarity", test_v3_engine.test_fallback_similarities),
        ("Retrieval Bullets", test_v3_engine.test_retrieval_bullet_adaptation),
        ("ATS & Recruiter Simulations", test_v3_engine.test_ats_and_recruiter_simulators),
        ("Resume Differentials", test_v3_engine.test_resume_differentials),
        ("GitHub deep portfolio", test_v3_engine.test_github_deep_portfolio_analysis),
        ("Orchestration Pipeline", test_v3_engine.test_employability_pipeline_orchestrator)
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
            print(f"  Error details: {exc}")
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
