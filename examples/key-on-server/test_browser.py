"""A browser-driven check of the key-on-server page. Start server.py or Server.java first.

  pip install playwright && playwright install chromium     # once
  python3 -m pytest test_browser.py -v

It drives a real browser: types a question, clicks Ask, waits for an answer, and then
checks what the browser was allowed to see. The last two assertions are the point.
"""
from playwright.sync_api import sync_playwright

URL = "http://localhost:8000"


def test_page_answers_and_the_key_never_reaches_the_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        requests = []
        page.on("request", lambda r: requests.append((r.url, r.headers.get("authorization"))))

        page.goto(URL)
        assert "sk-or" not in page.content()                          # no key in the page source
        page.fill("#q", "Reply with the single word PONG.")
        page.click("form button")
        page.wait_for_function("document.querySelector('#out').textContent.length > 1", timeout=90_000)
        out = page.inner_text("#out")
        browser.close()

    assert not out.startswith("Error"), out
    assert "pong" in out.lower()
    assert all(auth is None for _, auth in requests)                  # no Authorization header left the browser
    assert all("openrouter" not in url for url, _ in requests)         # the browser never called the provider
    assert any(url.endswith("/api/ask") for url, _ in requests)        # it called our server
