from collections import defaultdict
from .base import tool, plain_profile
from backend.rules import load_all, check_eligibility as _check


@tool("rank_schemes")
def rank_schemes(ctx) -> dict:
    prof = plain_profile(ctx.case)
    schemes = load_all()
    results = {sid: _check(s, prof) for sid, s in schemes.items()}
    eligible = [sid for sid, r in results.items() if r["result"] == "eligible"]
    groups = defaultdict(list)
    for sid in eligible:
        g = schemes[sid].exclusive_group
        if g:
            groups[g].append(sid)
    conflicts = [ids for ids in groups.values() if len(ids) > 1]
    recommended = [sid for sid in eligible if not schemes[sid].exclusive_group]
    for ids in groups.values():
        if len(ids) == 1:
            recommended.append(ids[0])
        else:
            amounts = {i: schemes[i].benefit.amount_per_year for i in ids}
            if all(a is not None for a in amounts.values()):
                best = max(amounts, key=amounts.get)
                if list(amounts.values()).count(amounts[best]) == 1:
                    recommended.append(best)  # citizen still chooses
    return {
        "eligible": [{"scheme_id": s, "name": schemes[s].name, "benefit": schemes[s].benefit.text,
                      "reasons": results[s]["reasons"], "verified": schemes[s].verified,
                      "source": results[s]["source"]} for s in eligible],
        "not_eligible": [{"scheme_id": s, "name": schemes[s].name,
                          "reasons": [x for x in r["reasons"] if x["outcome"] in ("not_met", "excluded")],
                          "source": r["source"]}
                         for s, r in results.items() if r["result"] == "not_eligible"],
        "unknown": [{"scheme_id": s, "name": schemes[s].name, "missing_fields": r["missing_fields"],
                     "drafted": schemes[s].drafted, "source": r["source"]} for s, r in results.items() if r["result"] == "unknown"],
        "conflicts": conflicts, "recommended": recommended,
    }
