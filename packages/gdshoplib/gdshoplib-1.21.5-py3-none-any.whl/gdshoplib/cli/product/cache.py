import time
from datetime import datetime
from multiprocessing import Pool
from typing import List, Optional

import orjson as json
import typer
from kafka import KafkaProducer
from kafka.errors import KafkaError
from loguru import logger
from pydantic import BaseModel

from gdshoplib.apps.products.product import Product
from gdshoplib.core.settings import NotionSettings
from gdshoplib.packages.cache import KeyDBCache
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.notion import Notion

app = typer.Typer()


@app.command()
def clean(id: Optional[str] = typer.Option(None)):
    # TODO: сделать удаление по ID
    KeyDBCache().clean(r"[blocks|pages|databases]*")


@app.command()
def listen(topic: List[str]):
    for message in KeyDBCache().subscribe(topic):
        print(message)


@app.command()
def upload(page_id: Optional[str] = typer.Option(None), infinity: bool = True):
    producer = KafkaProducer(
        bootstrap_servers=NotionSettings().KAFKA_BROKER,
        value_serializer=lambda m: json.dumps(m),
        request_timeout_ms=1000,
    )

    class Message(BaseModel):
        id: str
        data: dict
        version_md5: Optional[str]
        timestamp: str
        data_md5: Optional[str]
        parrent_id: str

        def send(self):
            # - Отправить в kafka
            future = producer.send(NotionSettings().KAFKA_TOPIC, self.dict())
            try:
                future.get(timeout=10)
            except KafkaError as e:
                # Decide what to do if produce request failed...
                logger.exception(e)

    # Загрузить в базу объекты
    # - Проитерироваться по списку страниц
    last_edited = None
    while not last_edited or infinity:
        new_last_edited = None
        for message in (
            [Notion().get_page(page_id), *Notion().get_blocks(page_id)]
            if page_id
            else Notion().all()
        ):
            page_last_edited = datetime.strptime(
                message["last_edited_time"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
            )
            if not new_last_edited:
                new_last_edited = page_last_edited

            if infinity and last_edited and page_last_edited < last_edited:
                break

            Message(
                id=message["id"],
                data=message,
                parrent_id=message["parent"][message["parent"]["type"]],
                timestamp=str(time.time()),
            ).send()
            logger.info(f"{message['object']}: {message['id']}")

        last_edited = new_last_edited


@app.command()
def warm(
    only_exists: bool = typer.Option(False),
    single: bool = typer.Option(False),
    only_edited: bool = typer.Option(True),
    sku: Optional[str] = typer.Option(None),
    loop_iteration: Optional[int] = typer.Option(None),
):
    while True:
        if sku:
            cache_warm_func(Product.get(sku).id)
            return

        if single:
            with Database(
                Product.SETTINGS.PRODUCT_DB, notion=Notion(caching=True)
            ) as database:
                params = {}
                if only_edited and database.get_update_time():
                    print(f"Фильтрация от даты: {database.get_update_time()}")
                    params = database.edited_filter()

                for product in database.pages(params=params):
                    skipped = False
                    if only_exists:
                        if KeyDBCache().exists(product["id"]):
                            print(f"{product['id']}: SKIPPED")
                            skipped = True

                    if not skipped:
                        cache_warm_func(product["id"])
        else:
            with Pool(3) as p:
                with Database(
                    Product.SETTINGS.PRODUCT_DB, notion=Notion(caching=True)
                ) as database:
                    params = {}
                    if only_edited and database.get_update_time():
                        print(f"Фильтрация от даты: {database.get_update_time()}")
                        params = database.edited_filter()

                    for product in database.pages(params=params):
                        skipped = False
                        if only_exists:
                            if KeyDBCache().exists(product["id"]):
                                print(f"{product['id']}: SKIPPED")
                                skipped = True

                        if not skipped:
                            p.apply_async(cache_warm_func, (product["id"],))
                p.close()
                p.join()

        if loop_iteration:
            print("-" * 20)
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def count():
    print(KeyDBCache().count())


@app.command()
def check(single: bool = typer.Option(False)):
    if single:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            cache_check_action(product["id"])
    else:
        with Pool(3) as p:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                p.apply_async(cache_check_action, (product["id"],))
            p.close()
            p.join()


#####


def cache_check_action(id):
    for block in Notion().get_blocks(id):
        exists = KeyDBCache().exists(block["id"])
        print(f"{block['id']}: {exists}")


def cache_warm_func(id):
    product = Product(id)
    try:
        product.warm()
    except AttributeError:
        print(f"!= Пропущено {product.sku}: {product.last_edited_time}")
    else:
        print(f"{product.sku}: {product.last_edited_time}")
