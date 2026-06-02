#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매일 affirmation/마케팅팁/인스타캡션을 data/archive.json 에 한 줄(하루) 누적.
→ 나중에 웹사이트(GitHub Pages)가 이 JSON 을 읽어 타임라인으로 보여줌. 별도 DB 불필요.
"""
import json, os, datetime as dt
import affirmation, marketing, caption

KST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(KST).date()
PATH = "data/archive.json"


def load():
    if os.path.exists(PATH):
        try:
            return json.load(open(PATH, encoding="utf-8"))
        except Exception:
            return []
    return []


def main():
    data = load()
    today = str(TODAY)
    if any(e.get("date") == today for e in data):
        print("이미 오늘 기록됨:", today)
        return
    ai = affirmation.AFFIRMATIONS[TODAY.toordinal() % len(affirmation.AFFIRMATIONS)]
    t = marketing.TIPS[TODAY.toordinal() % len(marketing.TIPS)]
    cap = caption.CAPTIONS[TODAY.toordinal() % len(caption.CAPTIONS)]
    data.append({
        "date": today,
        "affirmation": ai,
        "tip": {"title": t[0], "insight": t[1], "action": t[2], "ref": t[3]},
        "caption": {"en": cap["en"], "ko": cap["ko"], "jp": cap["jp"], "tags": cap["tags"]},
    })
    os.makedirs("data", exist_ok=True)
    json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("archive 기록 OK", today, "/ 누적", len(data), "일")


if __name__ == "__main__":
    main()
