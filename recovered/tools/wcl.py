"""Shared WarcraftLogs v2 API helper: reads credentials from .env, caches the token, runs GraphQL queries."""
import base64, json, os, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

HOST = os.environ.get("WCL_HOST", "https://fresh.warcraftlogs.com")
API = HOST + "/api/v2/client"
TOKEN_URL = HOST + "/oauth/token"
ROOT = Path(__file__).resolve().parents[2]  # wow-tbc-logs/
TOKEN_CACHE = Path(__file__).resolve().parent / ".token-cache.json"


def load_env():
    """Read WCL_CLIENT_ID / WCL_CLIENT_SECRET from the environment or the nearest .env file."""
    for path in (Path.cwd() / ".env", ROOT / ".env"):
        if path.exists():
            for line in path.read_text().splitlines():
                m = re.match(r"\s*([A-Z_]+)\s*=\s*(.*?)\s*$", line)
                if m:
                    os.environ.setdefault(m.group(1), m.group(2).strip("'\""))
    cid, secret = os.environ.get("WCL_CLIENT_ID"), os.environ.get("WCL_CLIENT_SECRET")
    if not cid or not secret:
        sys.exit("Missing WCL_CLIENT_ID / WCL_CLIENT_SECRET (put them in %s)" % (ROOT / ".env"))
    return cid, secret


def token():
    if TOKEN_CACHE.exists():
        cached = json.loads(TOKEN_CACHE.read_text())
        if cached.get("host") == HOST and cached["expires"] > time.time() + 300:
            return cached["access_token"]
    cid, secret = load_env()
    auth = base64.b64encode(("%s:%s" % (cid, secret)).encode()).decode()
    req = urllib.request.Request(TOKEN_URL, urllib.parse.urlencode({"grant_type": "client_credentials"}).encode(),
                                 {"Authorization": "Basic " + auth})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    TOKEN_CACHE.write_text(json.dumps({"host": HOST, "access_token": d["access_token"],
                                       "expires": time.time() + d.get("expires_in", 3600)}))
    os.chmod(TOKEN_CACHE, 0o600)
    return d["access_token"]


def query(gql, variables=None, retries=5):
    body = json.dumps({"query": gql, "variables": variables or {}}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API, body, {"Authorization": "Bearer " + token(),
                                                     "Content-Type": "application/json"})
            d = json.load(urllib.request.urlopen(req, timeout=120))
            if "errors" in d:
                raise RuntimeError(d["errors"])
            return d["data"]
        except Exception as e:
            if attempt == retries - 1:
                raise
            print("retry %d: %s" % (attempt + 1, e), file=sys.stderr)
            time.sleep(5 * (attempt + 1))


def report_code(arg):
    """Accept a bare report code or any warcraftlogs report URL."""
    m = re.search(r"reports/([A-Za-z0-9]+)", arg)
    return m.group(1) if m else arg.strip("<> ")


def codes_from_file(path):
    """All report codes found in a text/markdown file of links, de-duplicated, in order."""
    seen = []
    for code in re.findall(r"warcraftlogs\.com/reports/([A-Za-z0-9]+)", Path(path).read_text()):
        if code not in seen:
            seen.append(code)
    return seen
