"""Provides a simple stateless caching system."""
from __future__ import annotations

import asyncio
import functools
import json
import time

from music_assistant.helpers.database import TABLE_CACHE
from music_assistant.helpers.typing import MusicAssistant


class Cache:
    """Basic cache using both memory and database."""

    def __init__(self, mass: MusicAssistant) -> None:
        """Initialize our caching class."""
        self.mass = mass
        self.logger = mass.logger.getChild("cache")
        self._mem_cache = {}

    async def setup(self) -> None:
        """Async initialize of cache module."""
        self.__schedule_cleanup_task()

    async def get(self, cache_key, checksum="", default=None):
        """
        Get object from cache and return the results.

        cache_key: the (unique) name of the cache object as reference
        checkum: optional argument to check if the checksum in the
                    cacheobject matches the checkum provided
        """
        cur_time = int(time.time())
        checksum = self._get_checksum(checksum)

        # try memory cache first
        cache_data = self._mem_cache.get(cache_key)
        if (
            cache_data
            and (not checksum or cache_data[1] == checksum)
            and cache_data[2] >= cur_time
        ):
            return cache_data[0]
        # fall back to db cache
        if db_row := await self.mass.database.get_row(TABLE_CACHE, {"key": cache_key}):
            if (
                not checksum
                or db_row["checksum"] == checksum
                and db_row["expires"] >= cur_time
            ):
                try:
                    data = await asyncio.get_running_loop().run_in_executor(
                        None, json.loads, db_row["data"]
                    )
                except Exception as exc:  # pylint: disable=broad-except
                    self.logger.exception(
                        "Error parsing cache data for %s", cache_key, exc_info=exc
                    )
                else:
                    # also store in memory cache for faster access
                    if cache_key not in self._mem_cache:
                        self._mem_cache[cache_key] = (
                            data,
                            db_row["checksum"],
                            db_row["expires"],
                        )
                    return data
        return default

    async def set(self, cache_key, data, checksum="", expiration=(86400 * 30)):
        """Set data in cache."""
        checksum = self._get_checksum(checksum)
        expires = int(time.time() + expiration)
        self._mem_cache[cache_key] = (data, checksum, expires)
        if (expires - time.time()) < 3600 * 4:
            # do not cache items in db with short expiration
            return
        data = await asyncio.get_running_loop().run_in_executor(None, json.dumps, data)
        await self.mass.database.insert_or_replace(
            TABLE_CACHE,
            {"key": cache_key, "expires": expires, "checksum": checksum, "data": data},
        )

    async def delete(self, cache_key):
        """Delete data from cache."""
        self._mem_cache.pop(cache_key, None)
        await self.mass.database.delete(TABLE_CACHE, {"key": cache_key})

    async def auto_cleanup(self):
        """Sceduled auto cleanup task."""
        # for now we simply reset the memory cache
        self._mem_cache = {}
        cur_timestamp = int(time.time())
        for db_row in await self.mass.database.get_rows(TABLE_CACHE):
            # clean up db cache object only if expired
            if db_row["expires"] < cur_timestamp:
                await self.delete(db_row["key"])
        # compact db
        async with self.mass.database.get_db() as _db:
            await _db.execute("VACUUM")

    def __schedule_cleanup_task(self):
        """Schedule the cleanup task."""
        self.mass.add_job(self.auto_cleanup(), "Cleanup cache")
        # reschedule self
        self.mass.loop.call_later(3600, self.__schedule_cleanup_task)

    @staticmethod
    def _get_checksum(stringinput):
        """Get int checksum from string."""
        if not stringinput:
            return 0
        stringinput = str(stringinput)
        return functools.reduce(lambda x, y: x + y, map(ord, stringinput))


def use_cache(expiration=86400 * 30):
    """Return decorator that can be used to cache a method's result."""

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            method_class = args[0]
            method_class_name = method_class.__class__.__name__
            cache_key_parts = [method_class_name, func.__name__]
            skip_cache = kwargs.pop("skip_cache", False)
            cache_checksum = kwargs.pop("cache_checksum", None)
            if len(args) > 1:
                cache_key_parts += args[1:]
            for key in sorted(kwargs.keys()):
                cache_key_parts.append(f"{key}{kwargs[key]}")
            cache_key = ".".join(cache_key_parts)
            cachedata = await method_class.cache.get(cache_key, checksum=cache_checksum)

            if not skip_cache and cachedata is not None:
                return cachedata
            result = await func(*args, **kwargs)
            await method_class.cache.set(
                cache_key, result, expiration=expiration, checksum=cache_checksum
            )
            return result

        return wrapped

    return wrapper
