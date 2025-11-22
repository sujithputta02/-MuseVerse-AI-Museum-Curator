"""Cache manager for improving performance of repeated operations."""
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Optional
from functools import wraps
import time

class CacheManager:
    """Manages caching of expensive operations."""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache = {}
        self.cache_ttl = 3600  # 1 hour default TTL
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a hash-based cache key."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Check memory cache first
        if key in self.memory_cache:
            cached_data, timestamp = self.memory_cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                del self.memory_cache[key]
        
        # Check disk cache
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data, timestamp = pickle.load(f)
                
                if time.time() - timestamp < self.cache_ttl:
                    # Restore to memory cache
                    self.memory_cache[key] = (cached_data, timestamp)
                    return cached_data
                else:
                    cache_file.unlink()  # Remove expired cache
            except Exception:
                pass
        
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache."""
        timestamp = time.time()
        
        # Store in memory cache
        self.memory_cache[key] = (value, timestamp)
        
        # Store in disk cache
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump((value, timestamp), f)
        except Exception:
            pass  # Fail silently for cache writes
    
    def clear(self):
        """Clear all caches."""
        self.memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
            except Exception:
                pass
    
    def cached(self, ttl: Optional[int] = None):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = f"{func.__name__}:{json.dumps([args, kwargs], sort_keys=True)}"
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                
                # Use custom TTL if provided
                old_ttl = self.cache_ttl
                if ttl is not None:
                    self.cache_ttl = ttl
                
                self.set(cache_key, result)
                
                # Restore original TTL
                self.cache_ttl = old_ttl
                
                return result
            
            return wrapper
        return decorator

# Global cache instance
_cache_instance = None

def get_cache() -> CacheManager:
    """Get or create global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheManager()
    return _cache_instance
