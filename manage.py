import click
from app import create_app

app=create_app()

@app.cli.command("create-db")
def create_db():
    pass

if __name__ == '__main__':
    app.run()