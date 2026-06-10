"""
Data Agent - وكيل هندسة المخطط والزمن
========================================
يستخرج البيانات الخام من Excel ويجهزها للوكلاء اللاحقة
"""

import json
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.helpers import DateHelper, TimeHelper, ValidationHelper, FileHelper

class DataAgent:
    """وكيل استخراج وهندسة البيانات"""
    
    def __init__(self, excel_path: str, config_path: str = "config"):
        self.logger = get_logger("data_agent")
        self.excel_path = excel_path
        self.config_path = Path(config_path)
        
        # تحميل ملفات التكوين
        self.excel_structure = FileHelper.load_json(self.config_path / "EXCEL_STRUCTURE.json")
        self.houses_dict = FileHelper.load_json(self.config_path / "houses_dictionary.json")
        
        # مسارات المخرجات
        self.output_dir = Path("data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.zodiac_signs = ValidationHelper.valid_zodiac_signs

    def _load_excel_data(self) -> pd.DataFrame:
        """قراءة بيانات الخرائط من ملف Excel"""
        self.logger.info(f"جاري قراءة ملف Excel: {self.excel_path}")
        try:
            sheet_name = self.excel_structure.get("sheet_name", "الخرائط")
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
            self.logger.success(f"تم قراءة {len(df)} صف بنجاح من ورقة '{sheet_name}'")
            return df
        except Exception as e:
            self.logger.error(f"فشل في قراءة ملف Excel: {str(e)}")
            return None

    def process_zodiac_sign(self, df: pd.DataFrame, sign_name: str) -> bool:
        """
        معالجة بيانات برج محدد وتقسيمها إلى فترات زمنية
        
        Args:
            df: dataframe البيانات الكاملة
            sign_name: اسم البرج (مثال: الحمل)
        """
        self.logger.section(f"معالجة برج: {sign_name}")
        
        # 1. فلترة البيانات بناءً على عمود الطالع_البرج
        col_mapping = self.excel_structure.get("columns_mapping", {})
        rising_col = col_mapping.get("rising_sign", "الطالع_البرج")
        
        sign_df = df[df[rising_col] == sign_name].copy()
        
        if sign_df.empty:
            self.logger.warning(f"لا توجد بيانات للبرج {sign_name} في العمود {rising_col}")
            return False
            
        self.logger.info(f"تم العثور على {len(sign_df)} صف للبرج {sign_name}")

        # 2. تجهيز هيكل البيانات لـ 549 يوماً
        processed_days = []
        time_periods = self.excel_structure.get("time_periods", {})
        
        for _, row in sign_df.iterrows():
            day_data = {
                "التاريخ": str(row.get(col_mapping.get("date", "التاريخ"))),
                "الطالع_البرج": sign_name,
                "الفترات": {}
            }
            
            # 3. استخراج بيانات كل فترة (صباح، ظهيرة، مساء)
            for period_name, period_time in time_periods.items():
                # في ملفك الحقيقي، كل يوم يحتوي على 3 صفوف (للأوقات الثلاثة)
                # هذا الكود يفترض أن الوقت موجود في العمود، أو يمكنك تعديله حسب هيكل ملفك
                time_col = col_mapping.get("time", "الوقت")
                
                # نبحث عن الصف الذي يطابق هذا الوقت في نفس التاريخ
                time_row = sign_df[(sign_df[col_mapping.get("date", "التاريخ")] == row[col_mapping.get("date", "التاريخ")]) & (sign_df[time_col].astype(str).str.startswith(period_time.split(":")[0]))]
                
                if not time_row.empty:
                    r = time_row.iloc[0]
                    day_data["الفترات"][period_name] = {
                        "الوقت": period_time,
                        "البيوت": {
                            "الشمس": int(r.get(col_mapping.get("sun_house", "الشمس_البيت"), 0)),
                            "القمر": int(r.get(col_mapping.get("moon_house", "القمر_البيت"), 0)),
                            "عطارد": int(r.get(col_mapping.get("mercury_house", "عطارد_البيت"), 0)),
                            "الزهرة": int(r.get(col_mapping.get("venus_house", "الزهرة_البيت"), 0)),
                            "المريخ": int(r.get(col_mapping.get("mars_house", "المريخ_البيت"), 0)),
                            "المشتري": int(r.get(col_mapping.get("jupiter_house", "المشتري_البيت"), 0)),
                            "زحل": int(r.get(col_mapping.get("saturn_house", "زحل_البيت"), 0))
                        }
                    }
            
            processed_days.append(day_data)
            
        # 4. حفظ البيانات المجمعنة في ملف JSON للبرج
        output_file = self.output_dir / f"{sign_name}_data.json"
        FileHelper.save_json({"days": processed_days, "total_days": len(processed_days)}, str(output_file))
        self.logger.success(f"تم حفظ بيانات {sign_name} في {output_file}")
        
        return True

    def run(self) -> bool:
        """تشغيل وكيل البيانات لجميع الأبراج"""
        df = self._load_excel_data()
        if df is None:
            return False
            
        success_count = 0
        for sign in self.zodiac_signs:
            if self.process_zodiac_sign(df, sign):
                success_count += 1
                
        self.logger.section(f"انتهى وكيل البيانات: تمت معالجة {success_count} من {len(self.zodiac_signs)} برج")
        return success_count == len(self.zodiac_signs)

if __name__ == "__main__":
    # للتجربة المباشرة
    agent = DataAgent("data/input/الخريطة_الشاملة_الاحترافية_بالتفسير_العربي.xlsx")
    agent.run()
