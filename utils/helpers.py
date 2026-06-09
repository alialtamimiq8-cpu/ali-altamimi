"""
Helper Functions - دوال مساعدة عامة
====================================

هذا الملف يحتوي على دوال مساعدة تُستخدم في جميع الوكلاء
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from pathlib import Path


class DateHelper:
    """فئة مساعدة للتعامل مع التواريخ"""
    
    @staticmethod
    def is_valid_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """التحقق من صحة تاريخ"""
        try:
            datetime.strptime(str(date_str), format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def parse_date(date_str: str, format: str = "%Y-%m-%d") -> datetime:
        """تحويل نص التاريخ إلى datetime"""
        return datetime.strptime(str(date_str), format)
    
    @staticmethod
    def get_day_of_week_ar(date: datetime) -> str:
        """الحصول على يوم الأسبوع باللغة العربية"""
        days_ar = {
            0: "الاثنين",
            1: "الثلاثاء",
            2: "الأربعاء",
            3: "الخميس",
            4: "الجمعة",
            5: "السبت",
            6: "الأحد"
        }
        return days_ar[date.weekday()]
    
    @staticmethod
    def get_days_between(start_date: datetime, end_date: datetime) -> int:
        """حساب عدد الأيام بين تاريخين"""
        return (end_date - start_date).days + 1


class TimeHelper:
    """فئة مساعدة للتعامل مع الأوقات"""
    
    @staticmethod
    def is_valid_time(time_str: str, format: str = "%H:%M:%S") -> bool:
        """التحقق من صحة وقت"""
        try:
            datetime.strptime(str(time_str), format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def parse_time(time_str: str, format: str = "%H:%M:%S") -> datetime:
        """تحويل نص الوقت إلى datetime"""
        return datetime.strptime(str(time_str), format)
    
    @staticmethod
    def get_time_period(time: str) -> str:
        """تحديد فترة اليوم (صباح/ظهيرة/مساء)"""
        time_obj = datetime.strptime(str(time), "%H:%M:%S")
        hour = time_obj.hour
        
        if 6 <= hour < 12:
            return "صباح"
        elif 12 <= hour < 17:
            return "ظهيرة"
        else:
            return "مساء"


class TextHelper:
    """فئة مساعدة للتعامل مع النصوص"""
    
    forbidden_keywords = [
        "برج", "كوكب", "طالع", "بيت", "شمس", "قمر",
        "عطارد", "زهرة", "مريخ", "مشتري", "زحل",
        "اقتران", "تربيع", "تثليث", "تسديس", "مقابلة",
        "جوانب", "فلك", "خريطة", "درجة"
    ]
    
    @staticmethod
    def check_forbidden_keywords(text: str) -> List[str]:
        """
        التحقق من وجود كلمات محظورة في النص
        
        Args:
            text: النص المراد فحصه
            
        Returns:
            قائمة الكلمات المحظورة الموجودة في النص
        """
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in TextHelper.forbidden_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    @staticmethod
    def remove_diacritics(text: str) -> str:
        """إزالة الحروف الإضافية العربية (التشكيل)"""
        import re
        arabic_diacritics = re.compile(r'[\u064B-\u0652]')
        return re.sub(arabic_diacritics, '', text)
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """تطبيع النص (إزالة مسافات إضافية، إلخ)"""
        text = text.strip()
        text = ' '.join(text.split())  # إزالة مسافات متعددة
        return text
    
    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """قص النص إذا تجاوز طول معين"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."


class ValidationHelper:
    """فئة مساعدة للتحقق من صحة البيانات"""
    
    valid_zodiac_signs = [
        "الحمل", "الثور", "الجوزاء", "السرطان",
        "الأسد", "العذراء", "الميزان", "العقرب",
        "القوس", "الجدي", "الدلو", "الحوت"
    ]
    
    valid_planets = [
        "الشمس", "القمر", "عطارد", "الزهرة",
        "المريخ", "المشتري", "زحل"
    ]
    
    valid_aspects = [
        "اقتران", "تثليث", "تسديس", "تربيع", "مقابلة"
    ]
    
    @staticmethod
    def is_valid_zodiac(zodiac: str) -> bool:
        """التحقق من صحة برج"""
        return zodiac in ValidationHelper.valid_zodiac_signs
    
    @staticmethod
    def is_valid_planet(planet: str) -> bool:
        """التحقق من صحة اسم كوكب"""
        return planet in ValidationHelper.valid_planets
    
    @staticmethod
    def is_valid_house(house: int) -> bool:
        """التحقق من صحة رقم البيت"""
        return 1 <= house <= 12
    
    @staticmethod
    def is_valid_aspect(aspect: str) -> bool:
        """التحقق من صحة نوع الجانب"""
        return aspect in ValidationHelper.valid_aspects


class FileHelper:
    """فئة مساعدة للتعامل مع الملفات"""
    
    @staticmethod
    def create_directory(path: str) -> bool:
        """إنشاء مجلد إذا لم يكن موجوداً"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"✗ خطأ في إنشاء المجلد {path}: {str(e)}")
            return False
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> bool:
        """حفظ بيانات كملف JSON"""
        try:
            FileHelper.create_directory(str(Path(filepath).parent))
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"✗ خطأ في حفظ الملف {filepath}: {str(e)}")
            return False
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """تحميل بيانات من ملف JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"✗ الملف غير موجود: {filepath}")
            return {}
        except json.JSONDecodeError:
            print(f"✗ الملف ليس JSON صحيح: {filepath}")
            return {}
    
    @staticmethod
    def file_exists(filepath: str) -> bool:
        """التحقق من وجود الملف"""
        return Path(filepath).exists()


class DataHelper:
    """فئة مساعدة للتعامل مع البيانات"""
    
    @staticmethod
    def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
        """دمج قاموسين"""
        merged = dict1.copy()
        merged.update(dict2)
        return merged
    
    @staticmethod
    def filter_dict(data: Dict, keys: List[str]) -> Dict:
        """تصفية قاموس بناءً على مفاتيح محددة"""
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def get_nested_value(data: Dict, path: str, default=None):
        """الحصول على قيمة متداخلة في قاموس"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current


class StatisticsHelper:
    """فئة مساعدة للإحصائيات"""
    
    @staticmethod
    def count_occurrences(items: List[str]) -> Dict[str, int]:
        """حساب عدد مرات حدوث كل عنصر"""
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts
    
    @staticmethod
    def get_percentage(part: int, total: int) -> float:
        """حساب النسبة المئوية"""
        if total == 0:
            return 0
        return round((part / total) * 100, 2)
    
    @staticmethod
    def get_summary_stats(data: List[int]) -> Dict[str, Any]:
        """الحصول على إحصائيات مختصرة"""
        if not data:
            return {}
        
        return {
            "count": len(data),
            "sum": sum(data),
            "average": round(sum(data) / len(data), 2),
            "min": min(data),
            "max": max(data)
        }


# أمثلة على الاستخدام
if __name__ == "__main__":
    print("=== اختبار Helpers ===\n")
    
    # اختبار DateHelper
    print("📅 DateHelper:")
    date1 = DateHelper.parse_date("2026-07-01")
    date2 = DateHelper.parse_date("2026-07-31")
    print(f"  - يوم الأسبوع: {DateHelper.get_day_of_week_ar(date1)}")
    print(f"  - عدد الأيام: {DateHelper.get_days_between(date1, date2)}")
    
    # اختبار TimeHelper
    print("\n⏰ TimeHelper:")
    print(f"  - فترة الصباح: {TimeHelper.get_time_period('06:30:00')}")
    print(f"  - فترة الظهيرة: {TimeHelper.get_time_period('12:00:00')}")
    print(f"  - فترة المساء: {TimeHelper.get_time_period('17:30:00')}")
    
    # اختبار TextHelper
    print("\n📝 TextHelper:")
    test_text = "هذا برج الحمل مع كوكب الشمس"
    forbidden = TextHelper.check_forbidden_keywords(test_text)
    print(f"  - الكلمات المحظورة الموجودة: {forbidden}")
    
    # اختبار ValidationHelper
    print("\n✓ ValidationHelper:")
    print(f"  - الحمل برج صحيح: {ValidationHelper.is_valid_zodiac('الحمل')}")
    print(f"  - الشمس كوكب صحيح: {ValidationHelper.is_valid_planet('الشمس')}")
    print(f"  - البيت 5 صحيح: {ValidationHelper.is_valid_house(5)}")
