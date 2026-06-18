import hashlib
import os
import json


def get_file_hash(filepath):
    """Calculeaza si returneaza hash-ul SHA-256 pentru un fisier."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None


def check_integrity(folder_path, baseline_file="baseline.json"):
    """Compara starea actuala a fișierelor cu starea salvata anterior."""
    current_hashes = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            if file != baseline_file:
                current_hashes[filepath] = get_file_hash(filepath)

    if not os.path.exists(baseline_file):
        print("Nu s-a gasit o stare de baza. Se creeaza una noua.")
        with open(baseline_file, 'w') as f:
            json.dump(current_hashes, f, indent=4)
        print(f"Starea initiala a fost salvata in '{baseline_file}'.")
        return

    with open(baseline_file, 'r') as f:
        saved_hashes = json.load(f)

    print("\n    Rezultatul Verificarii de Integritate    ")
    for filepath, current_hash in current_hashes.items():
        if filepath not in saved_hashes:
            print(f"[NOU] Fisier adaugat: {filepath}")
        elif current_hash != saved_hashes[filepath]:
            print(f"[MODIFICAT] Atentie! Fisierul a fost alterat: {filepath}")
        else:
            print(f"[OK] Fisier integru: {filepath}")

    for filepath in saved_hashes:
        if filepath not in current_hashes:
            print(f"[STERS] Fisierul lipseste: {filepath}")


if __name__ == "__main__":
    folder_de_test = "./test_folder"

    if not os.path.exists(folder_de_test):
        os.makedirs(folder_de_test)
        with open(os.path.join(folder_de_test, "document.txt"), "w") as f:
            f.write("Acesta este un document original.")

    check_integrity(folder_de_test)