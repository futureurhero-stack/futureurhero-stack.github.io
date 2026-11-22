# 발음 규칙 코너(sceneshadow/index.html)의 data-say 예시를 미국 영어 음성 파일로 만든다.
# 브라우저 내장 음성은 기기마다 달라(맥 크롬은 한국어 목소리가 영어를 읽기도 함) 미리 만든 파일을 튼다.
# 사용: python3 tools/make_say.py   (예시를 바꾸거나 추가하면 다시 돌린다. 이미 있는 파일은 건너뜀)
import base64, json, os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'sceneshadow', 'index.html')
OUT = os.path.join(ROOT, 'sceneshadow', 'assets', 'say')
KEY = open(os.path.expanduser('~/.config/sceneshadow/google_tts_key')).read().strip()
VOICE = 'en-US-Chirp3-HD-Aoede'
# 철자대로 주면 음성이 또박또박 읽어 규칙이 안 들린다. 줄어든 소리를 들려줘야 하는 예시는 소리 나는 철자로 준다.
# 여기를 바꾸면 해당 mp3 를 지우고 다시 돌린다.
SPOKEN = {
    'want to go': 'wanna go',
    'I want to go home': 'I wanna go home',
    'tell him': 'tellim',  # "tell 'im" 은 따옴표를 I(아이)로 읽었다
    'going home': "goin' home",
    'a lot of': 'a lotta',
    'did you': 'didja',
    'fades in': 'fadesin',  # 띄어 쓰면 짧은 조각이라 기계음처럼 끊어 읽었다
}


def slug(text):
    # 페이지 스크립트의 slug 와 같아야 한다
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


os.makedirs(OUT, exist_ok=True)
texts = sorted(set(re.findall(r'data-say="([^"]+)"', open(PAGE, encoding='utf-8').read())))
for t in texts:
    path = os.path.join(OUT, slug(t) + '.mp3')
    if os.path.exists(path):
        continue
    body = {
        'input': {'text': SPOKEN.get(t, t)},
        'voice': {'languageCode': 'en-US', 'name': VOICE},
        'audioConfig': {'audioEncoding': 'MP3'},
    }
    req = urllib.request.Request(
        'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + KEY,
        data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    audio = json.load(urllib.request.urlopen(req))['audioContent']
    open(path, 'wb').write(base64.b64decode(audio))
    print('만듦', t, '→', os.path.basename(path))
print(len(texts), '개 예시')
