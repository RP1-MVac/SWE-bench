import pandas as pd
from datasets import load_dataset, load_from_disk
import os

def main():
    print("Loading SWE-bench Lite dataset...")
    
    # Try to load from HuggingFace directly, it caches locally anyway
    try:
        dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    except Exception as e:
        print(f"Failed to load from HuggingFace: {e}")
        # Fallback to local arrow files if needed
        local_path = os.path.join("datasets", "SWE-bench_Lite", "test")
        print(f"Attempting to load from local path: {local_path}")
        dataset = load_from_disk(local_path)
    
    # Convert to pandas DataFrame for easy tabular inspection
    df = dataset.to_pandas()
    
    print("\n" + "="*50)
    print(f"Total test instances: {len(df)}")
    print(f"Available columns: {', '.join(df.columns.tolist())}")
    print("="*50 + "\n")
    
    # Let's count how many issues there are per repository
    print("Issues per repository:")
    print(df['repo'].value_counts().to_string())
    print("\n" + "="*50 + "\n")

    # Inspect the first row in detail
    first_row = df.iloc[0]
    print("--- Detailed look at the first example ---")
    print(f"Instance ID:   {first_row['instance_id']}")
    print(f"Repository:    {first_row['repo']}")
    print(f"Base Commit:   {first_row['base_commit']}")
    print(f"Created At:    {first_row['created_at']}")
    print("-" * 50)
    
    print("PROBLEM STATEMENT (first 500 chars):")
    print("-" * 50)
    # The problem statement is what the AI is given to solve the issue
    print(first_row['problem_statement'][:500])
    if len(first_row['problem_statement']) > 500:
        print("...\n[Truncated for brevity]")
    
    print("\n" + "-" * 50)
    print("REFERENCE PATCH (first 500 chars):")
    print("-" * 50)
    # The patch is the true solution written by human developers
    print(first_row['patch'][:500])
    if len(first_row['patch']) > 500:
        print("...\n[Truncated for brevity]")

if __name__ == "__main__":
    main()
