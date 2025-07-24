if __name__ == "__main__":
    from dotenv import load_dotenv
    from os.path import exists
    from os import environ
    from crawler_kit.entrypoints.cli.typer import app

    environ["RUN_MODE"] = "cli"

    if exists("functions/.env"):
        load_dotenv("functions/.env", override=True)
    if exists("functions/.env.local"):
        load_dotenv("functions/.env.local", override=True)
    app()

else:
    pass
