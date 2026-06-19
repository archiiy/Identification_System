import logging

from elasticsearch import (
    Elasticsearch
)

from datetime import (
    datetime
)


ENABLE_ELASTIC = False


es = None

if ENABLE_ELASTIC:

    try:

        es = Elasticsearch(
            "http://localhost:9200"
        )

    except:

        es = None


logger = logging.getLogger(
    "verification"
)

logger.setLevel(
    logging.INFO
)

file = logging.FileHandler(
    "verification.log"
)

formatter = logging.Formatter(
"%(asctime)s %(levelname)s %(message)s"
)

file.setFormatter(
    formatter
)

logger.addHandler(
    file)


def push_log(
    data
):

    try:

        data[
            "timestamp"
        ] = datetime.utcnow(
        ).isoformat()

        logger.info(
            str(data)
        )

        if (
            ENABLE_ELASTIC
            and
            es
        ):

            es.index(

                index=
                "verification-logs",

                document=
                data

            )

    except Exception as e:

        logger.error(
f"Log Error: {e}"
)