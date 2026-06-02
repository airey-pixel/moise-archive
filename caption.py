#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매일 오전, 바로 올릴 수 있는 MOISĒ 인스타 캡션 1개(영어→한국어→일본어)를 텔레그램으로 발송.
날짜 기반 로테이션. 해시태그 5개, MOISĒ 철자 고정, 과장 수치 없음.
환경변수: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
import os, datetime as dt, requests

KST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(KST).date()
DECO = ["♡", "⊹", "⟡", "🫧", "✿", "˚₊", "୨୧"]

# 영어=효능·결과 / 한국어=감성·무드(존댓말+명사형 믹스) / 일본어=일본 감성·韓国コスメ
CAPTIONS = [
    {"en": "Glass-glow skin starts the moment you slow down. ⊹",
     "ko": "바쁜 아침에도, 단 한 겹의 윤기. 오늘의 피부는 제가 챙길게요 ♡",
     "jp": "忙しい朝にも、ひと塗りのツヤ。今日の肌は私におまかせ。",
     "tags": "#MOISĒ #모아제 #kbeauty #글로우스킨 #韓国コスメ"},
    {"en": "A ritual, not a routine. Press, breathe, glow. 🫧",
     "ko": "루틴이 아니라 리추얼. 누르고, 숨 쉬고, 빛나는 순간 ⟡",
     "jp": "ルーティンじゃなくてリチュアル。押さえて、ひと呼吸、ツヤ肌へ。",
     "tags": "#MOISĒ #스킨케어리추얼 #kbeautyroutine #뷰티루틴 #スキンケア"},
    {"en": "Bare-skin confidence is the best filter. ✿",
     "ko": "가장 좋은 필터는 결국 내 피부예요. 민낯에 자신감 한 스푼 ♡",
     "jp": "一番のフィルターは、自分の肌。すっぴんに自信をひとさじ。",
     "tags": "#MOISĒ #민낯자신감 #cleanbeauty #글래스스킨 #素肌美"},
    {"en": "Hydration you can feel — dewy, never heavy. ⊹",
     "ko": "무겁지 않게, 촉촉하게. 속부터 차오르는 수분감 🫧",
     "jp": "重くないのにうるおう。内側から満ちる水分感。",
     "tags": "#MOISĒ #수분크림 #dewyskin #kskincare #うるおい"},
    {"en": "Made in Korea, made with care. The details you can feel. ⟡",
     "ko": "한국에서, 정성껏. 손끝에 닿는 디테일까지 ♡",
     "jp": "韓国から、ていねいに。指先で感じるディテールまで。",
     "tags": "#MOISĒ #메이드인코리아 #kbeauty #madeinkorea #韓国スキンケア"},
    {"en": "Less shelf, more glow. One hero, zero clutter. ✿",
     "ko": "복잡한 단계는 덜고, 빛은 더하고. 핵심 하나면 충분해요 ⊹",
     "jp": "工程はミニマルに、ツヤは最大に。これひとつで十分。",
     "tags": "#MOISĒ #미니멀스킨케어 #lessismore #뷰티템 #ミニマルケア"},
    {"en": "That soft-focus glow — like light caught on skin. ⟡",
     "ko": "조명을 머금은 듯한 결. 오늘 피부, 은은하게 빛나는 무드 ♡",
     "jp": "光をまとったような肌。今日のツヤは、ふんわり上品に。",
     "tags": "#MOISĒ #윤광피부 #glassskin #kbeautyglow #ツヤ肌"},
    {"en": "Self-care is not a luxury. It's the strategy. 🫧",
     "ko": "나를 돌보는 시간은 사치가 아니라 전략이에요 ⊹",
     "jp": "自分をいたわる時間は、ぜいたくじゃなくて戦略。",
     "tags": "#MOISĒ #셀프케어 #selfcare #뷰티감성 #ご自愛"},
    {"en": "Clean formula, clear conscience, clearer skin. ✿",
     "ko": "깨끗한 처방, 가벼운 마음, 맑아지는 피부 ♡",
     "jp": "クリーンな処方、軽やかな心、澄んだ肌へ。",
     "tags": "#MOISĒ #클린뷰티 #cleanbeauty #저자극 #敏感肌ケア"},
    {"en": "Morning glow in three seconds. Yes, really. ⊹",
     "ko": "3초면 끝나는 아침 윤기. 바쁜 날일수록 더 빛나게 ♡",
     "jp": "3秒で完成、朝のツヤ。忙しい日こそ、きれいに。",
     "tags": "#MOISĒ #아침루틴 #morningglow #데일리뷰티 #時短ケア"},
    {"en": "Your skin remembers kindness. Be gentle today. ⟡",
     "ko": "피부는 다정함을 기억해요. 오늘은 더 부드럽게 🫧",
     "jp": "肌はやさしさを覚えてる。今日はもっとそっと。",
     "tags": "#MOISĒ #순한스킨케어 #gentleskincare #피부장벽 #肌にやさしい"},
    {"en": "Quiet luxury for your everyday face. ✿",
     "ko": "매일의 얼굴에, 조용한 럭셔리 한 겹 ⊹",
     "jp": "毎日の素肌に、静かなラグジュアリーをひと塗り。",
     "tags": "#MOISĒ #데일리럭셔리 #quietluxury #뷰티무드 #上質ケア"},
    {"en": "Glow from within — skincare that works while you rest. 🫧",
     "ko": "쉬는 동안에도 일하는 케어. 안에서부터 차오르는 빛 ♡",
     "jp": "休んでいる間も働くケア。内側から満ちるツヤ。",
     "tags": "#MOISĒ #나이트케어 #glowfromwithin #수면팩 #ナイトケア"},
    {"en": "K-beauty isn't a trend here. It's the craft. ⟡",
     "ko": "우리에게 K-뷰티는 유행이 아니라 정성이에요 ⊹",
     "jp": "私たちにとってK-beautyは流行じゃなく、こだわり。",
     "tags": "#MOISĒ #kbeauty #케이뷰티 #뷰티장인 #韓国コスメ好き"},
    {"en": "Effortless is the hardest look — we made it easy. ✿",
     "ko": "가장 어려운 건 '꾸안꾸'. 그걸 쉽게 만들었어요 ♡",
     "jp": "一番むずかしいのは“がんばらない美しさ”。それを簡単に。",
     "tags": "#MOISĒ #꾸안꾸 #effortlessbeauty #내추럴메이크업 #抜け感"},
]


def build():
    c = CAPTIONS[TODAY.toordinal() % len(CAPTIONS)]
    d = DECO[TODAY.toordinal() % len(DECO)]
    msg = (f"📸 오늘의 인스타 캡션 {d}\n\n"
           f"{c['en']}\n\n{c['ko']}\n\n{c['jp']}\n\n{c['tags']}")
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
        print("caption 발송 OK", len(msg), "자")
    except Exception as e:
        print("발송 실패", e)


if __name__ == "__main__":
    send(build())
