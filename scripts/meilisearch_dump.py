#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "meilisearch>=0.15.0",  # Required for /export API (Meilisearch 1.16+)
#     "typer",
# ]
# ///

"""
MeiliSearch Dump & Export Tool

This script supports two modes:
1. DUMP MODE (Traditional): Creates backup files for manual transfer and import
2. EXPORT MODE (Meilisearch 1.16+): Direct instance-to-instance migration via API

REQUIREMENTS:
- Both source and target instances MUST be Meilisearch 1.16.0 or higher
- Python client meilisearch>=0.15.0 (automatically handled by script metadata)
- Network connectivity between instances during export

NEW EXPORT FEATURES:
- Direct migration without dump files
- Additive operations with conflict resolution  
- Selective export with index patterns and filters
- Settings override capabilities
- Configurable payload sizes for performance
- Automatic backup creation before/after export for data safety
- Import dump management with backup of existing files

Usage:
  # Export mode with auto-backup (recommended for 1.16+)
  uv run scripts/meilisearch_dump.py --export --target-url http://target:7700 --target-api-key key
  
  # Export with import dump update and no backup
  uv run scripts/meilisearch_dump.py --export --target-url http://target:7700 --target-api-key key --update-import --no-backup
  
  # Traditional dump mode with import update
  uv run scripts/meilisearch_dump.py --update-import
"""

from meilisearch import Client
from meilisearch.errors import MeilisearchApiError
from meilisearch.models.task import TaskInfo
import time
import os
import shutil
import typer
from typing import List, Optional, Dict, Any
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

def initiate_export(
    client: Client,
    target_url: str,
    target_api_key: str,
    payload_size: str = "50MiB",
    indexes: Optional[Dict[str, Dict[str, Any]]] = None
) -> Optional[TaskInfo]:
    """
    Initiate an export to another Meilisearch instance.
    
    Args:
        client: Source Meilisearch client
        target_url: Target instance URL
        target_api_key: Target instance API key
        payload_size: Payload size (e.g., "50MiB", "100MB")
        indexes: Optional dict of index patterns and their configs
                 Format: {"index_pattern": {"filter": "...", "overrideSettings": True/False}}
    """
    try:
        export_data = {
            "url": target_url,
            "apiKey": target_api_key,
            "payloadSize": payload_size
        }
        
        if indexes is not None:
            export_data["indexes"] = indexes
        
        task = client.http.post("export", export_data)
        print(f"Export status: {task.get('status', 'unknown')}")
        print(f"Export task id: {task.get('taskUid', 'unknown')}")
        
        # Create a TaskInfo-like object for compatibility
        task_info = TaskInfo(
            task_uid=task.get('taskUid'),
            index_uid=task.get('indexUid'),
            status=task.get('status'),
            type=task.get('type'),
            enqueued_at=task.get('enqueuedAt')
        )
        
        return task_info
    except MeilisearchApiError as e:
        print(f"Error creating export: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during export: {e}")
        return None

def wait_for_export(client: Client, task: TaskInfo, timeout_seconds: int = 600) -> Optional[TaskInfo]:
    """Wait for export task to complete."""
    try:
        # Convert seconds to milliseconds for the API
        timeout_ms = timeout_seconds * 1000
        updated_task = client.wait_for_task(task.task_uid, timeout_in_ms=timeout_ms)
        print(f"Export completed with status: {updated_task.status}")
        return updated_task
    except MeilisearchApiError as e:
        print(f"Error waiting for export: {e}")
        return None

def create_backup_dump(client: Client, dumps_path: str, label: str = "BACKUP") -> Optional[str]:
    """Create a backup dump and return the filename."""
    print(f"\n🔄 Creating {label} dump for data safety...")
    
    # Record start time for new dump detection
    start_time = time.time()
    
    task = initiate_dump(client)
    if task is None:
        print(f"❌ Failed to create {label} dump")
        return None
    
    # Wait for dump to complete
    completed_task = wait_for_dump(client, task, timeout_seconds=300)
    if completed_task is None or completed_task.status != "succeeded":
        print(f"❌ {label} dump failed")
        return None
    
    # Find the new dump file
    new_dump = find_new_dump(dumps_path, start_time)
    if new_dump:
        file_path = os.path.join(dumps_path, new_dump)
        size = os.path.getsize(file_path)
        print(f"✅ {label} dump created: {new_dump} ({size} bytes)")
        return new_dump
    else:
        print(f"⚠️ {label} dump created but file not found in monitoring")
        return None

def update_import_dump(dumps_path: str, latest_dump: str) -> bool:
    """Copy latest dump to just_chat_rag.dump with backup of existing."""
    import_dump_path = os.path.join(dumps_path, "just_chat_rag.dump")
    latest_dump_path = os.path.join(dumps_path, latest_dump)
    
    if not os.path.exists(latest_dump_path):
        print(f"❌ Latest dump not found: {latest_dump_path}")
        return False
    
    # Backup existing import dump if it exists
    if os.path.exists(import_dump_path):
        backup_path = f"{import_dump_path}.bak"
        if os.path.exists(backup_path):
            os.remove(backup_path)  # Remove old backup
        
        os.rename(import_dump_path, backup_path)
        print(f"📦 Backed up existing import dump to: just_chat_rag.dump.bak")
    
    # Copy latest dump to import location
    shutil.copy2(latest_dump_path, import_dump_path)
    print(f"✅ Updated import dump: just_chat_rag.dump")
    print(f"   Source: {latest_dump}")
    
    return True

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
    ),
    # Export-specific options
    export: bool = typer.Option(
        False,
        "--export",
        "-e",
        help="Use export mode instead of dump mode (Meilisearch 1.16+)"
    ),
    target_url: Optional[str] = typer.Option(
        None,
        "--target-url",
        help="Target Meilisearch instance URL for export mode"
    ),
    target_api_key: Optional[str] = typer.Option(
        None,
        "--target-api-key",
        help="Target Meilisearch instance API key for export mode"
    ),
    payload_size: str = typer.Option(
        "50MiB",
        "--payload-size",
        help="Payload size for export (e.g., '50MiB', '100MB')"
    ),
    index_patterns: Optional[str] = typer.Option(
        None,
        "--index-patterns",
        help="Comma-separated index patterns to export (e.g., 'index1,index2*')"
    ),
    override_settings: bool = typer.Option(
        False,
        "--override-settings",
        help="Override target instance settings with source settings"
    ),
    filter_expr: Optional[str] = typer.Option(
        None,
        "--filter",
        help="Filter expression for selective document export"
    ),
    # Backup and import management options
    no_backup: bool = typer.Option(
        False,
        "--no-backup",
        help="Disable automatic backup creation before/after export operations"
    ),
    update_import: bool = typer.Option(
        False,
        "--update-import",
        help="Copy latest dump to just_chat_rag.dump for import (backs up existing)"
    )
) -> None:
    """Create a MeiliSearch dump or export data to another instance."""
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
    
    client = get_client(host, port, api_key)
    
    if export:
        # Export mode validation
        if not target_url:
            print("Error: --target-url is required for export mode")
            return
        if not target_api_key:
            print("Error: --target-api-key is required for export mode")
            return
        
        print(f"Mode: EXPORT to {target_url}")
        print(f"Target API key: {'*' * (len(target_api_key) - 4)}{target_api_key[-4:] if len(target_api_key) > 4 else '****'}")
        print(f"Payload size: {payload_size}")
        print(f"Auto-backup: {'disabled' if no_backup else 'enabled'}")
        
        # Create backup before export (unless disabled)
        pre_export_dump = None
        if not no_backup:
            pre_export_dump = create_backup_dump(client, actual_dump_path, "PRE-EXPORT")
            if pre_export_dump is None:
                print("⚠️ Warning: Pre-export backup failed, but continuing with export...")
        
        # Prepare indexes configuration if patterns are provided
        indexes_config = None
        if index_patterns:
            indexes_config = {}
            patterns = [p.strip() for p in index_patterns.split(',')]
            for pattern in patterns:
                config = {}
                if filter_expr:
                    config["filter"] = filter_expr
                if override_settings:
                    config["overrideSettings"] = True
                indexes_config[pattern] = config
            
            print(f"Index patterns: {', '.join(patterns)}")
            if filter_expr:
                print(f"Filter: {filter_expr}")
            if override_settings:
                print("Override settings: enabled")
        
        # Record start time for export
        start_time = time.time()
        
        print(f"Initiating export at {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}...")
        task = initiate_export(client, target_url, target_api_key, payload_size, indexes_config)
        
        if task is None:
            print("Failed to initiate export")
            return
        
        # Wait for export to complete
        export_start_time = time.time()
        completed_task = wait_for_export(client, task, timeout_seconds=600)
        export_end_time = time.time()
        
        if completed_task is None:
            print("Failed to complete export")
            return
        
        # Calculate export duration
        export_duration = export_end_time - export_start_time
        
        if completed_task.status == "succeeded":
            print(f"Export completed successfully in {export_duration:.2f} seconds!")
            print(f"Data has been migrated to {target_url}")
            
            # Create backup after export (unless disabled)
            post_export_dump = None
            if not no_backup:
                post_export_dump = create_backup_dump(client, actual_dump_path, "POST-EXPORT")
                if post_export_dump is None:
                    print("⚠️ Warning: Post-export backup failed")
            
            # Update import dump if requested
            latest_dump_for_import = post_export_dump or pre_export_dump
            if update_import and latest_dump_for_import:
                print(f"\n📁 Updating import dump...")
                update_success = update_import_dump(actual_dump_path, latest_dump_for_import)
                if not update_success:
                    print("⚠️ Warning: Failed to update import dump")
            elif update_import:
                print("⚠️ Warning: --update-import requested but no dump available")
            
            # Calculate and display total process time
            process_end_time = time.time()
            total_duration = process_end_time - process_start_time
            print(f"\nTotal process time: {total_duration:.2f} seconds")
            print(f"Export operation time: {export_duration:.2f} seconds")
            print(f"Completed at {datetime.fromtimestamp(process_end_time).strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("\n" + "="*60)
            print("✅ EXPORT COMPLETED!")
            print("   Data has been migrated between instances.")
            print("   The operation was additive - existing data was preserved.")
            print("   Duplicate documents were replaced with new data.")
            if not no_backup:
                print("   🔒 Automatic backups created for data safety.")
            if update_import and latest_dump_for_import:
                print("   📁 Import dump updated and ready for use.")
            print("="*60)
        else:
            print(f"Export failed with status: {completed_task.status}")
            if hasattr(completed_task, 'error'):
                print(f"Error details: {completed_task.error}")
            
            # Show timing even for failed exports
            process_end_time = time.time()
            total_duration = process_end_time - process_start_time
            print(f"\nTotal process time: {total_duration:.2f} seconds")
            print(f"Export operation time: {export_duration:.2f} seconds")
    
    else:
        # Original dump mode
        print("Mode: DUMP")
        print(f"Monitoring dumps in: {actual_dump_path}")
        
        # Enumerate dumps folder before creating dump
        print_dumps_status(actual_dump_path, "BEFORE DUMP")
        
        # Record start time for new dump detection
        start_time = time.time()
        
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
            
            # Update import dump if requested
            if update_import and new_dump:
                print(f"\n📁 Updating import dump...")
                update_success = update_import_dump(actual_dump_path, new_dump)
                if not update_success:
                    print("⚠️ Warning: Failed to update import dump")
            elif update_import:
                print("⚠️ Warning: --update-import requested but no dump was created")
            
            # Calculate and display total process time
            process_end_time = time.time()
            total_duration = process_end_time - process_start_time
            print(f"\nTotal process time: {total_duration:.2f} seconds")
            print(f"Dump operation time: {dump_duration:.2f} seconds")
            print(f"Completed at {datetime.fromtimestamp(process_end_time).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show reset tip after successful dump
            print("\n" + "="*60)
            if update_import and new_dump:
                print("✅ DUMP COMPLETED AND IMPORT READY!")
                print("   📁 Import dump updated: just_chat_rag.dump")
                print("   🔄 Ready for immediate import with:")
            else:
                print("💡 TIP: To force re-import of this dump:")
                if new_dump:
                    print(f"   📁 First copy: cp ./dumps/{new_dump} ./dumps/just_chat_rag.dump")
            print("   # For Docker:")
            print("   docker compose down")
            print("   docker volume rm just-chat_meili-data")
            print("   USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up")
            print("   # For Podman:")
            print("   podman compose down")
            print("   podman volume rm just-chat_meili-data")
            print("   podman compose up")
            print("   # Removes named volume (MeiliSearch data), preserves mongo-data volume")
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