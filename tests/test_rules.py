from backend.rules import load_all, check_eligibility

S = load_all()["nmmss"]
BASE = {"family_income_annual": 180000, "current_level": 9, "institution_type": "government",
        "marks_pct_class7": 60, "category": "GEN"}


def test_eligible():
    assert check_eligibility(S, BASE)["result"] == "eligible"


def test_not_eligible_income():
    assert check_eligibility(S, {**BASE, "family_income_annual": 900000})["result"] == "not_eligible"


def test_missing_is_unknown_not_false():
    p = {k: v for k, v in BASE.items() if k != "family_income_annual"}
    r = check_eligibility(S, p)
    assert r["result"] == "unknown" and "family_income_annual" in r["missing_fields"]


def test_exclusion_private():
    assert check_eligibility(S, {**BASE, "institution_type": "private"})["result"] == "not_eligible"


def test_relaxation_for_sc():
    p = {**BASE, "marks_pct_class7": 50}
    assert check_eligibility(S, {**p, "category": "GEN"})["result"] == "not_eligible"
    assert check_eligibility(S, {**p, "category": "SC"})["result"] == "eligible"


def test_relaxation_unknown_category():
    p = {k: v for k, v in {**BASE, "marks_pct_class7": 50}.items() if k != "category"}
    assert check_eligibility(S, p)["result"] == "unknown"


def test_undrafted_scheme_is_unknown():
    from backend.rules.schema import Scheme
    stub = Scheme(scheme_id="stub", name="Stub", drafted=False)
    assert check_eligibility(stub, BASE)["result"] == "unknown"
