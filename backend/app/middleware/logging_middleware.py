import time
import uuid

from app.logger.elastic_logger import (
    logger,
    push_log
)


async def logging_middleware(
    request,
    call_next
):

    trace_id = str(
        uuid.uuid4()
    )

    try:
        content_type = request.headers.get(
            "content-type",
            ""
        )

        if "multipart/form-data" in content_type:
            body = "file_upload"

        else:
            body = (
                await request.body()
            ).decode()

    except:
        body = "unknown"

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
            time.time()
            -
            start
        ) * 1000

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

            "event":
            "api_request",

            "trace":
            trace_id,

            "endpoint":
            request.url.path,

            "method":
            request.method,

            "request":
            (
                "file_upload"
                if body
                and
                body != "cannot_read"
                else "empty"
            ),

            "response":
            500,

            "verification":
            "failed",

            "error":
            str(e),

            "duration(ms)":
            round(duration)

        })

        raise

    duration = (
        time.time()
        -
        start
    ) * 1000

    logger.info(
f"""
RESPONSE

trace={trace_id}

status={response.status_code}

duration={duration:.0f}ms
"""
    )

    push_log({

        "event":
        "api_request",

        "trace":
        trace_id,

        "endpoint":
        request.url.path,

        "method":
        request.method,

        "request":
        (
            "file_upload"
            if body
            and
            body != "cannot_read"
            else "empty"
        ),

        "response":
        response.status_code,

        "result":
        (
            "passed"
            if response.status_code < 400
            else "failed"
        ),

        "error":
        None,

        "duration(ms)":
        round(duration)

    })

    response.headers[
        "X-Trace-ID"
    ] = trace_id

    return response