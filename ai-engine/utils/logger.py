"""
Comprehensive logging utilities for AlgoMaster-Studio-AI AI Engine
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Dict, Any
import json

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Format the message
        formatted = super().format(record)
        
        # Reset levelname for other formatters
        record.levelname = levelname
        
        return formatted

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        if hasattr(record, 'algorithm_name'):
            log_entry["algorithm_name"] = record.algorithm_name
        if hasattr(record, 'execution_time'):
            log_entry["execution_time"] = record.execution_time
        
        return json.dumps(log_entry)

def setup_logger(
    name: str,
    level: str = "INFO",
    console_output: bool = True,
    file_output: bool = True,
    json_format: bool = False
) -> logging.Logger:
    """
    Set up a comprehensive logger with console and file handlers
    
    Args:
        name: Logger name (usually module name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Enable console output
        file_output: Enable file output
        json_format: Use JSON format for structured logging
    
    Returns:
        Configured logger instance
    """
    
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set logging level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Console handler with colors
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        if json_format:
            console_formatter = JSONFormatter()
        else:
            console_formatter = ColoredFormatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handlers
    if file_output:
        # General log file (rotating by size)
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, f"{name}.log"),
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        
        if json_format:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Error log file (errors and critical only)
        error_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, f"{name}_errors.log"),
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logger.addHandler(error_handler)
        
        # Daily rotating log file
        daily_handler = TimedRotatingFileHandler(
            os.path.join(LOGS_DIR, f"{name}_daily.log"),
            when='midnight',
            interval=1,
            backupCount=30  # Keep 30 days
        )
        daily_handler.setLevel(log_level)
        daily_handler.setFormatter(file_formatter)
        logger.addHandler(daily_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

class PerformanceLogger:
    """Logger for performance metrics and analytics"""
    
    def __init__(self, name: str = "performance"):
        self.logger = setup_logger(f"{name}_performance", json_format=True)
    
    def log_algorithm_analysis(
        self,
        user_id: str,
        algorithm_name: str,
        language: str,
        execution_time: float,
        complexity_score: float,
        quality_score: float,
        **kwargs
    ):
        """Log algorithm analysis performance"""
        self.logger.info(
            "Algorithm analysis completed",
            extra={
                "user_id": user_id,
                "algorithm_name": algorithm_name,
                "language": language,
                "execution_time": execution_time,
                "complexity_score": complexity_score,
                "quality_score": quality_score,
                "event_type": "algorithm_analysis",
                **kwargs
            }
        )
    
    def log_benchmark_results(
        self,
        user_id: str,
        algorithm_name: str,
        test_cases: int,
        avg_execution_time: float,
        memory_usage: float,
        performance_score: float,
        **kwargs
    ):
        """Log benchmark performance results"""
        self.logger.info(
            "Benchmark completed",
            extra={
                "user_id": user_id,
                "algorithm_name": algorithm_name,
                "test_cases": test_cases,
                "avg_execution_time": avg_execution_time,
                "memory_usage": memory_usage,
                "performance_score": performance_score,
                "event_type": "benchmark",
                **kwargs
            }
        )
    
    def log_ai_request(
        self,
        user_id: str,
        request_type: str,
        model_used: str,
        tokens_used: int,
        response_time: float,
        **kwargs
    ):
        """Log AI service requests"""
        self.logger.info(
            "AI request processed",
            extra={
                "user_id": user_id,
                "request_type": request_type,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "response_time": response_time,
                "event_type": "ai_request",
                **kwargs
            }
        )

class SecurityLogger:
    """Logger for security events and monitoring"""
    
    def __init__(self, name: str = "security"):
        self.logger = setup_logger(f"{name}_security")
    
    def log_authentication_attempt(
        self,
        user_id: Optional[str],
        success: bool,
        ip_address: str,
        user_agent: str,
        **kwargs
    ):
        """Log authentication attempts"""
        level = logging.INFO if success else logging.WARNING
        message = "Authentication successful" if success else "Authentication failed"
        
        self.logger.log(
            level,
            message,
            extra={
                "user_id": user_id,
                "success": success,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "event_type": "authentication",
                **kwargs
            }
        )
    
    def log_suspicious_activity(
        self,
        user_id: Optional[str],
        activity_type: str,
        description: str,
        ip_address: str,
        severity: str = "MEDIUM",
        **kwargs
    ):
        """Log suspicious security activities"""
        self.logger.warning(
            f"Suspicious activity detected: {description}",
            extra={
                "user_id": user_id,
                "activity_type": activity_type,
                "description": description,
                "ip_address": ip_address,
                "severity": severity,
                "event_type": "security_alert",
                **kwargs
            }
        )
    
    def log_rate_limit_exceeded(
        self,
        user_id: Optional[str],
        endpoint: str,
        ip_address: str,
        requests_count: int,
        **kwargs
    ):
        """Log rate limit violations"""
        self.logger.warning(
            f"Rate limit exceeded for {endpoint}",
            extra={
                "user_id": user_id,
                "endpoint": endpoint,
                "ip_address": ip_address,
                "requests_count": requests_count,
                "event_type": "rate_limit",
                **kwargs
            }
        )

class APILogger:
    """Logger for API requests and responses"""
    
    def __init__(self, name: str = "api"):
        self.logger = setup_logger(f"{name}_api")
    
    def log_request(
        self,
        method: str,
        path: str,
        user_id: Optional[str],
        ip_address: str,
        user_agent: str,
        request_size: int,
        **kwargs
    ):
        """Log API requests"""
        self.logger.info(
            f"{method} {path}",
            extra={
                "method": method,
                "path": path,
                "user_id": user_id,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "request_size": request_size,
                "event_type": "api_request",
                **kwargs
            }
        )
    
    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        response_time: float,
        response_size: int,
        user_id: Optional[str] = None,
        **kwargs
    ):
        """Log API responses"""
        level = logging.INFO if status_code < 400 else logging.WARNING if status_code < 500 else logging.ERROR
        
        self.logger.log(
            level,
            f"{method} {path} - {status_code} ({response_time:.3f}s)",
            extra={
                "method": method,
                "path": path,
                "status_code": status_code,
                "response_time": response_time,
                "response_size": response_size,
                "user_id": user_id,
                "event_type": "api_response",
                **kwargs
            }
        )

# Global loggers for easy access
performance_logger = PerformanceLogger()
security_logger = SecurityLogger()
api_logger = APILogger()

def log_startup_info():
    """Log startup information"""
    main_logger = setup_logger("main")
    main_logger.info("🚀 AlgoMaster-Studio-AI AI Engine starting up...")
    main_logger.info(f"📁 Logs directory: {LOGS_DIR}")
    main_logger.info("📊 Performance monitoring enabled")
    main_logger.info("🔒 Security monitoring enabled")
    main_logger.info("🌐 API request logging enabled")

def log_shutdown_info():
    """Log shutdown information"""
    main_logger = setup_logger("main")
    main_logger.info("🔄 AlgoMaster-Studio-AI AI Engine shutting down...")
    main_logger.info("💾 Flushing all log handlers...")

# Error tracking utilities
def log_exception(logger: logging.Logger, exception: Exception, context: Dict[str, Any] = None):
    """Log exception with context"""
    context = context or {}
    logger.error(
        f"Exception occurred: {str(exception)}",
        exc_info=True,
        extra=context
    )

def log_performance_warning(logger: logging.Logger, operation: str, duration: float, threshold: float = 5.0):
    """Log performance warnings for slow operations"""
    if duration > threshold:
        logger.warning(
            f"Slow operation detected: {operation} took {duration:.2f}s (threshold: {threshold}s)",
            extra={
                "operation": operation,
                "duration": duration,
                "threshold": threshold,
                "event_type": "performance_warning"
            }
        )

# Initialize logging system
log_startup_info()