#!/usr/bin/env bash
# Runs every test in the project: ./tests/run.sh
# Python tests use .venv if it exists (numpy, pandas, scikit-learn; see requirements.txt).
# Browser tests need Google Chrome; set CHROME to use another path.
set -u
cd "$(dirname "$0")/.."
status=0

echo "== Python: time-to-sort charts and sample-data prototype"
PY=.venv/bin/python
[ -x "$PY" ] || PY=python3
py_out=$("$PY" -m unittest discover -s tests -p "test_*.py" 2>&1) || status=1
printf '%s\n' "$py_out" | grep -vE "^(wrote |check: )"

echo
echo "== Browser: solution prototype"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
dom=$("$CHROME" --headless=new --disable-gpu --allow-file-access-from-files --window-size=1600,1100 \
  --virtual-time-budget=120000 --dump-dom "file://$PWD/tests/prototype.test.html" 2>/dev/null)
results=$(printf '%s' "$dom" | "$PY" -c '
import html, re, sys
m = re.search(r"<pre id=\"results\">(.*?)</pre>", sys.stdin.read(), re.S)
print(html.unescape(m.group(1)) if m else "No results: did Chrome run?")')
echo "$results"
echo "$results" | tail -1 | grep -q "^PASS" || status=1

echo
[ $status -eq 0 ] && echo "All tests passed." || echo "Some tests failed."
exit $status
