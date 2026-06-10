"""
Batching Agent - وكيل تقسيم وتقطيع الحزم
============================================
يقسم البيانات الضخمة إلى حزم صغيرة (30 يوماً) لتسهيل المعالجة
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.helpers import FileHelper

class BatchingAgent:
    """وكيل تقسيم البيانات إلى حزم شهرية"""
    
    def __init__(self, batch_size: int = 30):
        self.logger = get_logger("batching_agent")
        self.batch_size = batch_size
        self.processed_dir = Path("data/processed")
        self.batches_dir = Path("data/batches")
        self.batches_dir.mkdir(parents=True, exist_ok=True)

    def create_batches(self, sign_name: str) -> list:
        """
        أخذ ملف البرج الكامل وتقسيمه إلى ملفات صغيرة
        
        Args:
            sign_name: اسم البرج (مثال: الحمل)
            
        Returns:
            قائمة بمسارات ملفات الحزم الناتجة
        """
        self.logger.info(f"جاري تقطيع بيانات برج {sign_name} إلى حزم من {self.batch_size} يوم...")
        
        input_file = self.processed_dir / f"{sign_name}_data.json"
        if not input_file.exists():
            self.logger.error(f"ملف بيانات {sign_name} غير موجود!")
            return []

        # قراءة البيانات الكاملة
        data = FileHelper.load_json(str(input_file))
        days = data.get("days", [])
        
        batch_paths = []
        
        # تقسيم الأيام إلى حزم
        for i in range(0, len(days), self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch_data = days[i : i + self.batch_size]
            
            # إنشاء مجلد خاص بالبرج
            sign_batch_dir = self.batches_dir / sign_name
            sign_batch_dir.mkdir(parents=True, exist_ok=True)
            
            # حفظ الحزمة
            batch_file = sign_batch_dir / f"batch_{batch_num}.json"
            FileHelper.save_json({"batch_number": batch_num, "days": batch_data}, str(batch_file))
            batch_paths.append(str(batch_file))
            
            self.logger.info(f"تم إنشاء الحزمة {batch_num} ({len(batch_data)} يوم)")
            
        self.logger.success(f"انتهى تقطيع {sign_name} إلى {len(batch_paths)} حزمة")
        return batch_paths

if __name__ == "__main__":
    # للتجربة
    agent = BatchingAgent(batch_size=30)
    agent.create_batches("السرطان")
