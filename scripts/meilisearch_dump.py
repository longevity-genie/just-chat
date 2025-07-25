from meilisearch import Client
from meilisearch.errors import MeilisearchApiError
from meilisearch.models.task import TaskInfo
import time
import os
import typer
from typing import List, Optional
from datetime import datetime

def enumerate_dumps_folder(dumps_path: str = "./dumps") -> List[str]:
    """List all files in the dumps folder."""
    if not os.path.exists(dumps_path):
        print(f"Dumps folder '{dumps_path}' does not exist")
        return []
    
    files = []
    for item in os.listdir(dumps_path):
        item_path = os.path.join(dumps_path, item)
        if os.path.isfile(item_path):
            files.append(item)
    
    return files

def print_dumps_status(dumps_path: str = "./dumps", label: str = "") -> None:
    """Print the current status of the dumps folder."""
    files = enumerate_dumps_folder(dumps_path)
    print(f"\n{label} - Files in {dumps_path}:")
    if files:
        for file in files:
            file_path = os.path.join(dumps_path, file)
            size = os.path.getsize(file_path)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  - {file} ({size} bytes, modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("  (no files found)")
    print()

def find_new_dump(dumps_path: str, start_time: float, timeout_seconds: int = 30) -> Optional[str]:
    """Monitor dumps folder for new files created after start_time."""
    print(f"Monitoring {dumps_path} for new dump files...")
    
    end_time = time.time() + timeout_seconds
    
    while time.time() < end_time:
        if os.path.exists(dumps_path):
            for item in os.listdir(dumps_path):
                item_path = os.path.join(dumps_path, item)
                if os.path.isfile(item_path):
                    file_mtime = os.path.getmtime(item_path)
                    if file_mtime > start_time:
                        print(f"Found new dump: {item}")
                        return item
        
        time.sleep(1)  # Check every second
    
    print("No new dump file detected within timeout period")
    return None

def initiate_dump(client: Client) -> Optional[TaskInfo]:
    try:
        task = client.create_dump()
        print(f"Dump status: {task.status}")
        print(f"Dump task id: {task.task_uid}")
        return task
    except MeilisearchApiError as e:
        print(f"Error creating dump: {e}")
        return None

def wait_for_dump(client: Client, task: TaskInfo, timeout_seconds: int = 600) -> Optional[TaskInfo]:
    try:
        # Convert seconds to milliseconds for the API
        timeout_ms = timeout_seconds * 1000
        updated_task = client.wait_for_task(task.task_uid, timeout_in_ms=timeout_ms)
        print(f"Dump completed with status: {updated_task.status}")
        return updated_task
    except MeilisearchApiError as e:
        print(f"Error waiting for dump: {e}")
        return None

def get_client(host: str = "localhost", port: int = 7700, api_key: Optional[str] = None) -> Client:
    """Get MeiliSearch client with configurable host, port, and API key."""
    return Client(f"http://{host}:{port}", api_key=api_key)

def get_meilisearch_host() -> str:
    """Get MeiliSearch host from environment variable or default."""
    return os.getenv("MEILISEARCH_HOST", "localhost")

def get_meilisearch_port() -> int:
    """Get MeiliSearch port from environment variable or default."""
    return int(os.getenv("MEILISEARCH_PORT", "7700"))

def get_meilisearch_key() -> str:
    """Get MeiliSearch master key from environment variable or default."""
    return os.getenv("MEILI_MASTER_KEY", "fancy_master_key")

def main(
    host: Optional[str] = typer.Option(
        None, 
        "--host", 
        "-h", 
        help="MeiliSearch host (overrides MEILISEARCH_HOST env var)"
    ),
    port: Optional[int] = typer.Option(
        None, 
        "--port", 
        "-p", 
        help="MeiliSearch port (overrides MEILISEARCH_PORT env var)"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        "--api-key", 
        "-k", 
        help="MeiliSearch master key (overrides MEILI_MASTER_KEY env var)"
    ),
    dumps_path: str = typer.Option(
        "./dumps", 
        "--dumps-path", 
        "-d", 
        help="Path to dumps folder for monitoring"
    ),
    dump_path: Optional[str] = typer.Option(
        None,
        "--dump-path",
        help="Path where MeiliSearch actually creates dumps (overrides --dumps-path)"
    )
) -> None:
    """Create a MeiliSearch dump."""
    # Start timing the entire process
    process_start_time = time.time()
    
    # Determine host: CLI arg > env var > default
    if host is None:
        host = get_meilisearch_host()
    
    # Determine port: CLI arg > env var > default
    if port is None:
        port = get_meilisearch_port()
    
    # Determine API key: CLI arg > env var > default
    if api_key is None:
        api_key = get_meilisearch_key()
    
    # Use dump_path override if provided
    actual_dump_path = dump_path if dump_path is not None else dumps_path
    
    print(f"Using MeiliSearch at: {host}:{port}")
    print(f"Using API key: {'*' * (len(api_key) - 4)}{api_key[-4:] if len(api_key) > 4 else '****'}")
    print(f"Monitoring dumps in: {actual_dump_path}")
    
    # Enumerate dumps folder before creating dump
    print_dumps_status(actual_dump_path, "BEFORE DUMP")
    
    # Record start time for new dump detection
    start_time = time.time()
    
    client = get_client(host, port, api_key)
    
    print(f"Initiating dump at {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}...")
    task = initiate_dump(client)
    
    if task is None:
        print("Failed to initiate dump")
        return
    
    # Wait for dump to complete (5 minutes timeout)
    dump_start_time = time.time()
    completed_task = wait_for_dump(client, task, timeout_seconds=300)
    dump_end_time = time.time()
    
    if completed_task is None:
        print("Failed to complete dump")
        return
    
    # Calculate dump duration
    dump_duration = dump_end_time - dump_start_time
    
    # Check if dump was successful
    if completed_task.status == "succeeded":
        print(f"Dump created successfully in {dump_duration:.2f} seconds!")
        
        # Find the new dump file
        new_dump = find_new_dump(actual_dump_path, start_time)
        if new_dump:
            file_path = os.path.join(actual_dump_path, new_dump)
            size = os.path.getsize(file_path)
            print(f"New dump created: {new_dump} ({size} bytes)")
        
        # Show final status
        print_dumps_status(actual_dump_path, "AFTER SUCCESSFUL DUMP")
        
        # Calculate and display total process time
        process_end_time = time.time()
        total_duration = process_end_time - process_start_time
        print(f"\nTotal process time: {total_duration:.2f} seconds")
        print(f"Dump operation time: {dump_duration:.2f} seconds")
        print(f"Completed at {datetime.fromtimestamp(process_end_time).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show reset tip after successful dump
        print("\n" + "="*60)
        print("💡 TIP: To force re-import of this dump:")
        print("   # For Docker:")
        print("   docker compose down")
        print("   USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up -V")
        print("   # For Podman:")
        print("   podman compose down")
        print("   podman compose up -V")
        print("   # -V recreates anonymous volumes (MeiliSearch), keeps named volumes (MongoDB)")
        print("="*60)
    else:
        print(f"Dump failed with status: {completed_task.status}")
        if hasattr(completed_task, 'error'):
            print(f"Error details: {completed_task.error}")
        
        # Show timing even for failed dumps
        process_end_time = time.time()
        total_duration = process_end_time - process_start_time
        print(f"\nTotal process time: {total_duration:.2f} seconds")
        print(f"Dump operation time: {dump_duration:.2f} seconds")
        


if __name__ == "__main__":
    typer.run(main)