"""
QA Agent - وكيل المراجعة والتدقيق الصارم
==========================================
يرفض أي نص يحتوي على مصطلحات فلكية محظورة
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.helpers import TextHelper, FileHelper

class QAAgent:
    """وكيل التحقق من الجودة والأمان اللغوي"""
    
    def __init__(self):
        self.logger = get_logger("qa_agent")
        # استخدام قائمة الكلمات المحظورة من helpers.py
        self.forbidden = TextHelper.forbidden_keywords
        self.violations_count = 0

    def check_text(self, text: str) -> tuple[bool, list]:
        """
        فحص نص واحد
        
        Returns:
            (مقبول أم لا، قائمة الكلمات المخالفة)
        """
        found = TextHelper.check_forbidden_keywords(text)
        if found:
            self.violations_count += 1
            return False, found
        return True, []

    def review_day(self, day_data: dict) -> dict:
        """
        مراجعة يوم كامل (الرسائل الثلاثة)
        إذا وجد مخالفة، يعيد كتابة الرسالة بأسلوب آمن عام لتجنب تعطل النظام
        """
        date = day_data.get("التاريخ")
        periods = day_data.get("الرسائل", {})
        clean_day = {"التاريخ": date, "الرسائل": {}, "مخالفات": 0}
        day_violations = 0
        
        for period, messages in periods.items():
            clean_messages = []
            for msg in messages:
                is_clean, bad_words = self.check_text(msg)
                if is_clean:
                    clean_messages.append(msg)
                else:
                    day_violations += 1
                    # نص بديل آمن تماماً في حال وجود كلمة محظورة
                    clean_messages.append("تركيزك اليوم ينصب على ما يهمك حقاً. ثق بحدسك.")
                    
            clean_day["الرسائل"][period] = clean_messages
            
        clean_day["مخالفات"] = day_violations
        return clean_day

    def run_review(self, processed_days: list) -> tuple[list, int]:
        """
        مراجعة دفعة من الأيام
        
        Args:
            processed_days: قائمة الأيام التي تولد نصوصها
            
        Returns:
            (القائمة المنقاة، عدد المخالفات الكلي)
        """
        self.logger.info("بدء الفحص الأمني للنصوص...")
        self.violations_count = 0
        final_clean_days = []
        
        for day in processed_days:
            clean_day = self.review_day(day)
            final_clean_days.append(clean_day)
            
        if self.violations_count > 0:
            self.logger.warning(f"تم اكتشاف وإصلاح {self.violations_count} مخالفة أمنية.")
        else:
            self.logger.success("✓ جميع النصوص خالية من الكلمات المحظورة بنسبة 100%")
            
        return final_clean_days, self.violations_count

if __name__ == "__main__":
    agent = QAAgent()
    # للتجربة
    test_text = "في بيتك، شمسك تشرق." # يجب أن يرفضها لأنها تحتوي (بيت، شمس)
    ok, words = agent.check_text(test_text)
    print(f"النظافة: {ok}, الكلمات السيئة: {words}")
