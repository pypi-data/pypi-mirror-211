from __future__ import annotations

import asyncio
import functools
import typing as t

import pandas as pd
from fastapi import APIRouter, Body, Depends, Request

from sqlmesh.core.context import Context
from sqlmesh.core.snapshot.definition import SnapshotChangeCategory
from sqlmesh.utils.errors import PlanError
from web.server import models
from web.server.exceptions import ApiException
from web.server.settings import get_loaded_context
from web.server.utils import (
    ArrowStreamingResponse,
    df_to_pyarrow_bytes,
    run_in_executor,
)

router = APIRouter()


@router.post("/apply", response_model=models.ApplyResponse)
async def apply(
    request: Request,
    context: Context = Depends(get_loaded_context),
    environment: t.Optional[str] = Body(None),
    plan_dates: t.Optional[models.PlanDates] = None,
    plan_options: models.PlanOptions = models.PlanOptions(),
    categories: t.Optional[t.Dict[str, SnapshotChangeCategory]] = None,
) -> models.ApplyResponse:
    """Apply a plan"""

    if hasattr(request.app.state, "task") and not request.app.state.task.done():
        raise ApiException(
            message="Plan/apply is already running",
            origin="API -> commands -> apply",
        )

    plan_func = functools.partial(
        context.plan,
        environment=environment,
        no_prompts=True,
        start=plan_dates.start if plan_dates else None,
        end=plan_dates.end if plan_dates else None,
        skip_tests=plan_options.skip_tests,
        no_gaps=plan_options.no_gaps,
        restate_models=plan_options.restate_models,
        create_from=plan_options.create_from,
        skip_backfill=plan_options.skip_backfill,
        forward_only=plan_options.forward_only,
        no_auto_categorization=plan_options.no_auto_categorization,
    )
    request.app.state.task = task = asyncio.create_task(run_in_executor(plan_func))
    try:
        plan = await task
    except PlanError as e:
        raise ApiException(
            message=str(e),
            origin="API -> commands -> apply",
        )

    if categories is not None:
        for new, _ in plan.context_diff.modified_snapshots.values():
            if plan.is_new_snapshot(new) and new.name in categories:
                plan.set_choice(new, categories[new.name])

    request.app.state.task = asyncio.create_task(run_in_executor(context.apply, plan))
    if not plan.requires_backfill or plan_options.skip_backfill:
        await request.app.state.task

    return models.ApplyResponse(
        type=models.ApplyType.backfill if plan.requires_backfill else models.ApplyType.virtual
    )


@router.post("/evaluate")
async def evaluate(
    options: models.EvaluateInput,
    context: Context = Depends(get_loaded_context),
) -> ArrowStreamingResponse:
    """Evaluate a model with a default limit of 1000"""
    try:
        df = context.evaluate(
            options.model,
            start=options.start,
            end=options.end,
            latest=options.latest,
            limit=options.limit,
        )
    except Exception:
        raise ApiException(
            message="Unable to evaluate a model",
            origin="API -> commands -> evaluate",
        )

    if not isinstance(df, pd.DataFrame):
        df = df.toPandas()
    return ArrowStreamingResponse(df_to_pyarrow_bytes(df))


@router.post("/fetchdf")
async def fetchdf(
    sql: str = Body(embed=True),
    context: Context = Depends(get_loaded_context),
) -> ArrowStreamingResponse:
    """Fetches a dataframe given a sql string"""
    try:
        df = context.fetchdf(sql)
    except Exception:
        raise ApiException(
            message="Unable to fetch a dataframe from the given sql string",
            origin="API -> commands -> fetchdf",
        )
    return ArrowStreamingResponse(df_to_pyarrow_bytes(df))


@router.post("/render", response_model=models.Query)
async def render(
    options: models.RenderInput,
    context: Context = Depends(get_loaded_context),
) -> models.Query:
    """Renders a model's query, optionally expanding referenced models"""
    snapshot = context.snapshots.get(options.model)

    if not snapshot:
        raise ApiException(
            message="Unable to find a model",
            origin="API -> commands -> render",
        )

    try:
        rendered = context.render(
            snapshot,
            start=options.start,
            end=options.end,
            latest=options.latest,
            expand=options.expand,
        )
    except Exception:
        raise ApiException(
            message="Unable to render a model query",
            origin="API -> commands -> render",
        )

    dialect = options.dialect or context.config.dialect

    return models.Query(sql=rendered.sql(pretty=options.pretty, dialect=dialect))
