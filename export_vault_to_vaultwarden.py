import csv
import json
import subprocess
import os
import re
from pathlib import Path

def run_op(args):
    result = subprocess.run(["op"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Errore op {' '.join(args)}:\n{result.stderr}")
    return result.stdout

def signin_op():
    try:
        run_op(["vault", "list", "--format", "json"])
        print("✅ Sei già autenticato in 1Password CLI.\n")
    except Exception:
        print("🔐 Non sei autenticato. Effettuo il login...\n")

        # Esegue `op signin` e cattura il comando `export OP_SESSION_xyz=...`
        signin_cmd = subprocess.run(["op", "signin", "--raw"], capture_output=True, text=True)
        session_token = signin_cmd.stdout.strip()

        if signin_cmd.returncode != 0 or not session_token:
            print(signin_cmd.stderr)
            raise Exception("❌ Login non riuscito. Verifica le credenziali e riprova.")

        # Setta la variabile d'ambiente
        os.environ["OP_SESSION_my"] = session_token  # Cambia "my" con il tuo nome account se diverso

        # Verifica
        try:
            run_op(["vault", "list", "--format", "json"])
            print("✅ Login completato con successo!\n")
        except Exception as e:
            raise Exception(f"❌ Login non riuscito dopo export della sessione.\n{e}")



def estrai_item(item_json):
    item = json.loads(item_json)
    title = item.get("title", "")
    url = item.get("urls", [{}])[0].get("href", "")
    username = ""
    password = ""
    otp = ""

    for field in item.get("fields", []):
        if field.get("id") == "username":
            username = field.get("value", "")
        elif field.get("id") == "password":
            password = field.get("value", "")
        elif field.get("id") == "otp":
            otp = field.get("value", "")

    return {
        "folder": "",
        "favorite": "",
        "type": "login",
        "name": title,
        "notes": item.get("notesPlaintext", ""),
        "fields": "",
        "login_uri": url,
        "login_username": username,
        "login_password": password,
        "login_totp": otp,
        "tags": "imported-from-1password"
    }

def scegli_cassaforte():
    print("📂 Recupero elenco casseforti (vaults)...")
    output = run_op(["vault", "list", "--format", "json"])
    vaults = json.loads(output)
    if not vaults:
        raise Exception("Nessuna cassaforte trovata!")

    print("\nScegli una cassaforte dall'elenco:")
    for i, v in enumerate(vaults, 1):
        print(f"{i}: {v['name']} (ID: {v['id']})")

    scelta = input(f"\nInserisci un numero da 1 a {len(vaults)}: ").strip()
    try:
        idx = int(scelta) - 1
        if idx < 0 or idx >= len(vaults):
            raise ValueError
    except ValueError:
        raise Exception("Input non valido")

    return vaults[idx]['id'], vaults[idx]['name']

def sanitize_filename(name):
    # Rimuove caratteri non alfanumerici e sostituisce spazi con underscore
    name = name.lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

def main():
    signin_op()

    vault_id, vault_name = scegli_cassaforte()

    print(f"\n📤 Estrazione degli item dalla cassaforte '{vault_name}' (ID: {vault_id})...")
    output = run_op(["item", "list", "--vault", vault_id, "--format", "json"])
    items = json.loads(output)

    print(f"🔍 Trovati {len(items)} item. Inizio esportazione dettagli...")

    data = []
    for item in items:
        item_id = item["id"]
        item_json = run_op(["item", "get", item_id, "--format", "json"])
        item_data = estrai_item(item_json)
        data.append(item_data)

    filename = f"vault_{sanitize_filename(vault_name)}_bitwarden.csv"
    output_csv = Path(filename)
    with output_csv.open("w", newline="") as csvfile:
        fieldnames = [
            "folder", "favorite", "type", "name", "notes", "fields",
            "login_uri", "login_username", "login_password", "login_totp", "tags"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"\n✅ Esportazione completata: {output_csv.absolute()}")

if __name__ == "__main__":
    main()
