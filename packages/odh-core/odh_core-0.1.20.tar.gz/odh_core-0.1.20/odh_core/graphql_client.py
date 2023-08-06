from gql import Client as gql_client
from gql.transport.aiohttp import AIOHTTPTransport
from gql import gql
from graphql import DocumentNode
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# # Tracelog for aiohttp
# # from: https://stackoverflow.com/a/64954315
# async def on_request_end(session, context, params):
#     trace_log = logging.getLogger("aiohttp.client")
#     trace_log.debug(
#         f"Request: {params.method} {params.url} "
#         f"Response: status:{params.response.status} {await params.response.text()}"
#     )

# trace_config = aiohttp.TraceConfig()
# trace_config.on_request_end.append(on_request_end)

# session = (
#     aiohttp.ClientSession(
#         base_url="https://graph.microsoft.com/",
#         headers=settings.jsonheaders,
#         trust_env=True,
#         # log all requests made by the session
#         trace_configs=[trace_config],
#     ),
# )


class GraphQLClient:
    """GraphQL client with session management

    .. todo::
        - Add support for trace logging

    """

    def __init__(
        self, url: str, headers: dict = None, ssl: bool = True, timeout: int = 10
    ):
        """Initialize GraphQL client

        Args:
            url (str): GraphQL server URL
            headers (dict, optional): HTTP headers to send with each request
            ssl (bool, optional): Verify SSL certificate
            timeout (int, optional): Timeout in seconds

        """
        self._client = gql_client(
            transport=AIOHTTPTransport(
                url=url,
                headers=headers,
                ssl=ssl,
                timeout=timeout,
            ),
            fetch_schema_from_transport=True,
        )
        self._session = None

    async def connect_async(self):
        self._session = await self._client.connect_async(reconnecting=True)
        log.info(f"Connected to GraphQL server: {self._client.transport.url}")

    async def close_async(self):
        await self._client.close_async()
        log.info(f"Connection closed to GraphQL server: {self._client.transport.url}")

    async def execute_async(self, query: DocumentNode, variable_values=None):
        """Execute a GraphQL query"""
        if not isinstance(query, DocumentNode):
            raise TypeError("query must be a gql object")

        if variable_values is None:
            result = await self._session.execute(query)
        else:
            result = await self._session.execute(query, variable_values)
        return result

    async def lock_acquire_async(self):
        """
        Create a lock in the Hasura DB, lock will release after TTL expires
        or when release is called
        """
        query = gql(
            """
            mutation InsertLock($id: String = "", $ttl_seconds: Int = 30) {
                insert_lock_table(objects: {id: $id, ttl_seconds: $ttl_seconds},
                on_conflict: {constraint: lock_table_pkey}) {
                    affected_rows
                }
            }
            """
        )
        variables = {"id": self.lock_name, "ttl_seconds": self.ttl_seconds}
        lock = await self._client.execute_async(
            query, variable_values=variables
        )
        if lock["insert_lock_table"]["affected_rows"] == 1:
            return True
        else:
            return False

    async def lock_refresh_async(self):
        """
        Create a lock in the Hasura DB, lock will release after TTL expires
        or when release is called
        """
        query = gql(
            """
            mutation RefreshLock($id: String = "", $created_at: timestamptz = now) {
                update_lock_table_by_pk(pk_columns: {id: $id}, _set: {created_at: $created_at}) {
                    id
                }
            }
            """
        )
        variables = {"id": self.lock_name}
        lock = await self._client.execute_async(
            query, variable_values=variables
        )
        if lock["update_lock_table_by_pk"]["id"] == self.lock_name:
            return True
        else:
            return False

    async def lock_release_async(self):
        """
        Release the lock in the Hasura DB
        """
        query = gql(
            """
            mutation DeleteLock($id: String = "") {
                delete_lock_table(where: {id: {_eq: $id}}) {
                    affected_rows
                }
            }
            """
        )
        variables = {"id": self.lock_name}
        lock = await self._client.execute_async(
            query, variable_values=variables
        )
        if lock["delete_lock_table"]["affected_rows"] == 1:
            return True
        else:
            return False
