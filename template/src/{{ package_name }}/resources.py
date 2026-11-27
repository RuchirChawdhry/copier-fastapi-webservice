"""Resource measurements using psutil, without background sampling."""

import psutil


def resource_snapshot() -> dict[str, int]:
    memory = psutil.virtual_memory()
    return {
        "cpu_logical": psutil.cpu_count() or 0,
        "system_memory_total_bytes": memory.total,
        "system_memory_available_bytes": memory.available,
        "cli_rss_bytes": psutil.Process().memory_info().rss,
    }
