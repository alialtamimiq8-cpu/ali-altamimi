"""
Text Agent - وكيل الدمج والسيناريو
=====================================
يحول البيانات الرقمية إلى نصوص نفسية باستخدام القوالب والقواميس
"""

import json
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.helpers import FileHelper

class TextAgent:
    """وكيل توليد النصوص بالقوالب"""
    
    def __init__(self, config_path: str = "config"):
        self.logger = get_logger("text_agent")
        self.config_path = Path(config_path)
        
        # تحميل ملفات التغذية (القواميس والقوالب)
        self.templates = FileHelper.load_json(self.config_path / "Templates.json")
        self.planets = FileHelper.load_json(self.config_path / "Planets_dictionry.json")
        self.houses = FileHelper.load_json(self.config_path / "houses_dictionary.json")
        self.sentiments = FileHelper.load_json(self.config_path / "Sentimenet_words.json")
        
        # قائمة النوايا الثابتة (من دليل المشروع)
        self.intentions = {
            "صباح_المشتري": "نيتي اليوم أن أتفاءل وأوسع صدري.",
            "صباح_زحل": "نيتي اليوم أن أصبر على ما ينضج ببطء.",
            "صباح_المريخ": "نيتي اليوم أن أتحرك ولا أتأخر.",
            "ظهيرة_القمر": "نيتي اليوم أن أستمع لقلبي قبل عقلي.",
            "ظهيرة_عطارد": "نيتي اليوم أن أتكلم بما يصلح.",
            "ظهيرة_الزهرة": "نيتي اليوم أن أزرع سلامًا حولي.",
            "مساء_الشمس": "نيتي الليلة أن أراجع نهاري بشكر.",
            "مساء_الزهرة": "نيتي الليلة أن أغفر وأصفّي قلبي.",
            "مساء_زحل": "نيتي الليلة أن أسلم أمري وأستقبل غدي برجاء."
        }

    def _get_random_alias(self, house_num: int) -> str:
        """الحصول على مرادف عشوائي للبيت لتجنب الرتابة"""
        house_str = str(house_num)
        if house_str in self.houses:
            aliases = self.houses[house_str].get("aliases", [])
            return random.choice(aliases) if aliases else "مجالك"
        return "مجالك"

    def _get_random_verb(self, planet_name: str) -> str:
        """الحصول على فعل عشوائي للكوكب"""
        if planet_name in self.planets:
            verbs = self.planets[planet_name].get("verbs", [])
            return random.choice(verbs) if verbs else "يتحرك"
        return "يتحرك"

    def _generate_message_for_house(self, planet_name: str, house_num: int, is_moon_angular: bool = False) -> str:
        """
        توليد رسالة واحدة لكوكب في بيت معين
        يستخدم القوالب من 1 إلى 9
        """
        house_alias = self._get_random_alias(house_num)
        planet_verb = self._get_random_verb(planet_name)
        
        # قالب 5: القمر في البيوت الزاوية (1، 4، 7، 10)
        if planet_name == "القمر" and is_moon_angular:
            return self.templates["template_5_moon_angular"].format(house_alias=house_alias)
            
        # قالب 6: زحل
        if planet_name == "زحل":
            return self.templates["template_6_saturn"].format(house_alias=house_alias)
            
        # قالب 7: المشتري
        if planet_name == "المشتري":
            return self.templates["template_7_jupiter"].format(house_alias=house_alias)
            
        # قالب 8: المريخ
        if planet_name == "المريخ":
            return self.templates["template_8_mars"].format(house_alias=house_alias)
            
        # قالب 9: الزهرة
        if planet_name == "الزهرة":
            return self.templates["template_9_venus"].format(house_alias=house_alias)
            
        # القالب الافتراضي (1): كوكب منفرد
        return self.templates["template_1_single"].format(house_alias=house_alias, planet_verb=planet_verb)

    def _get_intention(self, time_period: str, dominant_planet: str) -> str:
        """تحديد النية المناسبة للرسالة 12"""
        key = f"{time_period}_{dominant_planet}"
        return self.intentions.get(key, "نيتي اليوم أن أكون صادقاً مع نفسي.")

    def process_batch(self, batch_file_path: str) -> list:
        """
        معالجة حزمة واحدة (30 يوماً) وتوليد النصوص لها
        
        Returns:
            قائمة بالأيام بعد توليد نصوصها
        """
        self.logger.info(f"جاري توليد النصوص للحزمة: {batch_file_path}")
        batch_data = FileHelper.load_json(batch_file_path)
        days = batch_data.get("days", [])
        processed_days = []
        
        # الكواكب بالترتيب المطلوب للرسائل من 1 إلى 11
        planets_order = ["الشمس", "القمر", "عطارد", "الزهرة", "المريخ", "المشتري", "زحل"]
        
        for day in days:
            date = day["التاريخ"]
            periods_text = {}
            
            for period_name, period_data in day["الفترات"].items():
                houses_data = period_data["البيوت"]
                messages = []
                
                # توليد الـ 11 رسالة الأولى
                for planet in planets_order:
                    house_num = houses_data.get(planet, 0)
                    is_angular = (planet == "القمر" and house_num in [1, 4, 7, 10])
                    msg = self._generate_message_for_house(planet, house_num, is_angular)
                    messages.append(msg)
                
                # إضافة الرسالة 12 (النية) - نعتبر المشتري هو المهيمن افتراضياً
                intention = self._get_intention(period_name, "المشتري")
                messages.append(intention)
                
                periods_text[period_name] = messages
                
            # إضافة اليوم بعد معالجته
            processed_days.append({
                "التاريخ": date,
                "الرسائل": periods_text
            })
            
        self.logger.success(f"تم توليد نصوص {len(processed_days)} يوم في هذه الحزمة")
        return processed_days

if __name__ == "__main__":
    # للتجربة
    agent = TextAgent()
    # ضع مسار أي حزمة من الحزم التي أنشأها الوكيل 2 لتجربتها
    agent.process_batch("data/batches/السرطان/batch_1.json")
