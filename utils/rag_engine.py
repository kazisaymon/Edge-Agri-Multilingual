# utils/rag_engine.py
# RAG (Retrieval-Augmented Generation) engine
# Uses local SQLite knowledge base — no internet required

from utils.database import search_knowledge, log_query

# Multi-language quick question suggestions
QUICK_QUESTIONS = {
    "bn": [
        "ধানে ব্লাস্ট রোগ হলে কী করবো?",
        "বোরো ধানে কতটুকু সার দিতে হবে?",
        "আমন ধান কখন রোপণ করবো?",
        "মাজরা পোকা দমনের উপায় কী?",
        "AWD পদ্ধতিতে সেচ কীভাবে দেবো?",
        "ধান কাটার সঠিক সময় কখন?",
    ],
    "zh": [
        "水稻稻瘟病怎么处理?",
        "博罗水稻需要多少肥料?",
        "阿曼水稻何时移栽?",
        "如何防治螟虫?",
        "如何进行AWD灌溉?",
        "水稻收割的正确时间是什么时候?",
    ],
    "en": [
        "What to do if rice has blast disease?",
        "How much fertilizer for Boro rice?",
        "When to transplant Aman rice?",
        "How to control stem borer?",
        "How to do AWD irrigation?",
        "When is the right time to harvest rice?",
    ],
}

NO_RESULT_MSG = {
    "bn": "দুঃখিত, এই বিষয়ে আমার জ্ঞানভাণ্ডারে তথ্য নেই। অনুগ্রহ করে কৃষি হেল্পলাইন **16123** এ কল করুন।",
    "zh": "抱歉，我的知识库中没有相关信息。请拨打农业热线 **16123**。",
    "en": "Sorry, I don't have information on this in my knowledge base. Please call the agricultural helpline **16123**.",
}

GREETING_MSG = {
    "bn": "আসসালামুয়ালাইকুম! 🌾 আমি **Edge-Agri চ্যাটবট**। আপনার কৃষি সমস্যা জানান, আমি BRRI জ্ঞানভাণ্ডার থেকে পরামর্শ দেবো।",
    "zh": "您好！🌾 我是 **Edge-Agri 聊天机器人**。请告诉我您的农业问题，我将从BRRI知识库为您提供建议。",
    "en": "Hello! 🌾 I am the **Edge-Agri Chatbot**. Tell me your agricultural problem and I'll provide advice from the BRRI knowledge base.",
}


def answer_query(query: str, lang: str = "bn", district: str = "") -> dict:
    """
    RAG pipeline:
    1. Retrieve top-k relevant documents from knowledge base
    2. Return best match with source citation
    """
    if not query.strip():
        return {"answer": GREETING_MSG.get(lang, GREETING_MSG["en"]),
                "source": "", "confidence": 1.0, "kb_id": None, "found": True}

    results = search_knowledge(query, lang, top_k=3)

    if not results:
        log_query(query, lang, NO_RESULT_MSG.get(lang), None, 0.0, district)
        return {
            "answer": NO_RESULT_MSG.get(lang, NO_RESULT_MSG["en"]),
            "source": "",
            "confidence": 0.0,
            "kb_id": None,
            "found": False,
        }

    best = results[0]

    # Select answer based on language
    if lang == "zh" and best.get("answer_zh"):
        answer = best["answer_zh"]
    elif lang == "en" and best.get("answer_en"):
        answer = best["answer_en"]
    else:
        answer = best["answer_bn"]

    # Simple confidence: keyword overlap ratio
    words = set(query.lower().split())
    keywords = set((best.get("keywords") or "").lower().split(","))
    overlap = len(words & keywords) / max(len(words), 1)
    confidence = min(0.95, 0.60 + overlap * 0.35)

    related = []
    for r in results[1:]:
        if lang == "en":
            q = r.get("question_en") or r["question_bn"]
        else:
            q = r["question_bn"]
        related.append(q)

    log_query(query, lang, answer, best["id"], confidence, district)

    return {
        "answer": answer,
        "source": best.get("source", "BRRI Manual"),
        "category": best.get("category", ""),
        "confidence": round(confidence, 2),
        "kb_id": best["id"],
        "found": True,
        "related": related,
    }
