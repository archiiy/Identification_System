from fastapi import FastAPI

from app.routes.upload import router
from app.routes.selfie import router as selfie_router
from app.routes.liveness import router as live_router
from fastapi.middleware.cors import CORSMiddleware
from app.logger.elastic_logger import logger
from app.middleware.logging_middleware import logging_middleware

logger.info(
    "Backend started"
)


app = FastAPI()

app.middleware(
"http"
)(
logging_middleware
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:4200"

    ],

    allow_credentials=True,

    allow_methods=[

        "*"

    ],

    allow_headers=[

        "*"

    ]

)


app.include_router(
    router
)

app.include_router(
    selfie_router
)

app.include_router(
    live_router
)




@app.get("/")
def home():

    return {

        "message":
        "Backend Running"

    }

