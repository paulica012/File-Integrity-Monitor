import hashlib
import os
import json


def get_file_hash(filepath):
    """Calculează și returnează hash-ul SHA-256 pentru un fișier."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Citim fișierul în bucăți (chunks) pentru a nu bloca memoria în cazul fișierelor mari
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None


def check_integrity(folder_path, baseline_file="baseline.json"):
    """Compară starea actuală a fișierelor cu starea salvată anterior."""
    current_hashes = {}

    # Parcurgem toate fișierele din folderul specificat
    for root, _, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            # Excludem fișierul de stare din verificare pentru a evita buclele infinite
            if file != baseline_file:
                current_hashes[filepath] = get_file_hash(filepath)

    # Dacă nu există un fișier de stare (prima rulare), îl creăm
    if not os.path.exists(baseline_file):
        print("Nu s-a găsit o stare de bază. Se creează una nouă...")
        with open(baseline_file, 'w') as f:
            json.dump(current_hashes, f, indent=4)
        print(f"Starea inițială a fost salvată în '{baseline_file}'.")
        return

    # Încărcăm starea veche (baseline) și comparăm
    with open(baseline_file, 'r') as f:
        saved_hashes = json.load(f)

    print("\n--- Rezultatul Verificării de Integritate ---")
    for filepath, current_hash in current_hashes.items():
        if filepath not in saved_hashes:
            print(f"[NOU] Fișier adăugat: {filepath}")
        elif current_hash != saved_hashes[filepath]:
            print(f"[MODIFICAT] Atenție! Fișierul a fost alterat: {filepath}")
        else:
            print(f"[OK] Fișier integru: {filepath}")

    for filepath in saved_hashes:
        if filepath not in current_hashes:
            print(f"[ȘTERS] Fișierul lipsește: {filepath}")


# --- Zona de Testare ---
if __name__ == "__main__":
    folder_de_test = "./test_folder"

    # Creăm automat un folder de test și un fișier dacă nu există
    if not os.path.exists(folder_de_test):
        os.makedirs(folder_de_test)
        with open(os.path.join(folder_de_test, "document.txt"), "w") as f:
            f.write("Acesta este un document original.")

    check_integrity(folder_de_test)