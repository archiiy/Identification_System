import time
import uuid

from app.logger.elastic_logger import (logger,push_log)

async def logging_middleware(
    request,
    call_next
):

    trace_id = str(
        uuid.uuid4()
    )

    try:
        body = await request.body()
        body = body.decode()

    except:
        body = "cannot_read"

    start = time.time()

    logger.info(
f"""
REQUEST

trace={trace_id}

endpoint={request.url.path}

method={request.method}

body={body}
"""
)

    try:

        response = await call_next(
            request
        )

    except Exception as e:

        duration = (
            time.time()-start
        )*1000

        logger.exception(
f"""
ERROR

trace={trace_id}

endpoint={request.url.path}

method={request.method}

error={str(e)}

duration={duration:.0f}ms
"""
        )

        push_log({

            "trace":
            trace_id,

            "endpoint":
            request.url.path,

            "method":
            request.method,

            "error":
            str(e),

            "duration(ms)":
            duration

        })

        raise

    duration = (
        time.time()-start
    )*1000

    logger.info(
f"""
RESPONSE

trace={trace_id}

status={response.status_code}

duration={duration:.0f}ms
"""
)

    push_log({

    "trace":
    trace_id,

    "endpoint":
    request.url.path,

    "method":
    request.method,

    "status":
    response.status_code,

    "duration(ms)":
    duration,

    "body":
    body

})
    response.headers[
        "X-Trace-ID"
    ] = trace_id

    return response