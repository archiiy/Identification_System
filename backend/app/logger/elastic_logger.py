import logging
from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch(
    "http://localhost:9200"
)


logger=logging.getLogger("verification")

logger.setLevel(
    logging.INFO
)

file=logging.FileHandler(
    "verification.log"
)

formatter=logging.Formatter(
"%(asctime)s %(levelname)s %(message)s"
)

file.setFormatter(
formatter
)

logger.addHandler(
file
)

def push_log(
    data
):

    try:

        data[
            "timestamp"
        ] = datetime.utcnow(
        ).isoformat()

        es.index(

            index=
            "verification-logs",

            document=
            data

        )

    except Exception as e:

        logger.error(
f"Elastic Error: {e}"
)