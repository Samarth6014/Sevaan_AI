# FROZEN contracts (E writes, A edits after telling the team)

## Profile fields (inputs to rules)
age, gender, state, category (GEN|SC|ST|OBC|EWS), minority_community (bool), disability_percent,
family_income_annual, current_level (class number | "UG" | "PG" | "diploma"),
institution_type (government|aided|local_body|private|central_school|residential),
institution_recognized, study_mode (regular|distance), marks_pct_class7, marks_pct_class10,
marks_pct_class12, class12_board_percentile, receiving_other_scholarship, orphan,
parent_in_armed_or_police_services, domicile_state.
Missing value => rule is `unknown`, never `false`.

## Rule ops
<=, >=, ==, in, not_in, is_true, is_false

## Scheme result
not_eligible: any all_of rule false OR any none_of rule true.
eligible: every all_of true AND no none_of true or unknown AND at least one rule exists.
otherwise unknown (+ missing_fields). A scheme with no drafted rules is always unknown.

## Stages
INTAKE, MATCH, PLAN, COLLECT, FILL, REVIEW_CONFIRM, SUBMIT, TRACK

## Tools
extract_profile, check_eligibility, rank_schemes, plan_documents, read_document, prefill_form,
validate_form, answer_faq, request_confirmation, submit_application, track_status,
schedule_reminder, explain. Contracts: backend/agent/tools/base.py.

## Confirmation token
HMAC(SECRET_KEY, case_id + sha256(sorted form JSON)). Any change to form => token invalid.

## Roles
citizen, helper (only granted cases), admin (metadata only, never documents).
