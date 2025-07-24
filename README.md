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

## CLI Structure for Implementation Project

### Add `functions/.env` and `functions/.env.local`

* Do **not** commit these files into the repository.
* These files **must** exist in the directory during deployment.
* `.env.local` will be loaded when using Firebase Functions Emulator, but **not** in production.

```.env
# functions/.env
TZ=Asia/Taipei
PROJECT_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
API_KEY=
AUTH_DOMAIN=
STORAGE_BUCKET=
MESSAGING_SENDER_ID=
APP_ID=
MEASUREMENT_ID=
DATABASE_URL=
HMAC_SIGNING_KEY=
```

```.env
# functions/.env.local
PUBSUB_EMULATOR_HOST=localhost:8085
```

> Remember to add `.env` and `.env.local` to `.gitignore`

---

### Create CLI using `typer`

We use `typer` for building the CLI because of its decorator-based API.
Here, we structure it using an `__init__.py`-style entrypoint.

Initial setup:

```python
from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop


def callback(context: Context):
    loop = ensure_event_loop()
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


app = Typer(callback=callback)
```

We use `ensure_event_loop` to prepare for running async functions.

---

### Add Your First CLI Command

1. Create `functions/crawler_kit/entrypoints/cli/typer/greet/__init__.py`:

```python
from typer import Typer

greet = Typer(name="greet")
```

2. Implement `functions/crawler_kit/modules/greet/presentation/cli/handlers/handle_hello.py`:

```python
from click.core import Context


def handle_hello(context: Context):
    print("hello, world")
```

3. Register the handler in `functions/crawler_kit/entrypoints/cli/typer/greet/__init__.py`:

```python
from typer import Typer
from crawler_kit.modules.greet.presentation.cli.handlers.handle_hello import (
    handle_hello,
)

greet = Typer(name="greet")
greet.command(name="hello")(handle_hello)
```

4. Register the `greet` CLI module in `functions/crawler_kit/entrypoints/cli/typer/__init__.py`:

```python
from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.entrypoints.cli.typer.greet import greet


def callback(context: Context):
    loop = ensure_event_loop()
    # context.obj = loop.run_until_complete(startup())
    # register(lambda: loop.run_until_complete(shutdown()))


app = Typer(callback=callback)
app.add_typer(greet)
```

---

### Run the CLI

```bash
python functions/main.py greet hello
```

Here's the English translation of your guide:

---

## Publish Message Demo

### Create `functions/crawler_kit/utils/google_cloud/publish_message.py`:

```python
from google.cloud.pubsub import PublisherClient
from crawler_kit.utils.google_cloud.credentials_from_env import credentials_from_env
from json import dumps
from asyncio import Future
from google.api_core.exceptions import AlreadyExists
from os import getenv

def publish_message(topic: str, payload: dict):
    pubsub = PublisherClient(credentials=credentials_from_env())
    name = str(f"projects/{getenv('PROJECT_ID')}/topics/{topic}")
    try:
        pubsub.create_topic(
            request=dict(name=name),
        )
    except AlreadyExists:
        pass
    data = bytes(dumps(payload), "utf-8")
    future: Future = pubsub.publish(name, data)
    return future.result()
```

### Implementation of `credentials_from_env` (`functions/crawler_kit/utils/google_cloud/credentials_from_env.py`):

```python
from google.oauth2.service_account import Credentials
from os import getenv

def credentials_from_env():
    credentials = Credentials.from_service_account_info(
        dict(
            type="service_account",
            project_id=getenv("PROJECT_ID"),
            client_email=getenv("CLIENT_EMAIL"),
            private_key=getenv("PRIVATE_KEY"),
            token_uri="https://oauth2.googleapis.com/token",
        )
    )
    return credentials
```

### Slight modification to `functions/crawler_kit/modules/greet/presentation/cli/handlers/handle_hello.py`:

```python
from click.core import Context
from crawler_kit.utils.google_cloud.publish_message import publish_message

def handle_hello(context: Context):
    topic = "test"
    payload = dict(message="hello, world")
    print(publish_message(topic, payload))
```

### Verify the functionality

Before testing, make sure the Pub/Sub emulator is running:

```bash
make dev
```

### Run the test

```bash
python functions/main.py greet hello
```

If it runs successfully, you'll see a number in the output. That number is the message ID assigned by the emulator. If the emulator is restarted, it will reset the counter.
