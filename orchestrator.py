"""
Orchestrator - منسق سير العمل
==============================

هذا الملف يحتوي على منسق سير العمل الذي يربط جميع الوكلاء معاً
ويدير تدفق البيانات من البداية إلى النهاية
"""

import json
from pathlib import Path
from typing import Dict, Any
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.data_agent import DataAgent
from agents.text_agent import TextAgent
from agents.insight_agent import InsightAgent
from utils.logger import get_logger


class Orchestrator:
    """منسق سير العمل الرئيسي"""
    
    def __init__(self, excel_path: str = None, config_path: str = "config"):
        """
        تهيئة Orchestrator
        
        Args:
            excel_path: مسار ملف Excel
            config_path: مسار ملفات التكوين
        """
        self.logger = get_logger("orchestrator")
        self.config_path = config_path
        self.excel_path = excel_path or "data/input/الخريطة_الشاملة_الاحترافية_بالتفسير_العربي.xlsx"
        
        # الوكلاء
        self.data_agent = None
        self.text_agent = None
        self.insight_agent = None
        
        # المسارات
        self.processed_data_dir = Path("data/processed")
        self.output_dir = Path("data/output")
        self.reports_dir = Path("reports")
        
        self._create_directories()
    
    def _create_directories(self):
        """إنشاء جميع المجلدات المطلوبة"""
        for dir_path in [self.processed_data_dir, self.output_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def stage_1_extract_data(self) -> bool:
        """
        المرحلة الأولى: استخراج البيانات من Excel
        
        Returns:
            True إذا نجحت المرحلة
        """
        self.logger.section("📊 المرحلة الأولى: استخراج البيانات")
        
        try:
            self.data_agent = DataAgent(self.excel_path, self.config_path)
            success = self.data_agent.run()
            
            if success:
                self.logger.success("✓ انتهت المرحلة الأولى بنجاح")
                return True
            else:
                self.logger.error("✗ فشلت المرحلة الأولى")
                return False
        except Exception as e:
            self.logger.error(f"✗ خطأ في المرحلة الأولى: {str(e)}")
            return False
    
    def stage_2_generate_messages(self) -> bool:
        """
        المرحلة الثانية: توليد الرسائل
        
        Returns:
            True إذا نجحت المرحلة
        """
        self.logger.section("✍️  المرحلة الثانية: توليد الرسائل")
        
        try:
            self.text_agent = TextAgent(self.config_path)
            
            # توليد رسائل للفترات الثلاث
            time_periods = ["صباح", "ظهيرة", "مساء"]
            messages_count = 0
            
            for period in time_periods:
                self.logger.info(f"🔄 توليد رسائل فترة {period}...")
                try:
                    self.text_agent.run(time_period=period)
                    messages_count += 1
                except Exception as e:
                    self.logger.warning(f"⚠️  خطأ في معالجة فترة {period}: {str(e)}")
            
            if messages_count > 0:
                self.logger.success("✓ انتهت المرحلة الثانية بنجاح")
                return True
            else:
                self.logger.error("✗ فشلت المرحلة الثانية")
                return False
        except Exception as e:
            self.logger.error(f"✗ خطأ في المرحلة الثانية: {str(e)}")
            return False
    
    def stage_3_generate_insights(self) -> bool:
        """
        المرحلة الثالثة: توليد الرؤى والتفسيرات
        
        Returns:
            True إذا نجحت المرحلة
        """
        self.logger.section("🔍 المرحلة الثالثة: توليد الرؤى")
        
        try:
            self.insight_agent = InsightAgent(self.config_path)
            self.insight_agent.run()
            
            self.logger.success("✓ انتهت المرحلة الثالثة بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"✗ خطأ في المرحلة الثالثة: {str(e)}")
            return False
    
    def generate_final_report(self) -> bool:
        """
        إنشاء تقرير نهائي شامل
        
        Returns:
            True إذا نجح إنشاء التقرير
        """
        self.logger.section("📋 إنشاء التقرير النهائي")
        
        try:
            report = {
                "execution_date": datetime.now().isoformat(),
                "stages": {
                    "stage_1_data_extraction": {
                        "name": "استخراج البيانات",
                        "status": "completed",
                        "input": self.excel_path,
                        "output": str(self.processed_data_dir)
                    },
                    "stage_2_message_generation": {
                        "name": "توليد الرسائل",
                        "status": "completed",
                        "input": str(self.processed_data_dir),
                        "output": str(self.processed_data_dir)
                    },
                    "stage_3_insights_generation": {
                        "name": "توليد الرؤى",
                        "status": "completed",
                        "input": str(self.processed_data_dir),
                        "output": str(self.output_dir)
                    }
                },
                "summary": {
                    "total_stages": 3,
                    "completed_stages": 3,
                    "status": "success"
                },
                "output_locations": {
                    "processed_data": str(self.processed_data_dir),
                    "final_messages": str(self.output_dir),
                    "reports": str(self.reports_dir)
                }
            }
            
            # حفظ التقرير
            report_file = self.reports_dir / f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            self.logger.success(f"✓ تم حفظ التقرير في {report_file}")
            return True
        except Exception as e:
            self.logger.error(f"✗ خطأ في إنشاء التقرير: {str(e)}")
            return False
    
    def run_full_pipeline(self) -> bool:
        """
        تشغيل خط أنابيب المعالجة الكامل
        
        Returns:
            True إذا نجح كل شيء
        """
        self.logger.section("🚀 بدء خط الأنابيب الكامل")
        
        stages = [
            ("المرحلة الأولى: استخراج البيانات", self.stage_1_extract_data),
            ("المرحلة الثانية: توليد الرسائل", self.stage_2_generate_messages),
            ("المرحلة الثالثة: توليد الرؤى", self.stage_3_generate_insights),
            ("إنشاء التقرير النهائي", self.generate_final_report)
        ]
        
        all_success = True
        
        for stage_name, stage_func in stages:
            self.logger.section(f"▶️  {stage_name}")
            
            try:
                if not stage_func():
                    all_success = False
                    self.logger.error(f"✗ فشلت {stage_name}")
                    break
            except Exception as e:
                all_success = False
                self.logger.error(f"✗ خطأ في {stage_name}: {str(e)}")
                break
        
        if all_success:
            self.logger.section("✅ انتهى خط الأنابيب بنجاح")
            self._print_summary()
        else:
            self.logger.section("❌ فشل خط الأنابيب")
        
        return all_success
    
    def _print_summary(self):
        """طباعة ملخص الإنجازات"""
        print("\n" + "="*60)
        print("📊 ملخص الإنجازات")
        print("="*60)
        print(f"✓ تم استخراج البيانات من Excel بنجاح")
        print(f"✓ تم توليد الرسائل اليومية للفترات الثلاث")
        print(f"✓ تم توليد الرؤى والتفسيرات")
        print(f"✓ تم حفظ جميع البيانات والرسائل")
        print(f"\n📁 مسارات المخرجات:")
        print(f"   - البيانات المعالجة: {self.processed_data_dir}")
        print(f"   - الرسائل النهائية: {self.output_dir}")
        print(f"   - التقارير: {self.reports_dir}")
        print("="*60 + "\n")


def main():
    """الدالة الرئيسية"""
    orchestrator = Orchestrator()
    orchestrator.run_full_pipeline()


if __name__ == "__main__":
    main()
