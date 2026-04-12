# utils/database.py
import sqlite3
import bcrypt
import os
from datetime import datetime

DB_PATH = "data/edge_agri.db"

def get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        question_bn TEXT NOT NULL,
        question_en TEXT,
        answer_bn TEXT NOT NULL,
        answer_en TEXT,
        answer_zh TEXT,
        source TEXT DEFAULT 'BRRI Manual',
        keywords TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS farmer_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_text TEXT NOT NULL,
        query_lang TEXT DEFAULT 'bn',
        response_text TEXT,
        matched_kb_id INTEGER,
        confidence_score REAL,
        district TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS disease_detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        plant_type TEXT,
        detected_disease TEXT,
        confidence REAL,
        severity TEXT,
        recommendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed admin user (password: admin123)
    c.execute("SELECT COUNT(*) FROM admin_users")
    if c.fetchone()[0] == 0:
        pw_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        c.execute("INSERT INTO admin_users (username, password_hash, role) VALUES (?,?,?)",
                  ("admin", pw_hash, "admin"))

    # Seed knowledge base
    c.execute("SELECT COUNT(*) FROM knowledge_base")
    if c.fetchone()[0] == 0:
        seed_knowledge(c)

    conn.commit()
    conn.close()

def seed_knowledge(c):
    entries = [
        ("ধানের রোগ",
         "ধানে ব্লাস্ট রোগ কী এবং কীভাবে প্রতিরোধ করা যায়?",
         "What is rice blast disease and how to prevent it?",
         "ধান ব্লাস্ট রোগ Magnaporthe oryzae ছত্রাক দ্বারা সৃষ্ট। পাতায় ধূসর কেন্দ্র ও বাদামি প্রান্তবিশিষ্ট ডায়মন্ড আকৃতির দাগ দেখা দেয়। প্রতিকার: ট্রাইসাইক্লাজোল বা আইসোপ্রোথিওলেন (৭৫০ মিলি/হেক্টর) স্প্রে করুন। BRRI dhan29 বা BRRI dhan49 জাত ব্যবহার করুন।",
         "Rice blast is caused by Magnaporthe oryzae. Diamond-shaped grey spots with brown margins appear on leaves. Treatment: Spray Tricyclazole or Isoprothiolane (750ml/hectare). Use BRRI dhan29 or dhan49 resistant varieties.",
         "水稻稻瘟病由稻瘟病菌引起。叶片出现菱形灰色斑点，边缘棕色。防治：喷施三环唑（750ml/公顷）。使用BRRI dhan29或dhan49抗病品种。",
         "BRRI Disease Management Manual 2023", "blast,ব্লাস্ট,ছত্রাক,দাগ,পাতা,rice blast"),

        ("ধানের রোগ",
         "বাদামি দাগ রোগের লক্ষণ ও প্রতিকার কী?",
         "What are symptoms and treatment of brown spot disease?",
         "বাদামি দাগ রোগ Cochliobolus miyabeanus ছত্রাক দ্বারা হয়। পাতায় গোলাকার বাদামি দাগ পড়ে, মাঝে সাদা কেন্দ্র থাকে। প্রতিকার: ম্যানকোজেব ২ গ্রাম/লিটার পানিতে স্প্রে করুন। পটাশ সার বাড়ান।",
         "Brown spot is caused by Cochliobolus miyabeanus. Circular brown spots with white center on leaves. Treatment: Spray Mancozeb 2g/liter. Increase potash fertilizer.",
         "褐斑病由宫部旋孢腔菌引起。叶片出现圆形褐色斑点，中心白色。防治：喷施代森锰锌2g/升。增施钾肥。",
         "BRRI Disease Management Manual 2023", "brown spot,বাদামি দাগ,ছত্রাক,পাতা"),

        ("সার ব্যবস্থাপনা",
         "এক বিঘা জমিতে বোরো ধানের জন্য কতটুকু সার লাগবে?",
         "How much fertilizer for Boro rice per bigha?",
         "বোরো ধানের জন্য প্রতি বিঘায় (৩৩ শতাংশ): ইউরিয়া ২০-২৫ কেজি, টিএসপি ১০-১২ কেজি, এমওপি ১০-১২ কেজি, জিপসাম ৬-৮ কেজি। ইউরিয়া তিন ভাগে দিন: রোপণের ১০-১৫ দিন পর, কুশি ও থোড় আসার সময়।",
         "For Boro rice per bigha: Urea 20-25kg, TSP 10-12kg, MOP 10-12kg, Gypsum 6-8kg. Apply urea in 3 splits: 10-15 days after transplanting, at tillering, at panicle initiation.",
         "每比加博罗水稻施肥：尿素20-25公斤，三重过磷酸钙10-12公斤，氯化钾10-12公斤，石膏6-8公斤。分三次施尿素。",
         "BRRI Fertilizer Recommendation 2023", "সার,ইউরিয়া,টিএসপি,বোরো,বিঘা,fertilizer"),

        ("পোকামাকড়",
         "মাজরা পোকা দমনের উপায় কী?",
         "How to control stem borer in rice?",
         "মাজরা পোকা ধানের মারাত্মক শত্রু। লক্ষণ: ডেড হার্ট (কুশি অবস্থায়) এবং হোয়াইট ইয়ার (থোড় অবস্থায়)। দমন: কার্বোফুরান ৩জি (১৭ কেজি/হেক্টর) অথবা ক্লোরপাইরিফস স্প্রে করুন। আলোক ফাঁদ ব্যবহার করুন।",
         "Stem borer causes Dead Heart at tillering and White Ear at panicle stage. Control: Apply Carbofuran 3G (17kg/hectare) or spray Chlorpyrifos. Use light traps.",
         "螟虫在分蘖期造成枯心，在穗期造成白穗。防治：施用呋喃丹3G（17公斤/公顷）或喷施毒死蜱。使用诱虫灯。",
         "BRRI Pest Management Guide 2023", "মাজরা,stem borer,পোকা,ডেড হার্ট"),

        ("আবহাওয়া ও মৌসুম",
         "কখন আমন ধান রোপণ করা উচিত?",
         "When to transplant Aman rice?",
         "আমন ধান রোপণ: বীজতলায় বপন জুন প্রথম সপ্তাহ থেকে জুলাই দ্বিতীয় সপ্তাহ। মূল জমিতে রোপণ জুলাই মাঝামাঝি থেকে আগস্ট মাঝামাঝি। ৩০-৩৫ দিন বয়সের চারা রোপণ করুন। বন্যাপ্রবণ এলাকায় BRRI dhan52 বা dhan79 ব্যবহার করুন।",
         "Aman rice: Seedbed sowing from first week of June to second week of July. Transplant mid-July to mid-August. Use 30-35 day old seedlings. In flood-prone areas use BRRI dhan52 or dhan79.",
         "阿曼水稻：6月第一周到7月第二周播种育秧。7月中旬到8月中旬移栽。使用30-35天秧苗。洪涝地区使用BRRI dhan52或dhan79。",
         "BRRI Crop Calendar 2023", "আমন,রোপণ,মৌসুম,সময়,aman"),

        ("সেচ ব্যবস্থাপনা",
         "ধান চাষে AWD পদ্ধতিতে সেচ কীভাবে দেবো?",
         "How to use AWD irrigation method in rice?",
         "AWD (Alternate Wetting and Drying) পদ্ধতি: রোপণ থেকে কুশি পর্যন্ত ৫-৭ সেমি পানি রাখুন। কুশি পরিপূর্ণ হলে ৩-৫ দিন শুকাতে দিন। পানি ১৫ সেমি নিচে নামলে সেচ দিন। থোড় ও শীষ আসার সময় পানি আবশ্যক। পাকার ১৫ দিন আগে সেচ বন্ধ। AWD-তে ৩০% পানি সাশ্রয় হয়।",
         "AWD method: Maintain 5-7cm water from transplanting to tillering. After full tillering, allow 3-5 days drying. Re-irrigate when water drops 15cm below surface. Water essential at panicle and heading. Stop 15 days before harvest. AWD saves 30% water.",
         "AWD方法：移栽到分蘖保持5-7厘米水层。分蘖完成后干燥3-5天。水位下降15厘米时重新灌溉。穗期和抽穗期必须有水。收获前15天停止灌溉。AWD节水30%。",
         "BRRI Water Management Manual 2023", "সেচ,পানি,AWD,irrigation"),

        ("ফসল কাটা",
         "ধান কাটার সঠিক সময় কখন?",
         "When is the right time to harvest rice?",
         "ধান কাটার সময়: শীষের ৮০-৮৫% ধান পাকলে কাটুন। শীষ বের হওয়ার ৩০-৩৫ দিন পর। পাকা ধানের রং হলুদ-সোনালি হবে। দেরিতে কাটলে ঝরে পড়ার ক্ষতি বাড়ে। ভোরে বা বিকেলে কাটুন। কাটার পর দ্রুত মাড়াই করুন।",
         "Harvest when 80-85% of grains are mature. Usually 30-35 days after heading. Ripe grains will be yellow-golden. Late harvest increases shattering loss. Harvest in morning or evening. Thresh quickly after cutting.",
         "当80-85%的谷粒成熟时收割。通常在抽穗后30-35天。成熟谷粒呈金黄色。收割过晚会增加脱粒损失。在清晨或傍晚收割。收割后迅速脱粒。",
         "BRRI Post-Harvest Management 2023", "কাটা,মাড়াই,পাকা,harvest"),

        ("মাটি পরীক্ষা",
         "মাটি পরীক্ষা কেন করা দরকার?",
         "Why do soil testing?",
         "মাটি পরীক্ষা কেন জরুরি: সঠিক সার সুপারিশের জন্য, অতিরিক্ত সার অপচয় রোধে, মাটির স্বাস্থ্য জানতে। কীভাবে: জমির বিভিন্ন স্থান থেকে ৫-৬টি মাটির নমুনা সংগ্রহ করুন। মিশিয়ে ৫০০ গ্রাম রাখুন। নিকটবর্তী উপজেলা কৃষি অফিস বা BRRI ল্যাবে পাঠান।",
         "Soil testing importance: For correct fertilizer recommendations, prevent over-fertilization, know soil health. How to: Collect 5-6 soil samples from different spots. Mix and keep 500g. Send to Upazila Agriculture Office or BRRI lab.",
         "土壤测试的重要性：获得正确的施肥建议，防止过度施肥，了解土壤健康状况。方法：从不同地点采集5-6个土壤样品。混合保留500克。送至乡镇农业办公室或BRRI实验室。",
         "BRRI Soil Health Manual 2023", "মাটি,soil test,পরীক্ষা"),
    ]
    c.executemany("""
        INSERT INTO knowledge_base
        (category, question_bn, question_en, answer_bn, answer_en, answer_zh, source, keywords)
        VALUES (?,?,?,?,?,?,?,?)
    """, entries)

# ── Query Functions ──────────────────────────────────────────────

def search_knowledge(query: str, lang: str = "bn", top_k: int = 3):
    conn = get_conn()
    c = conn.cursor()
    words = [w.strip() for w in query.split() if len(w.strip()) > 1]
    if not words:
        conn.close()
        return []

    conditions = []
    params = []
    for w in words[:6]:
        conditions.append("(question_bn LIKE ? OR keywords LIKE ? OR answer_bn LIKE ? OR question_en LIKE ?)")
        params.extend([f"%{w}%", f"%{w}%", f"%{w}%", f"%{w}%"])

    sql = f"SELECT * FROM knowledge_base WHERE {' OR '.join(conditions)} LIMIT {top_k}"
    c.execute(sql, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def log_query(query_text, lang, response_text, kb_id, confidence, district=""):
    conn = get_conn()
    conn.execute("""INSERT INTO farmer_queries
        (query_text, query_lang, response_text, matched_kb_id, confidence_score, district)
        VALUES (?,?,?,?,?,?)""",
        (query_text, lang, response_text, kb_id, confidence, district))
    conn.commit()
    conn.close()

def log_detection(image_name, plant_type, disease, confidence, severity, recommendation):
    conn = get_conn()
    conn.execute("""INSERT INTO disease_detections
        (image_name, plant_type, detected_disease, confidence, severity, recommendation)
        VALUES (?,?,?,?,?,?)""",
        (image_name, plant_type, disease, confidence, severity, recommendation))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_conn()
    c = conn.cursor()
    stats = {}
    c.execute("SELECT COUNT(*) FROM farmer_queries"); stats["total_queries"] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM farmer_queries WHERE date(created_at)=date('now')"); stats["today_queries"] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM knowledge_base"); stats["kb_count"] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM disease_detections"); stats["detections"] = c.fetchone()[0]
    c.execute("SELECT AVG(confidence_score) FROM farmer_queries WHERE confidence_score > 0"); avg = c.fetchone()[0]; stats["avg_confidence"] = round((avg or 0) * 100, 1)
    conn.close()
    return stats

def get_all_queries(limit=50):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM farmer_queries ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_detections(limit=50):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM disease_detections ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_kb():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM knowledge_base ORDER BY category, id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_kb_entry(category, question_bn, answer_bn, source, keywords, question_en="", answer_en=""):
    conn = get_conn()
    conn.execute("""INSERT INTO knowledge_base
        (category, question_bn, question_en, answer_bn, answer_en, source, keywords)
        VALUES (?,?,?,?,?,?,?)""",
        (category, question_bn, question_en, answer_bn, answer_en, source, keywords))
    conn.commit()
    conn.close()

def delete_kb_entry(entry_id):
    conn = get_conn()
    conn.execute("DELETE FROM knowledge_base WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def verify_admin(username, password):
    conn = get_conn()
    row = conn.execute("SELECT password_hash FROM admin_users WHERE username=?", (username,)).fetchone()
    conn.close()
    if not row:
        return False
    return bcrypt.checkpw(password.encode(), row["password_hash"].encode())
