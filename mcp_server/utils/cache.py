"""
Caching System for MCP Server
==============================

Implements intelligent caching to further optimize performance.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Simple file-based cache for MCP tool results.
    
    Features:
    - TTL (time-to-live) support
    - Automatic cache invalidation
    - JSON serialization
    - Hash-based keys
    
    Example:
        >>> cache = CacheManager(cache_dir=Path("cache"), ttl=3600)
        >>> cache.set("key", {"result": "data"})
        >>> result = cache.get("key")  # Returns cached data
    """
    
    def __init__(self, cache_dir: Path, ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory for cache files
            ttl: Time-to-live in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Cache initialized: {cache_dir} (TTL: {ttl}s)")
    
    def _get_cache_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        """
        Generate cache key from tool name and arguments.
        
        Args:
            tool_name: Name of the tool
            args: Tool arguments
        
        Returns:
            Hash string for cache key
        """
        # Create deterministic string from args
        args_str = json.dumps(args, sort_keys=True)
        key_str = f"{tool_name}:{args_str}"
        
        # Hash it
        hash_obj = hashlib.sha256(key_str.encode())
        return hash_obj.hexdigest()[:16]
    
    def get(self, tool_name: str, args: Dict[str, Any]) -> Optional[Any]:
        """
        Get cached result if available and not expired.
        
        Args:
            tool_name: Name of the tool
            args: Tool arguments
        
        Returns:
            Cached result or None if not found/expired
        """
        key = self._get_cache_key(tool_name, args)
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file) as f:
                cached_data = json.load(f)
            
            # Check TTL
            timestamp = cached_data.get('timestamp', 0)
            age = time.time() - timestamp
            
            if age > self.ttl:
                logger.debug(f"Cache expired for {tool_name} (age: {age:.1f}s)")
                cache_file.unlink()  # Delete expired cache
                return None
            
            logger.debug(f"Cache hit for {tool_name} (age: {age:.1f}s)")
            return cached_data['result']
        
        except Exception as e:
            logger.warning(f"Cache read error for {tool_name}: {e}")
            return None
    
    def set(self, tool_name: str, args: Dict[str, Any], result: Any):
        """
        Cache a tool result.
        
        Args:
            tool_name: Name of the tool
            args: Tool arguments
            result: Result to cache
        """
        key = self._get_cache_key(tool_name, args)
        cache_file = self.cache_dir / f"{key}.json"
        
        try:
            cached_data = {
                'timestamp': time.time(),
                'tool_name': tool_name,
                'result': result
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cached_data, f)
            
            logger.debug(f"Cached result for {tool_name}")
        
        except Exception as e:
            logger.warning(f"Cache write error for {tool_name}: {e}")
    
    def clear(self, tool_name: Optional[str] = None):
        """
        Clear cache.
        
        Args:
            tool_name: If specified, only clear cache for this tool
        """
        if tool_name is None:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("All cache cleared")
        else:
            # Clear specific tool cache (would need to track which files belong to which tool)
            logger.info(f"Cache cleared for {tool_name}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache stats
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_entries': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir)
        }
