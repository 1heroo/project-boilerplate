"""Liveness endpoint for the taskiq worker, which otherwise has no HTTP.

Every worker child process binds the same port with SO_REUSEPORT.
"""
import asyncio

_OK = (
    b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    b'Content-Length: 16\r\nConnection: close\r\n\r\n{"status": "ok"}'
)
_NOT_FOUND = b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'
_READ_TIMEOUT_SECONDS = 2.0


async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        request_line = await asyncio.wait_for(reader.readline(), _READ_TIMEOUT_SECONDS)
        method, path, *_ = request_line.decode('latin-1').split(' ') + ['', '']
        writer.write(_OK if (method, path) == ('GET', '/health/check') else _NOT_FOUND)
        await writer.drain()
    except (TimeoutError, ConnectionError):
        pass
    finally:
        writer.close()


async def start_health_server(host: str, port: int) -> asyncio.Server:
    return await asyncio.start_server(_handle, host, port, reuse_port=True)
