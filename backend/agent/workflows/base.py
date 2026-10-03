STAGES = ["INTAKE", "MATCH", "PLAN", "COLLECT", "FILL", "REVIEW_CONFIRM", "SUBMIT", "TRACK"]

# order in which missing profile fields are asked
QUESTION_ORDER = ["family_income_annual", "current_level", "institution_type",
                  "marks_pct_class7", "category"]
YES = {"yes", "y", "ok", "okay", "yeah", "haan", "han", "हाँ", "हां", "అవును", "సరే"}
NO = {"no", "n", "nahi", "नहीं", "కాదు", "వద్దు"}
DONT_KNOW = ("don't know", "dont know", "not sure", "no idea", "नहीं पता", "తెలియదు")


def is_yes(t: str) -> bool:
    return t.strip().lower().strip(".!") in YES


def is_no(t: str) -> bool:
    return t.strip().lower().strip(".!") in NO
