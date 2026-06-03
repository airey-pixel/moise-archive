#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매일 오전, 바로 올릴 수 있는 MOISĒ 인스타 캡션 1개(영어→한국어→일본어)를 텔레그램으로 발송.
각 언어 = 훅+본문+참여유도까지 완성형. 날짜 로테이션. 해시태그 5개, MOISĒ 철자 고정, 과장 수치 없음.
환경변수: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
import os, datetime as dt, requests

KST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(KST).date()
DECO = ["♡", "⊹", "⟡", "🫧", "✿", "˚₊", "୨୧"]

CAPTIONS = [
    {"en": "Your skin, but make it glass. ✨\nThat lit-from-within glow isn't a filter — it's hydration that actually sinks in, layer by layer. Three seconds in the morning, dewy all the way to golden hour.\nDrop your one non-negotiable step below 👇",
     "ko": "오늘도 한 겹의 윤기로 시작 ⊹\n필터 없이 빛나는 피부, 비결은 속까지 스며드는 수분이에요. 바쁜 아침엔 단 3초, 그래도 하루 종일 촉촉하게.\n여러분의 '이건 절대 안 빼먹어' 단계는 뭐예요? 댓글로 알려주세요 💬",
     "jp": "今日もひと塗りのツヤから ⟡\nフィルターなしで輝く肌の秘密は、奥まで届く水分。忙しい朝は3秒だけ、それでも一日中うるおいキープ。\nあなたの“絶対外せない”ステップは？コメントで教えてね",
     "tags": "#MOISĒ #글라스스킨 #kbeauty #글로우스킨 #韓国コスメ"},
    {"en": "Skincare shouldn't feel like homework. 🫧\nWe stripped the 10-step routine down to what your skin actually craves — clean, gentle, effortless. Less shelf, more glow.\nHow many steps is YOUR morning routine?",
     "ko": "스킨케어가 숙제처럼 느껴지지 않게 ⊹\n10단계는 덜어내고, 피부가 진짜 원하는 것만. 순하고, 가볍고, 부담 없이. 단계는 줄이고 윤기는 더하고.\n여러분의 아침 루틴은 몇 단계예요?",
     "jp": "スキンケアは宿題じゃない 🫧\n10ステップは手放して、肌が本当に求めるものだけ。やさしくて、軽くて、頑張らない。工程はミニマルに、ツヤは最大に。\nあなたの朝のルーティンは何ステップ？",
     "tags": "#MOISĒ #미니멀스킨케어 #cleanbeauty #kbeautyroutine #ミニマルケア"},
    {"en": "Bare skin is the new full glam. ✿\nThe best filter has always been healthy skin. Pressed in, breathed out — a quiet morning ritual that lets your real glow do the talking.\nTeam bare-skin or team full-beat?",
     "ko": "민낯이 곧 가장 완벽한 메이크업 ⟡\n가장 좋은 필터는 결국 건강한 피부예요. 꾹 누르고, 천천히 숨 쉬고 — 진짜 윤기가 말하게 하는 조용한 아침 리추얼.\n여러분은 민낯파인가요, 풀메파인가요?",
     "jp": "すっぴんこそ、最高のメイク ✿\n一番のフィルターは、いつだって健やかな肌。押さえて、ひと呼吸 — 本当のツヤに語らせる、静かな朝のリチュアル。\nあなたはすっぴん派？しっかりメイク派？",
     "tags": "#MOISĒ #민낯자신감 #glassskin #cleanbeauty #素肌美"},
    {"en": "Made in Korea. Made slowly. Made for you. ⊹\nEvery texture, every scent, every detail — obsessed over until it feels like a small luxury in your palm. This is K-beauty as craft, not trend.\nWhat made you fall for K-beauty?",
     "ko": "한국에서, 천천히, 당신을 위해 ♡\n텍스처 하나, 향 하나, 디테일 하나까지 — 손안의 작은 럭셔리가 될 때까지 매만진 정성. 유행이 아니라 '정성'으로서의 K-뷰티.\n여러분이 K-뷰티에 빠진 순간은 언제였나요?",
     "jp": "韓国から、ていねいに、あなたのために ⟡\nテクスチャーも、香りも、ディテールも — 手のひらの小さな贅沢になるまで磨いた一品。流行じゃなく“こだわり”としてのK-beauty。\nあなたがK-beautyに惹かれた瞬間は？",
     "tags": "#MOISĒ #메이드인코리아 #kbeauty #madeinkorea #韓国スキンケア"},
    {"en": "Glow doesn't sleep. 🌙\nWhile you rest, your skin gets to work — drinking in moisture, waking up softer, bouncier, brighter. Self-care isn't a luxury. It's the strategy.\nSave this as your tonight reminder.",
     "ko": "윤기는 잠들지 않아요 🫧\n쉬는 동안에도 피부는 일하는 중. 수분을 머금고, 더 부드럽고 탱탱하게, 더 환하게 깨어나는 밤. 나를 돌보는 시간은 사치가 아니라 전략이에요.\n오늘 밤 리마인더로 저장해두세요.",
     "jp": "ツヤは眠らない 🌙\n休んでいる間も、肌は働いてる。水分を抱えて、もっとやわらかく、もっとふっくら、もっと明るく目覚める夜。ご自愛は、ぜいたくじゃなくて戦略。\n今夜のリマインダーに保存してね。",
     "tags": "#MOISĒ #나이트케어 #glowfromwithin #수면팩 #ナイトケア"},
    {"en": "Effortless is the hardest look — so we made it easy. ✿\nThat undone, just-woke-up-glowing finish? It takes the right base, not more product. One hero step, zero clutter, all you.\nTag the friend who always looks effortless.",
     "ko": "가장 어려운 건 '꾸안꾸' — 그래서 쉽게 만들었어요 ⊹\n방금 일어난 듯 자연스러운 윤광은 제품 가짓수가 아니라 '좋은 베이스'에서 와요. 핵심 한 단계, 군더더기 제로, 온전히 나답게.\n늘 꾸안꾸로 예쁜 그 친구를 태그해보세요.",
     "jp": "一番むずかしいのは“抜け感” — だから簡単にした ✿\n起きたばかりみたいな自然なツヤは、アイテムの数じゃなくて“良いベース”から。ひとつの主役ステップ、ムダなし、まるごと自分らしく。\nいつも抜け感のあるあの友達をタグ付けして。",
     "tags": "#MOISĒ #꾸안꾸 #effortlessbeauty #내추럴메이크업 #抜け感"},
    {"en": "Hydration you can feel — dewy, never heavy. 🫧\nNo tight, no sticky, no 30-minute wait. Just that fresh, plump finish that makes you keep touching your own cheek (no judgment, we do too).\nDewy or matte — what's your finish?",
     "ko": "무겁지 않게, 촉촉하게 — 느껴지는 수분 ⟡\n당기지 않고, 끈적이지 않고, 30분 기다릴 필요도 없이. 자꾸 볼을 만지게 되는 산뜻하고 탱탱한 마무리 (저희도 그래요).\n여러분은 촉촉 마무리파? 매트파?",
     "jp": "重くないのにうるおう — 感じる水分 🫧\nつっぱらない、ベタつかない、30分待つ必要もない。つい頬を触りたくなる、みずみずしくてふっくらした仕上がり（私たちもです）。\nうるツヤ派？マット派？",
     "tags": "#MOISĒ #수분크림 #dewyskin #kskincare #うるおい"},
    {"en": "A brand isn't what we sell — it's how you feel. ⊹\nMOISĒ was never about a bottle. It's the two quiet minutes that are just for you, before the day asks for everything. Confidence, in a jar.\nWhat does your me-time look like?",
     "ko": "브랜드는 파는 게 아니라, 당신이 느끼는 거예요 ♡\nMOISĒ는 한 통의 화장품이 아니에요. 하루가 모든 걸 요구하기 전, 오롯이 나를 위한 2분. 한 통에 담긴 자존감.\n여러분의 '나만의 시간'은 어떤 모습인가요?",
     "jp": "ブランドは“売るもの”じゃなく、“感じるもの” ⟡\nMOISĒは一本のコスメじゃない。一日がすべてを求める前の、自分だけの2分間。瓶に詰めた自信。\nあなたの“私の時間”はどんな感じ？",
     "tags": "#MOISĒ #셀프케어 #selfcare #뷰티감성 #ご自愛"},
    {"en": "Quiet luxury, for your everyday face. ✿\nNot loud. Not extra. Just that expensive-skin look that whispers instead of shouts. The kind of glow people can't quite place — but never forget.\nComment ✨ if your skin deserves this today.",
     "ko": "매일의 얼굴에, 조용한 럭셔리 ⊹\n요란하지 않게, 과하지 않게. 외치지 않고 속삭이는 '비싼 피부' 무드. 콕 집어 말할 순 없지만 절대 잊히지 않는 윤기.\n오늘 내 피부에게 선물하고 싶다면 댓글에 ✨ 남겨주세요.",
     "jp": "毎日の素肌に、静かなラグジュアリー ✿\n派手じゃなく、やりすぎず。叫ばずにささやく“高見え肌”のムード。うまく言えないけど、忘れられないツヤ。\n今日の肌にこれをあげたいなら、コメントに ✨ を。",
     "tags": "#MOISĒ #데일리럭셔리 #quietluxury #뷰티무드 #上質ケア"},
    {"en": "Your skin remembers kindness. 🤍\nStressed, tired, over-exfoliated? Today, go gentle. Barrier-first, fragrance-light, made for the days your skin needs a soft place to land.\nWhat does your skin need more of right now?",
     "ko": "피부는 다정함을 기억해요 ⟡\n지치고, 예민하고, 너무 많이 만진 날엔 — 오늘은 부드럽게. 장벽 먼저, 향은 은은하게, 피부가 쉬어갈 자리가 필요한 날을 위해.\n지금 내 피부에게 가장 필요한 건 뭘까요?",
     "jp": "肌は、やさしさを覚えてる 🤍\n疲れて、敏感で、こすりすぎた日は — 今日はそっと。バリア優先、香りはひかえめ、肌が休める場所が必要な日のために。\n今、あなたの肌に一番必要なものは？",
     "tags": "#MOISĒ #순한스킨케어 #gentleskincare #피부장벽 #敏感肌ケア"},
]


def build():
    c = CAPTIONS[TODAY.toordinal() % len(CAPTIONS)]
    d = DECO[TODAY.toordinal() % len(DECO)]
    return "📸 오늘의 인스타 캡션 " + d + "\n\n" + c["en"] + "\n\n" + c["ko"] + "\n\n" + c["jp"] + "\n\n" + c["tags"]


def send(msg):
    tok = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    cid = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not tok or not cid:
        print("토큰/chat_id 미설정 → 출력만\n" + msg); return
    try:
        r = requests.post("https://api.telegram.org/bot" + tok + "/sendMessage",
                          json={"chat_id": cid, "text": msg, "disable_web_page_preview": True}, timeout=20)
        r.raise_for_status(); print("caption 발송 OK", len(msg), "자")
    except Exception as e:
        print("발송 실패", e)


if __name__ == "__main__":
    send(build())
