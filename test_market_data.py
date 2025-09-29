#!/usr/bin/env python3
"""
Test script for market data service enhancements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.market_data_service import MarketDataService
import time

def test_enhanced_retry_logic():
    """Test the enhanced retry logic and fallback symbols"""
    print("Testing enhanced retry logic and fallback symbols...")

    service = MarketDataService()

    # Test cases with different indices
    test_cases = [
        ("^NSEI", "Nifty 50"),
        ("^GSPC", "S&P 500"),
        ("^DJI", "Dow Jones"),
        ("^IXIC", "NASDAQ")
    ]

    results = {}

    for symbol, name in test_cases:
        print(f"\nTesting {name} ({symbol})...")
        start_time = time.time()

        try:
            analysis = service._analyze_index(symbol, f"{name} Analysis", 3)
            end_time = time.time()

            # Verify the analysis structure
            required_keys = [
                "topic", "analysis_type", "symbol", "current_data",
                "historical_performance", "risk_metrics", "technical_indicators",
                "market_comparison", "key_insights", "forecast_data"
            ]

            missing_keys = [key for key in required_keys if key not in analysis]
            if missing_keys:
                print(f"❌ FAIL: Missing keys in analysis: {missing_keys}")
                results[symbol] = False
                continue

            # Check if we got actual data (not fallback)
            if analysis.get("data_quality") == "high":
                print(f"✅ PASS: High quality data retrieved for {symbol}")
            elif analysis.get("data_quality") == "medium":
                print(f"⚠️  MEDIUM: Medium quality data for {symbol}")
            else:
                print(f"❌ FAIL: No data quality indicator for {symbol}")
                results[symbol] = False
                continue

            # Verify symbol might be different (fallback used)
            actual_symbol = analysis.get("symbol")
            if actual_symbol != symbol:
                print(f"ℹ️  INFO: Used fallback symbol {actual_symbol} instead of {symbol}")

            # Check current data has realistic values
            current_data = analysis.get("current_data", {})
            if current_data.get("current_price", 0) > 0:
                print(f"✅ Current price: ${current_data['current_price']:.2f}")
            else:
                print(f"❌ FAIL: Invalid current price for {symbol}")
                results[symbol] = False
                continue

            # Check historical performance
            hist_perf = analysis.get("historical_performance", {})
            if hist_perf.get("1_year", 0) != 0:
                print(f"✅ 1-year return: {hist_perf['1_year']:.2f}%")
            else:
                print(f"❌ FAIL: No historical performance data for {symbol}")
                results[symbol] = False
                continue

            # Check risk metrics
            risk_metrics = analysis.get("risk_metrics", {})
            if risk_metrics.get("volatility", 0) > 0:
                print(f"✅ Volatility: {risk_metrics['volatility']:.2f}%")
            else:
                print(f"❌ FAIL: No risk metrics for {symbol}")
                results[symbol] = False
                continue

            results[symbol] = True
            print(f"⏱️  Time taken: {end_time - start_time:.2f}s")

        except Exception as e:
            end_time = time.time()
            print(f"❌ FAIL: Exception for {symbol}: {str(e)}")
            print(f"⏱️  Time taken: {end_time - start_time:.2f}s")
            results[symbol] = False

    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for symbol, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{symbol}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Enhanced retry logic is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = test_enhanced_retry_logic()
    sys.exit(0 if success else 1)
