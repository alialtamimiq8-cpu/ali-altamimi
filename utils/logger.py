"""
Logger Module - نظام تسجيل الأخطاء والمعلومات
==============================================

نظام شامل لتسجيل جميع الأحداث والأخطاء في المشروع
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Formatter مع ألوان للـ terminal"""
    
    # ألوان ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class CustomLogger:
    """فئة Logger مخصصة للمشروع"""
    
    def __init__(self, name: str):
        """
        تهيئة Logger
        
        Args:
            name: اسم Logger
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # إزالة Handlers السابقة إن وجدت
        self.logger.handlers = []
        
        # Console Handler مع ألوان
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_format = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File Handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.warning(f"⚠️  لم يتمكن من إنشاء file handler: {str(e)}")
    
    def debug(self, message: str):
        """تسجيل رسالة debug"""
        self.logger.debug(f"🔍 {message}")
    
    def info(self, message: str):
        """تسجيل رسالة معلومة"""
        self.logger.info(f"ℹ️  {message}")
    
    def warning(self, message: str):
        """تسجيل تحذير"""
        self.logger.warning(f"⚠️  {message}")
    
    def error(self, message: str):
        """تسجيل خطأ"""
        self.logger.error(f"❌ {message}")
    
    def critical(self, message: str):
        """تسجيل خطأ حرج"""
        self.logger.critical(f"🚨 {message}")
    
    def success(self, message: str):
        """تسجيل نجاح"""
        self.logger.info(f"✅ {message}")
    
    def section(self, title: str):
        """طباعة عنوان قسم"""
        separator = "=" * 60
        self.logger.info(f"\n{separator}")
        self.logger.info(f"  {title}")
        self.logger.info(f"{separator}\n")
    
    def subsection(self, title: str):
        """طباعة عنوان فرعي"""
        self.logger.info(f"\n--- {title} ---\n")


# Cache للـ loggers
_loggers = {}


def get_logger(name: str) -> CustomLogger:
    """
    الحصول على Logger أو إنشاء واحد جديد
    
    Args:
        name: اسم Logger
        
    Returns:
        CustomLogger instance
    """
    if name not in _loggers:
        _loggers[name] = CustomLogger(name)
    return _loggers[name]
