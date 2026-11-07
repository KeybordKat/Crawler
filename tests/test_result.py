from crawler.core.result import Result


def test_success_and_failure():
    assert Result.success(distance_cm=12.5).to_dict() == {
        "ok": True, "data": {"distance_cm": 12.5}, "error": None}
    r = Result.failure("blocked", reason="obstacle")
    assert not r.ok and r.error == "blocked" and r.data["reason"] == "obstacle"
