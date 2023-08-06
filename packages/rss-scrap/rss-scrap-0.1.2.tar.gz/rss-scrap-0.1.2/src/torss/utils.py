import sys
from datetime import timezone, datetime


def eprint(*a, **kw):
    kw["file"] = sys.stderr
    print(*a, **kw)


def die(msg, code=1):
    eprint(msg, file=sys.stderr)
    sys.exit(code)


def expect(expr, msg, code=1):
    if not expr:
        die(msg, code)


async def fetch_bs(session, url):
    from bs4 import BeautifulSoup

    async with session.get(url) as resp:
        return BeautifulSoup(await resp.text(), "html.parser")


def pub_date_fmt(dt: datetime):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def utcnow():
    tm = datetime.now(timezone.utc)
    return pub_date_fmt(tm)
