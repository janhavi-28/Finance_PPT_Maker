import os
from services.content_generator import content_generator
from services.ppt_generator import ppt_generator
from datetime import datetime

def test_thorough_visuals():
    """Thorough test for visual enhancements with focus on remaining areas"""
    test_cases = [
        {
            "name": "Balance Sheet Focus with Real Data",
            "topic": "AAPL Balance Sheet Analysis",
            "presentation_type": "quarterly_analysis",
            "target_audience": "Finance Team",
            "slide_count": 8,
            "include_real_data": True,
            "template": "corporate_blue",
            "focus": "balance"
        },
        {
            "name": "No Market Data Edge Case",
            "topic": "Generic Financial Review",
            "presentation_type": "quarterly_analysis",
            "target_audience": "Executive",
            "slide_count": 10,
            "include_real_data": False,
            "template": "financial_green",
            "focus": "fallback"
        },
        {
            "name": "High Slide Count Test",
            "topic": "Comprehensive MSFT Analysis",
            "presentation_type": "quarterly_analysis",
            "target_audience": "Investors",
            "slide_count": 15,
            "include_real_data": True,
            "template": "colorful_modern",
            "focus": "high_count"
        },
        {
            "name": "Image Placeholders in Various Templates",
            "topic": "Market Position and Risk",
            "presentation_type": "investment_proposal",
            "target_audience": "Board",
            "slide_count": 9,
            "include_real_data": False,
            "template": "modern_orange",
            "focus": "images"
        },
        {
            "name": "Performance Test with Charts/Tables",
            "topic": "GOOGL Revenue Projections",
            "presentation_type": "budget_planning",
            "target_audience": "Management",
            "slide_count": 12,
            "include_real_data": True,
            "template": "executive_dark",
            "focus": "performance"
        }
    ]
    
    results = []
    import time
    for case in test_cases:
        print(f"\n=== Testing {case['name']} ===")
        start_time = time.time()
        
        # Generate content
        content = content_generator.generate_presentation_content(
            topic=case["topic"],
            presentation_type=case["presentation_type"],
            target_audience=case["target_audience"],
            slide_count=case["slide_count"],
            include_real_data=case["include_real_data"],
            content_provider="SerpAPI"
        )
        
        generation_time = time.time() - start_time
        print(f"Content generation time: {generation_time:.2f}s")
        
        if not content:
            results.append({"case": case["name"], "status": "FAILED - No content generated", "time": generation_time})
            continue
        
        # Analyze content visuals with enhanced checks
        visual_summary = {
            "total_slides": len(content.get("slides", [])),
            "slides_with_charts": 0,
            "slides_with_tables": 0,
            "slides_with_images": 0,
            "pie_charts": 0,
            "bar_charts": 0,
            "line_charts": 0,
            "balance_pie": False,
            "risk_pie": False,
            "competitive_pie": False,
            "revenue_table": False,
            "performance_table": False,
            "balance_table": False,
            "image_placeholders": [],
            "balance_sheet_slide": None
        }
        
        for slide in content["slides"]:
            title_lower = slide["title"].lower()
            vs = slide.get("visual_suggestion", {})
            if vs:
                visual_summary["slides_with_charts"] += 1
                chart_type = vs.get("chart_type", "")
                if chart_type == "pie":
                    visual_summary["pie_charts"] += 1
                    if "balance" in title_lower:
                        visual_summary["balance_pie"] = True
                    if "risk" in title_lower or "volatility" in title_lower or "assessment" in title_lower:
                        visual_summary["risk_pie"] = True
                    if "competitive" in title_lower or "market position" in title_lower or "position" in title_lower:
                        visual_summary["competitive_pie"] = True
                elif chart_type == "bar":
                    visual_summary["bar_charts"] += 1
                elif chart_type == "line":
                    visual_summary["line_charts"] += 1
            
            if slide.get("table_data"):
                visual_summary["slides_with_tables"] += 1
                if "revenue" in title_lower or "profitability" in title_lower:
                    visual_summary["revenue_table"] = True
                if "performance" in title_lower:
                    visual_summary["performance_table"] = True
                if "balance" in title_lower:
                    visual_summary["balance_table"] = True
            
            if slide.get("image_suggestion"):
                visual_summary["slides_with_images"] += 1
                img_desc = slide["image_suggestion"].get("description", "")
                visual_summary["image_placeholders"].append(f"{slide['title']}: {img_desc}")
            
            # Specific balance sheet check
            if "balance sheet" in title_lower or "balance" in title_lower:
                visual_summary["balance_sheet_slide"] = {
                    "title": slide["title"],
                    "has_chart": bool(vs),
                    "chart_type": vs.get("chart_type") if vs else None,
                    "has_table": bool(slide.get("table_data")),
                    "has_image": bool(slide.get("image_suggestion"))
                }
        
        # Generate PPT with timing
        ppt_start = time.time()
        try:
            ppt_bytes = ppt_generator.create_presentation(
                content=content,
                template=case["template"],
                include_charts=True
            )
            ppt_time = time.time() - ppt_start
            print(f"PPT generation time: {ppt_time:.2f}s")
            
            if ppt_bytes:
                sanitized_topic = case["topic"].replace(" ", "_")[:20]
                filename = f"test_{sanitized_topic}_{case['presentation_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
                ppt_file = ppt_generator.save_presentation(ppt_bytes, filename)
                
                visual_summary["ppt_generated"] = True
                visual_summary["ppt_file"] = ppt_file
                print(f"PPT generated successfully: {ppt_file}")
            else:
                visual_summary["ppt_generated"] = False
                print("PPT generation failed")
        except Exception as e:
            visual_summary["ppt_generated"] = False
            visual_summary["error"] = str(e)
            print(f"PPT generation error: {e}")
            ppt_time = 0
        
        total_time = time.time() - start_time
        results.append({
            "case": case["name"],
            "status": "PASSED" if visual_summary.get("ppt_generated", False) else "FAILED",
            "visual_summary": visual_summary,
            "times": {"content": generation_time, "ppt": ppt_time, "total": total_time}
        })
    
    # Overall summary with enhanced details
    print("\n=== OVERALL TEST SUMMARY ===")
    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    total_content_time = sum(r["times"]["content"] for r in results)
    total_ppt_time = sum(r["times"]["ppt"] for r in results)
    print(f"Average Content Time: {total_content_time/total:.2f}s")
    print(f"Average PPT Time: {total_ppt_time/total:.2f}s")
    
    for result in results:
        print(f"\n{result['case']}: {result['status']}")
        summary = result["visual_summary"]
        print(f"  Charts: {summary['slides_with_charts']}/{summary['total_slides']}")
        print(f"  Tables: {summary['slides_with_tables']}")
        print(f"  Images: {summary['slides_with_images']}")
        print(f"  Pie Charts: {summary['pie_charts']} (Balance: {summary['balance_pie']}, Risk: {summary['risk_pie']}, Competitive: {summary['competitive_pie']})")
        print(f"  Revenue Table: {summary['revenue_table']}, Performance: {summary['performance_table']}, Balance: {summary['balance_table']}")
        if summary.get("image_placeholders"):
            print(f"  Image Placeholders: {len(summary['image_placeholders'])}")
        if summary.get("balance_sheet_slide"):
            bs = summary["balance_sheet_slide"]
            print(f"  Balance Sheet Slide: Chart={bs['has_chart']} ({bs['chart_type']}), Table={bs['has_table']}, Image={bs['has_image']}")
        print(f"  Times: Content={result['times']['content']:.2f}s, PPT={result['times']['ppt']:.2f}s, Total={result['times']['total']:.2f}s")
    
    # App integration note (manual verification needed)
    print("\n=== APP INTEGRATION NOTE ===")
    print("For full app.py integration, run 'streamlit run app.py' and generate a PPT via UI.")
    print("Verify: Visuals appear in generated PPT, no errors in console, UI responsive.")
    
    return results

if __name__ == "__main__":
    test_results = test_thorough_visuals()
    print("\nThorough testing completed.")
