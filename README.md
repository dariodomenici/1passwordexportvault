# 🔐 Esporta da 1Password a Vaultwarden

Uno script Python che consente di esportare in modo sicuro le credenziali da una cassaforte di [1Password](https://1password.com) in un file CSV compatibile con l'importazione in [Vaultwarden](https://github.com/dani-garcia/vaultwarden), con supporto anche per codici OTP.

---

## ✨ Funzionalità

✅ Accesso tramite 1Password CLI (`op`)  
✅ Scelta interattiva della cassaforte da esportare  
✅ Conversione dei dati in formato CSV per Vaultwarden  
✅ Supporto a username, password, URI e OTP  
✅ Etichetta opzionale per filtrare facilmente le voci importate  
✅ Nome del file CSV basato sul nome della cassaforte  

---

## ⚙️ Requisiti

- [Python 3.7+](https://www.python.org/)
- [jq](https://stedolan.github.io/jq/) installato e disponibile nel `PATH`
- [1Password CLI v2+](https://developer.1password.com/docs/cli/)

Puoi installare `jq` ad esempio con:

```bash
brew install jq         # macOS
sudo apt install jq     # Ubuntu/Debian
```

---

## 📦 Installazione

1. **Clona la repo**:

```bash
git clone https://github.com/dariodomenici/1passwordexportvault.git
cd 1passwordexportvault
```

2. **(Opzionale) Installa eventuali dipendenze Python**:

Se lo script verrà esteso, potresti voler usare:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Uso

### 🔑 1. Esegui il login a 1Password CLI

Prima di lanciare lo script, **è obbligatorio** autenticarsi con `op`:

```bash
eval $(op signin)
```

Ti verranno chiesti:
- Dominio (es. `my.1password.eu`)
- Email
- Secret Key
- Master Password

⚠️ Se salti questo passaggio, lo script non riuscirà ad accedere ai dati.

---

### 🚀 2. Esegui lo script

```bash
python3 export_vault_to_vaultwarden.py
```

### 🧭 3. Segui le istruzioni interattive

- Verrà mostrata la lista delle casseforti disponibili: scegli quella da esportare
- Inserisci un'etichetta personalizzata da assegnare a tutte le voci (opzionale)
- Il file CSV verrà generato con il nome:

```
vaultwarden_import_<nome_cassaforte>.csv
```

Esempio:

```
vaultwarden_import_Marketing_e_Comunicazione.csv
```

---

## 🗃️ Output generato

Il CSV contiene queste colonne, compatibili con l'importazione in Vaultwarden:

| Campo            | Contenuto                                 |
|------------------|--------------------------------------------|
| `folder`         | Vuoto                                       |
| `favorite`       | Vuoto                                       |
| `type`           | `login`                                     |
| `name`           | Titolo della voce                           |
| `notes`          | Note in chiaro                              |
| `fields`         | Vuoto                                       |
| `login_uri`      | Primo URL associato                         |
| `login_username` | Username, se presente                       |
| `login_password` | Password, se presente                       |
| `login_totp`     | Codice OTP, se presente                     |

---

## ⚠️ Attenzione

- Il file CSV generato contiene **password e OTP in chiaro**: gestiscilo con estrema cautela.
- Lo script esporta solo le voci con categoria `LOGIN`.
- Dopo l'import in Vaultwarden, puoi usare l'etichetta per selezionare rapidamente le voci da spostare in una cassaforte specifica.

---

## 🧑‍💻 Autore

Realizzato da [Dario Domenici](https://github.com/dariodomenici) – Consulente in innovazione e digitalizzazione @ Seedble

---

## 📄 Licenza

Questo progetto è distribuito con licenza [MIT](LICENSE).
