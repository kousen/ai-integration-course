"""No-key tests for the checker: the code that compares a critique with the requirements.

    python3 -m pytest tests -v     # from examples/image-set; runs in well under a second
"""
from critique import check, disagreements, extract_json, text_matches

REQS = ["There is a robot in the image", "There is a whiteboard in the image"]


def critique_with(*met):
    return {"checks": [{"requirement": r, "met": m, "evidence": "x"} for r, m in zip(REQS, met)]}


def test_all_met_is_ok():
    assert check(REQS, critique_with(True, True)) == {"ok": True, "problems": [], "unmet": [], "missing": [], "extra": []}


def test_unmet_requirement_is_reported_by_name():
    result = check(REQS, critique_with(True, False))
    assert not result["ok"]
    assert result["unmet"] == ["There is a whiteboard in the image"]


def test_missing_requirement_is_a_problem_even_if_the_rest_pass():
    partial = {"checks": [{"requirement": REQS[0], "met": True}]}
    result = check(REQS, partial)
    assert not result["ok"]
    assert result["missing"] == [REQS[1]]


def test_invented_requirement_is_flagged():
    c = critique_with(True, True)
    c["checks"].append({"requirement": "The lighting is dramatic", "met": True})
    result = check(REQS, c)
    assert result["extra"] == ["The lighting is dramatic"]
    assert not result["ok"]


def test_requirement_text_is_matched_loosely():
    c = {"checks": [{"requirement": "there is a robot in the image.", "met": True},
                    {"requirement": "There is a WHITEBOARD in the image", "met": True}]}
    assert check(REQS, c)["ok"]


def test_non_json_reply_is_a_failed_critique_not_a_crash():
    result = check(REQS, extract_json("Sorry, I can't see any image."))
    assert not result["ok"]
    assert result["missing"] == REQS


def test_json_inside_prose_and_fences_is_extracted():
    text = 'Here you go:\n```json\n{"checks": [{"requirement": "a", "met": true}]}\n```'
    assert extract_json(text) == {"checks": [{"requirement": "a", "met": True}]}


def test_text_match_ignores_case_and_punctuation():
    assert text_matches("AI Integration", "  ai integration! ")
    assert not text_matches("AI Integration", "AI Integratlon")   # the October 19 story
    assert not text_matches("AI Integration", None)


def test_disagreements_between_two_critics():
    a = [{"name": "p1", "critique": critique_with(True, True), "text_read": "AI Integration"}]
    b = [{"name": "p1", "critique": critique_with(True, False), "text_read": "AI Integratlon"}]
    d = disagreements(a, b)
    assert len(d) == 1
    assert {x["requirement"] for x in d[0]["diffs"]} == {REQS[1], "<text read>"}
    assert disagreements(a, a) == []
