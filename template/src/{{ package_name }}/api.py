"""FastAPI HTTP layer; work executes out-of-process in ARQ."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field
from redis.exceptions import RedisError

from .db import count_messages, init_db
from .queue import new_pool


class JobRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class JobReceipt(BaseModel):
    job_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(init_db)
    app.state.redis = await new_pool()
    try:
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(
    title="Background Webservice",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness endpoint. Redis connectivity is checked during startup."""
    return {"status": "ok"}


@app.get("/messages/count")
async def message_count() -> dict[str, int]:
    count = await asyncio.to_thread(count_messages)
    return {"count": count}


@app.post("/jobs", response_model=JobReceipt, status_code=status.HTTP_202_ACCEPTED)
async def enqueue_job(payload: JobRequest, request: Request) -> JobReceipt:
    """Queue a job without blocking the API on its execution."""
    try:
        job = await request.app.state.redis.enqueue_job("save_message", payload.message)
    except (OSError, RedisError) as exc:
        raise HTTPException(status_code=503, detail="Job queue unavailable") from exc
    if job is None:
        raise HTTPException(status_code=503, detail="Job was not accepted")
    return JobReceipt(job_id=job.job_id)
