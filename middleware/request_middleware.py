import logging
import time
import uuid

from fastapi import Request


logger = logging.getLogger("enterprise_business_management_system")


async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    response = await call_next(request)

    execution_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Execution-Time"] = f"{execution_time:.6f}"

    logger.info(
        "request_id=%s method=%s path=%s status_code=%s execution_time=%.6fs",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        execution_time,
    )

    return response
