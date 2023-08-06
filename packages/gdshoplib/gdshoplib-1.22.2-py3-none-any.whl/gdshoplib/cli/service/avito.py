from datetime import datetime

import typer

from gdshoplib.core.ecosystem import Ecosystem
from gdshoplib.services.avito.avito import Avito

app = typer.Typer()


@app.command()
def access_code():
    print(Avito().get_access_token())


@app.command()
def upload(infinity: bool = True):
    last_edited = datetime.utcnow() if infinity else None
    ecosystem = Ecosystem()
    while not last_edited or infinity:
        new_last_edited = None

        for message in Avito().get_statistic():
            ecosystem.send_message("avito", data=message, message_type="stats")

        if new_last_edited:
            last_edited = new_last_edited


# if __name__ == "__main__":
#     app()
