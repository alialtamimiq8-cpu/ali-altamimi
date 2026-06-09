"""
Validators Module - التحقق من صحة البيانات
==========================================

هذا الملف يحتوي على فئات التحقق من صحة البيانات المختلفة
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class DataValidator:
    """فئة للتحقق من صحة البيانات"""
    
    @staticmethod
    def validate_zodiac_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات الأبراج
        
        Args:
            data: قاموس البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        required_fields = ['name', 'symbol', 'start_date', 'end_date', 'element', 'ruling_planet']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"الحقل المطلوب '{field}' مفقود")
        
        if 'dates' in data:
            if not isinstance(data['dates'], dict):
                errors.append("'dates' يجب أن يكون قاموساً")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_planet_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات الكواكب
        
        Args:
            data: قاموس البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        required_fields = ['name', 'symbol', 'type', 'characteristics']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"الحقل المطلوب '{field}' مفقود")
        
        if 'characteristics' in data:
            if not isinstance(data['characteristics'], (list, dict)):
                errors.append("'characteristics' يجب أن تكون قائمة أو قاموساً")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_house_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات البيوت
        
        Args:
            data: قاموس البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        if 'house_number' not in data or not (1 <= data.get('house_number', 0) <= 12):
            errors.append("رقم البيت يجب أن يكون بين 1 و 12")
        
        if 'meanings' not in data:
            errors.append("الحقل 'meanings' مفقود")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_aspect_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات الجوانب
        
        Args:
            data: قاموس البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        valid_aspects = ['اقتران', 'تثليث', 'تسديس', 'تربيع', 'مقابلة']
        
        if 'name' not in data or data.get('name') not in valid_aspects:
            errors.append(f"نوع الجانب غير صحيح. الأنواع المسموحة: {valid_aspects}")
        
        if 'angle' not in data or not isinstance(data['angle'], (int, float)):
            errors.append("الزاوية يجب أن تكون رقماً")
        
        if 'interpretation' not in data:
            errors.append("الحقل 'interpretation' مفقود")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_excel_data(data: List[Dict]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات Excel
        
        Args:
            data: قائمة البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        if not data:
            errors.append("لا توجد بيانات للتحقق منها")
            return False, errors
        
        if not isinstance(data, list):
            errors.append("البيانات يجب أن تكون قائمة")
            return False, errors
        
        # التحقق من كل صف
        required_columns = ['date', 'zodiac', 'planets', 'houses', 'aspects']
        
        for idx, row in enumerate(data):
            if not isinstance(row, dict):
                errors.append(f"الصف {idx} ليس قاموساً")
                continue
            
            for col in required_columns:
                if col not in row:
                    errors.append(f"الصف {idx}: العمود '{col}' مفقود")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """
        التحقق من صيغة التاريخ
        
        Args:
            date_str: نص التاريخ
            format: الصيغة المتوقعة
            
        Returns:
            True إذا كانت الصيغة صحيحة
        """
        try:
            datetime.strptime(str(date_str), format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_text_content(text: str, min_length: int = 10, max_length: int = 1000) -> tuple[bool, Optional[str]]:
        """
        التحقق من صحة محتوى النص
        
        Args:
            text: النص المراد التحقق منه
            min_length: الطول الأدنى
            max_length: الطول الأقصى
            
        Returns:
            (صحة النص، رسالة الخطأ إن وجدت)
        """
        if not text or not isinstance(text, str):
            return False, "النص يجب أن يكون نصاً غير فارغ"
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"النص قصير جداً (الحد الأدنى: {min_length} أحرف)"
        
        if len(text) > max_length:
            return False, f"النص طويل جداً (الحد الأقصى: {max_length} أحرف)"
        
        return True, None
    
    @staticmethod
    def validate_intentions_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        التحقق من صحة بيانات النوايا
        
        Args:
            data: قاموس البيانات
            
        Returns:
            (صحة البيانات، قائمة الأخطاء)
        """
        errors = []
        
        required_fields = ['intention', 'keywords', 'affirmations']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"الحقل المطلوب '{field}' مفقود")
        
        if 'keywords' in data and not isinstance(data['keywords'], list):
            errors.append("'keywords' يجب أن تكون قائمة")
        
        if 'affirmations' in data and not isinstance(data['affirmations'], list):
            errors.append("'affirmations' يجب أن تكون قائمة")
        
        return len(errors) == 0, errors
