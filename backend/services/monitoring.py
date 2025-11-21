"""
Intelligent Monitoring Service
Tracks system metrics, usage, and errors for analytics
"""

from datetime import datetime
from typing import Dict, List, Any
from collections import deque
import time


class IntelligentMonitor:
    """
    Monitor system health and track usage analytics
    """
    
    def __init__(self, max_history: int = 100):
        self.start_time = time.time()
        self.max_history = max_history
        
        # Metrics storage
        self.metrics = {
            "requests": 0,
            "successful_builds": 0,
            "failed_builds": 0,
            "cli_calculations": 0,
            "errors": 0
        }
        
        # History queues (FIFO with max size)
        self.recent_builds = deque(maxlen=max_history)
        self.recent_errors = deque(maxlen=max_history)
        
        # Task queues for background processing
        self.code_review_queue = []
        self.error_analysis_queue = []
        self.doc_query_queue = []
    
    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def get_uptime(self) -> float:
        """Get system uptime in seconds"""
        return time.time() - self.start_time
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return {
            **self.metrics,
            "uptime_seconds": self.get_uptime(),
            "uptime_formatted": self._format_uptime(self.get_uptime())
        }
    
    def get_recent_builds(self) -> List[Dict[str, Any]]:
        """Get recent build history"""
        return list(self.recent_builds)
    
    def get_recent_errors(self) -> List[Dict[str, Any]]:
        """Get recent error history"""
        return list(self.recent_errors)
    
    def track_build(self, paper_id: str, success: bool, duration: float):
        """Track paper build"""
        build_record = {
            "paper_id": paper_id,
            "success": success,
            "duration": duration,
            "timestamp": self.get_timestamp()
        }
        
        self.recent_builds.append(build_record)
        
        if success:
            self.metrics["successful_builds"] += 1
        else:
            self.metrics["failed_builds"] += 1
    
    def track_error(self, error: str, context: Dict[str, Any] = None):
        """Track error occurrence"""
        error_record = {
            "error": error,
            "context": context or {},
            "timestamp": self.get_timestamp()
        }
        
        self.recent_errors.append(error_record)
        self.metrics["errors"] += 1
    
    def track_cli_calculation(self, entity: str, cli: float):
        """Track CLI calculation"""
        self.metrics["cli_calculations"] += 1
    
    def queue_code_review(self, file_path: str, content: str):
        """Queue code review task"""
        self.code_review_queue.append({
            "file_path": file_path,
            "content": content,
            "queued_at": self.get_timestamp()
        })
    
    def queue_error_analysis(self, error_log: str):
        """Queue error analysis task"""
        self.error_analysis_queue.append({
            "error_log": error_log,
            "queued_at": self.get_timestamp()
        })
    
    def queue_doc_query(self, question: str):
        """Queue documentation query"""
        self.doc_query_queue.append({
            "question": question,
            "queued_at": self.get_timestamp()
        })
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime as human-readable string"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        
        return " ".join(parts)
