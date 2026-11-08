# কাঠের হিসাব — Wood Business Manager

বাংলা ভাষার কাঠ ব্যবসার হিসাব ব্যবস্থাপনা ওয়েব অ্যাপ। Django + SQLite দিয়ে শুরু; MySQL-এ নেওয়ার জন্য settings-এ প্রস্তুতি আছে।

## চালু করার নিয়ম (Windows)
1. Python 3.10+ ইনস্টল করুন।
2. ZIP Extract করে `wood_business_manager` ফোল্ডারে যান।
3. Command Prompt খুলে চালান:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. ব্রাউজারে `http://127.0.0.1:8000/` খুলুন।
5. তৈরি করা username/password দিয়ে লগইন করুন।

## macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## মূল ফিচার
- কাস্টমার যোগ ও তালিকা
- বাকিতে বিক্রি রেকর্ড (বিক্রির পরিমাণ/টাকা)
- আংশিক বা পূর্ণ পেমেন্ট গ্রহণ
- স্বয়ংক্রিয় বকেয়া হিসাব
- কাঠের স্টক (কাঠের ধরন, একক, পরিমাণ, ক্রয়মূল্য)
- রিপোর্ট
- প্রিন্ট-ফ্রেন্ডলি কাস্টমার স্টেটমেন্ট
- JSON ব্যাকআপ ডাউনলোড (সুপারইউজার)

## গুরুত্বপূর্ণ ব্যবহারবিধি
- প্রথমে কাঠের ধরন/স্টক যোগ করুন।
- কাস্টমার তৈরি করুন।
- বিক্রি যোগ করার সময় কাঠের পরিমাণ দিলে স্টক কমবে।
- টাকা পেলে Payment যোগ করুন; বকেয়া নিজে থেকে কমবে।
- ভুল এন্ট্রি হলে পুরোনো লেনদেন মুছে না দিয়ে নতুন সংশোধনী এন্ট্রি রাখুন। এই প্রাথমিক সংস্করণে admin থেকে রেকর্ড delete সীমিত রাখা হয়েছে।

## MySQL-এ নেওয়া
`settings.py`-এ `DB_ENGINE=mysql` সেট করে `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` environment variable দিন। তারপর `pip install mysqlclient` (আপনার OS-এর build dependency লাগতে পারে) এবং `python manage.py migrate` চালান।

## Backup
লগইন করে `/backup/` খুললে JSON ফাইল ডাউনলোড হবে। ব্যাকআপ ফাইল নিরাপদ স্থানে রাখুন। এটি প্রাথমিক JSON export; restore/import screen পরবর্তী সংস্করণে যোগ করা যাবে।
