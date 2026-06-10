"""
مثبت الوكلاء التلقائي
=====================
هذا الملف يقوم بإنشاء جميع ملفات الوكلاء الجديدة تلقائياً
لتجنب مشاكل تعارض الأسماء على الهاتف
"""

import json
from pathlib import Path

# تحديد المسارات
agents_dir = Path("agents")
agents_dir.mkdir(parents=True, exist_ok=True)

# --- أكواد الوكلاء السبعة ---
# تم وضعها هنا كنصوص لتتم كتابتها تلقائياً كملفات جديدة

AGENT_1_DATA = '''
import json, pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import ValidationHelper, FileHelper

class DataAgent:
    def __init__(self, excel_path: str, config_path: str = "config"):
        self.logger = get_logger("data_agent")
        self.config_path = Path(config_path)
        self.excel_structure = FileHelper.load_json(self.config_path / "EXCEL_STRUCTURE.json")

    def extract_raw_data(self, sign_name: str) -> list:
        self.logger.section(f"الوكيل 1: استخراج بيانات برج {sign_name}")
        col_map = self.excel_structure.get("columns_mapping", {})
        time_periods = self.excel_structure.get("time_periods", {})
        df = pd.read_excel("data/input/الخريطة_الشاملة_الاحترافية_بالتفسير_العربي.xlsx", sheet_name=self.excel_structure.get("sheet_name", "الخرائط"))
        sign_df = df[df[col_map.get("rising_sign", "الطالع_البرج")] == sign_name].copy()
        if sign_df.empty: return []
        days_data = []
        for date, group in sign_df.groupby(col_map.get("date", "التاريخ")):
            day_entry = {"التاريخ": str(date), "الفترات": {}}
            for period_name, period_time in time_periods.items():
                time_row = group[group[col_map.get("time", "الوقت")].astype(str).str.startswith(period_time.split(":")[0])]
                if not time_row.empty:
                    r = time_row.iloc[0]
                    day_entry["الفترات"][period_name] = {"البيوت": {p: int(r.get(col_map.get(f"{p.lower()}_house", f"{p}_البيت"), 0)) for p in ["الشمس", "القمر", "عطارد", "الزهرة", "المريخ", "المشتري", "زحل"]}}
            days_data.append(day_entry)
        self.logger.success(f"تم استخراج {len(days_data)} يوماً خاماً")
        return days_data
'''

AGENT_5_BATCHING = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import FileHelper

class BatchingAgent:
    def __init__(self, batch_size=30):
        self.logger = get_logger("batching_agent")
        self.batch_size = batch_size
        self.batches_dir = Path("data/batches")
        self.batches_dir.mkdir(parents=True, exist_ok=True)

    def slice_into_batches(self, sign_name: str, raw_days: list) -> list:
        self.logger.section(f"الوكيل 5: تقطيع بيانات برج {sign_name}")
        batch_paths = []
        sign_dir = self.batches_dir / sign_name
        sign_dir.mkdir(parents=True, exist_ok=True)
        for i in range(0, len(raw_days), self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch_file = sign_dir / f"batch_{batch_num}.json"
            FileHelper.save_json({"days": raw_days[i:i+self.batch_size]}, str(batch_file))
            batch_paths.append(str(batch_file))
        self.logger.success(f"تم إنشاء {len(batch_paths)} حزمة")
        return batch_paths
'''

AGENT_2_INSIGHT = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import FileHelper

class InsightAgent:
    def __init__(self, config_path="config"):
        self.logger = get_logger("insight_agent")
        self.houses = FileHelper.load_json(Path(config_path) / "houses_dictionary.json")

    def process_batch(self, batch_path: str) -> list:
        self.logger.info(f"الوكيل 2: صياغة المفاتيح")
        data = FileHelper.load_json(batch_path)
        processed = []
        for day in data.get("days", []):
            noon = day["الفترات"].get("ظهيرة", {}).get("البيوت", {})
            h1 = self.houses.get(str(noon.get("الشمس",0)), {}).get("aliases", [""])[0]
            h2 = self.houses.get(str(noon.get("القمر",0)), {}).get("aliases", [""])[0]
            processed.append({"التاريخ": day["التاريخ"], "مفتاح_اليوم": f"اليوم، حضورك قوي في {h1}، لكن قلبك مشغول بأمر في {h2}. لا تتجاهل شعورك.", "الفترات": day["الفترات"]})
        return processed
'''

AGENT_3_TEXT = '''
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import FileHelper

class TextAgent:
    def __init__(self, config_path="config"):
        self.logger = get_logger("text_agent")
        self.planets = FileHelper.load_json(Path(config_path) / "Planets_dictionry.json")
        self.houses = FileHelper.load_json(Path(config_path) / "houses_dictionary.json")

    def process_batch(self, insights_batch: list) -> list:
        self.logger.info(f"الوكيل 3: تطبيق القوالب")
        final, p_order = [], ["الشمس","القمر","عطارد","الزهرة","المريخ","المشتري","زحل"]
        for day in insights_batch:
            t_day = {"التاريخ": day["التاريخ"], "مفتاح_اليوم": day["مفتاح_اليوم"], "رسائل": {}}
            for period, p_data in day["الفترات"].items():
                msgs, houses = [], p_data.get("البيوت", {})
                for p in p_order:
                    h, v = houses.get(p,0), random.choice(self.planets.get(p,{}).get("verbs",["يتحرك"]))
                    a = random.choice(self.houses.get(str(h),{}).get("aliases",["مجالك"]))
                    if p=="زحل": m=f"في {a}، يعلمك الصبر. ما يتأخر اليوم، ينضج غدًا."
                    elif p=="المشتري": m=f"في {a}، باب يُفتح. خذ نفسًا واسعًا."
                    elif p=="المريخ": m=f"في {a}، أنت اليوم أسرع. تحرك، ولكن بحذر."
                    elif p=="الزهرة": m=f"في {a}، ليّن جانبك. الكلمة الطيبة اليوم تصنع ما لا تصنعه القوة."
                    elif p=="القمر" and h in [1,4,7,10]: m=f"قلبك اليوم في {a}. منه يبدأ يومك وإليه يعود."
                    else: m=f"في {a}، {v}."
                    msgs.append(m)
                t_day["رسائل"][period] = msgs
            final.append(t_day)
        return final
'''

AGENT_4_QA = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import TextHelper

class QAAgent:
    def __init__(self):
        self.logger = get_logger("qa_agent")

    def review_batch(self, text_batch: list) -> tuple:
        self.logger.info(f"الوكيل 4: الفحص الأمني")
        clean, v = [], 0
        for day in text_batch:
            c_day = {"التاريخ": day["التاريخ"], "مفتاح_اليوم": day["مفتاح_اليوم"] if not TextHelper.check_forbidden_keywords(day["مفتاح_اليوم"]) else "تركيزك اليوم ينصب على ما يهمك.", "رسائل": {}}
            for per, ms in day.get("رسائل",{}).items():
                c_ms = [m if not TextHelper.check_forbidden_keywords(m) else "تركيزك اليوم ينصب على ما يهمك حقاً. ثق بحدسك." for m in ms]
                v += sum(1 for m in ms if TextHelper.check_forbidden_keywords(m))
                c_day["رسائل"][per] = c_ms
            clean.append(c_day)
        self.logger.success(f"تم الفحص. المخالفات: {v}")
        return clean, v
'''

AGENT_6_VARIETY = '''
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger

class VarietyAgent:
    def __init__(self):
        self.logger = get_logger("variety_agent")
        self.intentions = {"صباح": ["نيتي اليوم أن أتفاءل وأوسع صدري.", "نيتي اليوم أن أصبر على ما ينضج ببطء.", "نيتي اليوم أن أتحرك ولا أتأخر."], "ظهيرة": ["نيتي اليوم أن أستمع لقلبي قبل عقلي.", "نيتي اليوم أن أتكلم بما يصلح.", "نيتي اليوم أن أزرع سلامًا حولي."], "مساء": ["نيتي الليلة أن أراجع نهاري بشكر.", "نيتي الليلة أن أغفر وأصفّي قلبي.", "نيتي الليلة أن أسلم أمري وأستقبل غدي برجاء."]}

    def enrich_batch(self, qa_batch: list) -> list:
        self.logger.info(f"الوكيل 6: إضافة النوايا والتنويع")
        final = []
        for day in qa_batch:
            r_day = day.copy()
            r_day["الرسائل_الكاملة"] = {}
            for per, ms in day.get("رسائل", {}).items():
                full = ms.copy()
                full.append(random.choice(self.intentions.get(per, ["نيتي اليوم أن أكون صادقاً."])))
                r_day["الرسائل_الكاملة"][per] = full
            final.append(r_day)
        return final
'''

AGENT_7_ARCHIVING = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger
from utils.helpers import FileHelper

class ArchivingAgent:
    def __init__(self):
        self.logger = get_logger("archiving_agent")
        self.final_dir = Path("output/final_formatted")
        self.final_dir.mkdir(parents=True, exist_ok=True)

    def save_zodiac(self, sign_name: str, enriched_days: list, violations: int):
        self.logger.section(f"الوكيل 7: أرشفة برج {sign_name}")
        struct = [{"التاريخ": d["التاريخ"], "مفتاح_اليوم": d["مفتاح_اليوم"], "صباح": d["الرسائل_الكاملة"].get("صباح",[]), "ظهيرة": d["الرسائل_الكاملة"].get("ظهيرة",[]), "مساء": d["الرسائل_الكاملة"].get("مساء",[])} for d in enriched_days]
        FileHelper.save_json({"البرج": sign_name, "الإحصائيات": {"الأيام": len(struct), "الرسائل": len(struct)*36, "المخالفات": violations}, "الأيام": struct}, str(self.final_dir / f"مفكرة_{sign_name}.json"))
        self.logger.success(f"تم الحفظ النهائي بنجاح")
'''

# ==========================================
# منطق التثبيت التلقائي
# ==========================================

def install_agents():
    print("="*50)
    print("🚀 بدء تثبيت الوكلاء السبعة تلقائياً...")
    print("="*50)
    
    agents_to_create = {
        "agent_1_data.py": AGENT_1_DATA,
        "agent_5_batching.py": AGENT_5_BATCHING,
        "agent_2_insight.py": AGENT_2_INSIGHT,
        "agent_3_text.py": AGENT_3_TEXT,
        "agent_4_qa.py": AGENT_4_QA,
        "agent_6_variety.py": AGENT_6_VARIETY,
        "agent_7_archiving.py": AGENT_7_ARCHIVING
    }
    
    for filename, code in agents_to_create.items():
        filepath = agents_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code.strip())
            print(f"✅ تم إنشاء/تحديث: {filename}")
        except Exception as e:
            print(f"❌ فشل في إنشاء {filename}: {e}")
            
    print("="*50)
    print("✅ انتهى التثبيت! يمكنك الآن تشغيل المنسق العام.")
    print("="*50)

if __name__ == "__main__":
    install_agents()
