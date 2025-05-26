import pandas as pd
import logging

def ingest_data(
    client, data: pd.DataFrame, db: str, coll: str
) -> None:
    collection = client[db][coll]
    collection.drop()
    collection.insert_many(data.to_dict("records"))
    logging.info(f"📥 Inserted {len(data)} documents into {db}.{coll}")