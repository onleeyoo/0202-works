#!/usr/bin/env python3
"""0202 Works dashboard data tool.

  python3 _src/works.py decrypt PASSWORD [out.json]   # index.html -> plain items json (default: _src/items.json)
  python3 _src/works.py build   PASSWORD [in.json]    # items json + template -> encrypted index.html

items.json is a list of {id, area, topic, title, status, next, updated, changed?, change?}
  topic:   주제 (예: 0202Transition, 0202Swatch). 채팅 단위가 아니라 주제 단위로 묶는다
  area:    프리미어 플러그인 | 0202PD 웹·서비스 | 인스타 | 블로그
  status:  진행중 | 대기 | 아이디어 | 완료
  updated: YYYY-MM-DD (last time it was discussed)
  changed/change: date + label ("추가" / "상태 변경" / "내용 수정") shown as a tag for 2 days
Never commit the plain items json (.gitignore covers _src/items.json).
"""
import base64, datetime, json, os, re, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index.html")
TEMPLATE = os.path.join(HERE, "template.html")
DEFAULT_JSON = os.path.join(HERE, "items.json")
AREAS = {"프리미어 플러그인", "0202PD 웹·서비스", "인스타", "블로그"}
STATUSES = {"진행중", "대기", "아이디어", "완료"}


def key(pw, salt, it):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw.encode())


def decrypt(pw, out):
    html = open(INDEX, encoding="utf-8").read()
    enc = json.loads(re.search(r"const ENC = (\{.*?\});", html).group(1))
    b = lambda s: base64.b64decode(s)
    data = AESGCM(key(pw, b(enc["salt"]), enc["iter"])).decrypt(b(enc["iv"]), b(enc["ct"]), None)
    items = json.loads(data)
    json.dump(items, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"decrypted {len(items)} items -> {out}")


def validate(items):
    ids = set()
    for r in items:
        for f in ("id", "area", "title", "status", "next", "updated"):
            assert r.get(f), f"missing {f}: {r}"
        assert r["area"] in AREAS, f"bad area: {r}"
        assert r["status"] in STATUSES, f"bad status: {r}"
        datetime.date.fromisoformat(r["updated"])
        assert r["id"] not in ids, f"duplicate id {r['id']}"
        ids.add(r["id"])


def build(pw, src):
    items = json.load(open(src, encoding="utf-8"))
    validate(items)
    it = 200000
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key(pw, salt, it)).encrypt(iv, json.dumps(items, ensure_ascii=False).encode(), None)
    enc = {"salt": base64.b64encode(salt).decode(), "iv": base64.b64encode(iv).decode(),
           "ct": base64.b64encode(ct).decode(), "iter": it}
    today = (datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))).strftime("%m.%d")
    t = open(TEMPLATE, encoding="utf-8").read().replace("__ENC__", json.dumps(enc)).replace("__UPDATED__", today)
    open(INDEX, "w", encoding="utf-8").write(t)
    print(f"built index.html with {len(items)} items")


if __name__ == "__main__":
    cmd, pw = sys.argv[1], sys.argv[2]
    path = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_JSON
    {"decrypt": decrypt, "build": build}[cmd](pw, path)
