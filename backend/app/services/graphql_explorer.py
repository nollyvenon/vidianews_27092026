"""A read-only GraphQL schema over published, publicly visible content, executed with graphql-core.

Only content that anyone could read on the site is exposed: published status and public access level.
Resolvers share one database session, which cannot run two statements at once, so every resolver takes
the request's lock before touching it.
"""

import asyncio
from typing import Any, Dict, List, Optional

from graphql import (
    GraphQLArgument,
    GraphQLField,
    GraphQLInt,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    graphql,
)
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Content, ContentAccessLevel, ContentStatus

MAX_QUERY_LENGTH = 4000
MAX_CONTENT_LIMIT = 100
DEFAULT_CONTENT_LIMIT = 10


def _publicly_visible():
    return and_(
        Content.status == ContentStatus.PUBLISHED,
        Content.access_level == ContentAccessLevel.PUBLIC,
    )


def _content_payload(row: Content) -> Dict[str, Any]:
    return {
        "id": row.id,
        "title": row.title,
        "slug": row.slug,
        "description": row.description,
        "viewsCount": row.views_count or 0,
        "publishedAt": row.published_at.isoformat() if row.published_at else None,
    }


async def _resolve_content(_root, info, id: int) -> Optional[Dict[str, Any]]:
    session: AsyncSession = info.context["session"]
    async with info.context["lock"]:
        row = (await session.execute(
            select(Content).where(Content.id == id, _publicly_visible())
        )).scalar_one_or_none()
    return _content_payload(row) if row else None


async def _resolve_contents(_root, info, limit: int = DEFAULT_CONTENT_LIMIT) -> List[Dict[str, Any]]:
    session: AsyncSession = info.context["session"]
    bounded = min(max(limit, 1), MAX_CONTENT_LIMIT)
    async with info.context["lock"]:
        rows = (await session.execute(
            select(Content)
            .where(_publicly_visible())
            .order_by(Content.published_at.desc().nulls_last(), Content.id.desc())
            .limit(bounded)
        )).scalars().all()
    return [_content_payload(row) for row in rows]


CONTENT_TYPE = GraphQLObjectType(
    "Content",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "title": GraphQLField(GraphQLNonNull(GraphQLString)),
        "slug": GraphQLField(GraphQLNonNull(GraphQLString)),
        "description": GraphQLField(GraphQLString),
        "viewsCount": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "publishedAt": GraphQLField(GraphQLString),
    },
)

QUERY_TYPE = GraphQLObjectType(
    "Query",
    lambda: {
        "content": GraphQLField(
            CONTENT_TYPE,
            args={"id": GraphQLArgument(GraphQLNonNull(GraphQLInt))},
            resolve=_resolve_content,
        ),
        "contents": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(CONTENT_TYPE))),
            args={"limit": GraphQLArgument(GraphQLInt, default_value=DEFAULT_CONTENT_LIMIT)},
            resolve=_resolve_contents,
        ),
    },
)

SCHEMA = GraphQLSchema(query=QUERY_TYPE)


def schema_summary() -> List[Dict[str, Any]]:
    """The object types of the schema with each field's name and type, for the explorer's documentation panel."""
    types = []
    for name, graphql_type in sorted(SCHEMA.type_map.items()):
        if name.startswith("__") or not isinstance(graphql_type, GraphQLObjectType):
            continue
        types.append({
            "name": name,
            "fields": [
                {"name": field_name, "type": str(field.type)}
                for field_name, field in graphql_type.fields.items()
            ],
        })
    return types


async def run_query(session: AsyncSession, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute a query. Syntax and validation problems come back in `errors`, as the GraphQL spec requires."""
    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Query is longer than {MAX_QUERY_LENGTH} characters")
    result = await graphql(
        SCHEMA,
        query,
        context_value={"session": session, "lock": asyncio.Lock()},
        variable_values=variables,
    )
    envelope: Dict[str, Any] = {"data": result.data}
    if result.errors:
        envelope["errors"] = [{"message": error.message} for error in result.errors]
    return envelope
