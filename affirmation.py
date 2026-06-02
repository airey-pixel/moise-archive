#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매일 오전, MOISĒ 창업자(Airey)를 위한 오늘의 affirmation(affirmation) 1개를 텔레그램으로 발송.
날짜 기반 로테이션이라 매일 다른 문장이 나와요. 별도 메시지로 갑니다.
환경변수: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
import os, datetime as dt, requests

KST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(KST).date()

DECO = ["♡", "⊹", "⟡", "୨୧", "🎀", "🩰", "🫧", "✿", "❀", "✩", "˚₊"]

# MOISĒ 창업자를 위한 다짐 — 버블리하고 단단하게.
AFFIRMATIONS = [
    "내 브랜드는 세상에 없던 무드를 만들어요. 그건 아무도 못 베껴요.",
    "오늘 완벽하지 않아도 괜찮아요. 매일 0.1mm씩 나아가는 중이니까.",
    "MOISĒ는 제품이 아니라 사람들이 갖고 싶은 '느낌'이에요.",
    "작게 시작했다고 작게 끝나는 건 아니에요. 글로시에도 한 통에서 시작했어요.",
    "내 직감은 데이터가 따라잡지 못하는 정보예요. 믿어도 돼요.",
    "거절은 방향을 알려주는 신호일 뿐, 나에 대한 평가가 아니에요.",
    "오늘 내가 보내는 메일 한 통이 6개월 뒤의 바이어를 만들어요.",
    "나는 공장이 없어도 세계로 나가는 브랜드를 만들고 있어요.",
    "완성이 아니라 출시가 먼저예요. 시장이 나머지를 가르쳐줘요.",
    "내 브랜드를 사랑해줄 1,000명이면 충분해요. 전부일 필요 없어요.",
    "지치는 날엔 일을 줄이는 게 아니라 나를 먼저 채워요.",
    "MOISĒ라는 이름을 발음할 때, 사람들은 이미 설레요.",
    "비교는 도둑이에요. 오늘은 어제의 나하고만 경쟁해요.",
    "여성·청년 창업자라는 건 약점이 아니라 내 서사의 핵심이에요.",
    "지금 막막한 건, 아직 안 가본 길 위에 서 있다는 증거예요.",
    "작은 디테일에 집착하는 내 성격이 결국 브랜드의 격을 만들어요.",
    "오늘 하나만 끝내도 충분해요. 모멘텀은 거기서 시작돼요.",
    "내 제품을 처음 쓰는 사람의 표정을 상상해요. 그게 내 연료예요.",
    "돈은 따라오는 거예요. 먼저 사랑받는 브랜드를 만들면.",
    "나는 트렌드를 좇지 않아요. 내가 좋아하는 걸 깊게 팔 뿐이에요.",
    "오늘의 불안은 내가 크게 베팅하고 있다는 뜻이에요. 좋은 신호.",
    "쉬는 것도 일이에요. 번아웃된 대표는 브랜드에 제일 나빠요.",
    "내 이야기를 솔직하게 할수록 사람들은 더 가까이 와요.",
    "K-뷰티의 다음 챕터를 내가 쓰고 있어요. 진심으로.",
    "작은 브랜드의 무기는 빠른 속도와 진짜 사람의 온도예요.",
    "오늘 들은 'No' 하나가 내일의 더 좋은 'Yes'를 위한 자리예요.",
    "나는 모든 걸 알 필요 없어요. 다음 한 걸음만 알면 돼요.",
    "내 취향이 곧 브랜드예요. 그러니 취향을 계속 갈고닦아요.",
    "성장은 직선이 아니라 계단이에요. 지금은 다음 칸을 모으는 중.",
    "오늘 나는 대표답게, 그리고 나답게 결정할 거예요.",
    "남들이 안 된다 한 곳에서 MOISĒ의 빈틈이 보여요.",
    "내 브랜드는 화장품을 파는 게 아니라 자존감을 파는 거예요.",
    "느리게 가도 멈추지만 않으면 결국 도착해요.",
    "오늘 나에게 친절할 것. 그게 가장 생산적인 전략이에요.",
]


def deco_for(d):
    a = DECO[d.toordinal() % len(DECO)]
    b = DECO[(d.toordinal() // 3) % len(DECO)]
    return a, b


def build():
    i = TODAY.toordinal() % len(AFFIRMATIONS)
    a, b = deco_for(TODAY)
    msg = f"{a} 오늘의 affirmation {b}\n\n{AFFIRMATIONS[i]}\n\n— 매기가, MOISĒ 대표님께"
    return msg


def send(msg):
    tok = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        print("토큰/chat_id 미설정 → 출력만\n" + msg)
        return
    try:
        r = requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                          json={"chat_id": cid, "text": msg, "disable_web_page_preview": True}, timeout=20)
        r.raise_for_status()
        print("affirmation 발송 OK", len(msg), "자")
    except Exception as e:
        print("발송 실패", e)


if __name__ == "__main__":
    send(build())
