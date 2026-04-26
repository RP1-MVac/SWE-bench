import json
import os
from collections import defaultdict
from datasets import load_dataset, load_from_disk

def main():
    print("Loading SWE-bench_Lite dataset...")
    
    # Try Hugging Face first, fallback to local if needed
    try:
        dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    except Exception as e:
        print(f"Failed to load from HuggingFace: {e}")
        local_path = os.path.join("datasets", "SWE-bench_Lite", "test")
        dataset = load_from_disk(local_path)

    # Convert to a list of dicts
    records = dataset.to_pandas().to_dict(orient="records")

    # Group by repository to make it a useful, navigable structure
    structured_data = defaultdict(dict)
    
    for row in records:
        repo = row["repo"]
        instance_id = row["instance_id"]
        
        # Build a clean dictionary for the instance
        instance_data = {
            "base_commit": row.get("base_commit", ""),
            "created_at": row.get("created_at", ""),
            "version": row.get("version", ""),
            "environment_setup_commit": row.get("environment_setup_commit", ""),
            "problem_statement": row.get("problem_statement", ""),
            "hints_text": row.get("hints_text", ""),
            "tests": {
                "FAIL_TO_PASS": row.get("FAIL_TO_PASS", ""),
                "PASS_TO_PASS": row.get("PASS_TO_PASS", "")
            },
            "patches": {
                "reference_patch": row.get("patch", ""),
                "test_patch": row.get("test_patch", "")
            }
        }
        
        structured_data[repo][instance_id] = instance_data

    # Convert defaultdict back to a standard dict for JSON serialization
    structured_data = dict(structured_data)

    output_file = "swe_bench_lite_structured.json"
    print(f"Writing data to {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        # indent=2 makes it human readable
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
    print(f"Success! {len(records)} instances organized by repository and saved to {output_file}")

if __name__ == "__main__":
    main()
