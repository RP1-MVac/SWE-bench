from datasets import load_dataset
import os

def download_and_save(dataset_name, save_dir):
    print(f"Downloading {dataset_name}...")
    dataset = load_dataset(dataset_name)
    print(f"Saving {dataset_name} to {save_dir}...")
    dataset.save_to_disk(save_dir)
    print(f"Extraction of {dataset_name} complete.")

if __name__ == "__main__":
    os.makedirs("datasets", exist_ok=True)
    download_and_save("princeton-nlp/SWE-bench_Lite", "datasets/SWE-bench_Lite")
    # Uncomment the below line to also download the full SWE-bench, which is very large
    # download_and_save("princeton-nlp/SWE-bench", "datasets/SWE-bench")