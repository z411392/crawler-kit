## Initialize the Project

### Initialize Firebase

```bash
firebase init
```

```txt
✔ Which Firebase features do you want to set up for this directory? Press Space to select features, then Enter to confirm your choices.
 Firestore: Configure security rules and indexes files for Firestore, Functions: Configure a Cloud Functions directory and its files,
✔ Emulators: Set up local emulators for Firebase products
✔ Please select an option: Use an existing project
✔ Select a default Firebase project for this directory: Your Project (Your Project)
✔ What file should be used for Firestore Rules? firestore.rules
✔ What file should be used for Firestore indexes? firestore.indexes.json
✔ What language would you like to use to write Cloud Functions? Python
✔ Do you want to install dependencies now? Yes
✔ Which Firebase emulators do you want to set up? Press Space to select emulators, then Enter to confirm your choices. Functions Emulator, Pub/Sub Emulator
✔ Which port do you want to use for the functions emulator? 5001
✔ Which port do you want to use for the pubsub emulator? 8085
✔ Would you like to enable the Emulator UI? No
✔ Would you like to download the emulators now? Yes
```

### Modify `firebase.json`

Firebase will generate some unnecessary settings by default, so we need to clean them up manually.

```json
{
    "functions": [
        {
            "source": "functions",
            "codebase": "default",
            "ignore": [
                "venv",
                ".git",
                "firebase-debug.log",
                "firebase-debug.*.log",
                "*.local",
                "**/tests/**",
                "**/__pycache__/**",
                "**/*.pyc"
            ],
            "runtime": "python313"
        }
    ],
    "emulators": {
        "functions": {
            "port": 5001
        },
        "pubsub": {
            "port": 8085
        },
        "ui": {
            "enabled": false
        },
        "singleProjectMode": true
    }
}
```

### Remove Unnecessary Files

```bash
rm firestore.indexes.json
rm firestore.rules
```

## Manage the Project with `uv`

### Initialize `venv`

```bash
uv venv -p 3.13 functions/venv
source functions/venv/bin/activate
```

### Make `.vscode` Recognize the Virtual Environment

Create `.vscode/settings.json`:

```json
{
    "python.venvPath": "functions/venv",
    "python.defaultInterpreterPath": "functions/venv/bin/python"
}
```

### Create `pyproject.toml`

-   Add a new `pyproject.toml`
-   Add `venv`, `*egg-info` and `requirements.txt` to `.gitignore`
-   Merge `functions/.gitignore` into the root `.gitignore`, then delete the `functions/.gitignore`

### Install Dependencies

```bash
make install
```

### Generate `requirements.txt`

Since Firebase Functions still expects `functions/requirements.txt`, we need to manually generate this file:

```bash
make freeze
```
