# 🌙 مفكرة النوايا اليومية – 12 برجًا

مشروع متخصص لإنشاء 12 مفكرة يومية، كل واحدة تغطي 549 يوماً (من 1 يوليو 2026 إلى 31 ديسمبر 2027).

## 📌 معلومات المشروع

- **الفترة الزمنية**: 1 يوليو 2026 - 31 ديسمبر 2027 (549 يوم)
- **عدد المفكرات**: 12 مفكرة (برج واحد لكل مفكرة)
- **الأوقات المغطاة**: صباح (06:30)، ظهيرة (12:00)، مساء (17:30)
- **الرسائل اليومية**: 36 رسالة يومية (12 رسالة × 3 أوقات)
- **إجمالي الرسائل**: ~237,168 رسالة

## 🎯 الهدف

توليد مفكرات يومية بلغة نفسية حكيمة، مستندة إلى حركة الكواكب، دون ذكر مباشر للفلك أو الأبراج.

## 📁 هيكل المشروع

```
ali-altamimi/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   ├── houses_dictionary.json
│   ├── planets_dictionary.json
│   ├── relationships_dictionary.json
│   ├── intentions_rules.json
│   ├── forbidden_keywords.json
│   └── templates.json
├── data/
│   ├── input/
│   │   └── الخريطة_الشاملة_الاحترافية_بالتفسير_العربي.xlsx
│   └── processed/
├── agents/
│   ├── __init__.py
│   ├── data_agent.py
│   ├── text_agent.py
│   ├── intentions_agent.py
│   ├── pdf_agent.py
│   ├── qa_agent.py
│   └── orchestrator_agent.py
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── helpers.py
│   └── logger.py
├── tests/
│   └── test_data_agent.py
├── output/
│   └── PDFs/
└── logs/
```

## 🚀 البدء السريع

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. إضافة ملف البيانات
ضع ملف Excel في:
```
data/input/الخريطة_الشاملة_الاحترافية_بالتفسير_العربي.xlsx
```

### 3. تشغيل الوكيل الأول
```bash
python agents/data_agent.py
```

## 📚 الوكلاء المتاحة

| الوكيل | الوصف |
|--------|--------|
| **Data Agent** | استخراج ومعالجة البيانات |
| **Text Agent** | توليد الرسائل والنصوص |
| **Intentions Agent** | توليد المفاتيح والنوايا |
| **PDF Agent** | تصميم وإنشاء ملفات PDF |
| **QA Agent** | التحقق من الجودة |
| **Orchestrator Agent** | تشغيل خط الأنابيب كاملاً |

## 📝 الترخيص

هذا المشروع مفتوح المصدر

## 👤 المؤلف

تم بناؤه بواسطة فريق التطوير - 2026
