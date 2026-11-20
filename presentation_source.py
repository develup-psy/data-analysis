"""데이터 분석·시각화 강의의 편집 가능한 슬라이드 원고."""

from __future__ import annotations

from html import escape


SLIDES: list[dict[str, str]] = []


def add(kind: str, part: str, title: str, lead: str, body: str = "", note: str = "", source: str = "") -> None:
    SLIDES.append(dict(kind=kind, part=part, title=title, lead=lead, body=body, note=note, source=source))


def card(number: str, title: str, detail: str, extra: str = "") -> str:
    return f'<article class="card reveal"><span class="card-number">{number}</span><h2>{title}</h2><p>{detail}</p>{extra}</article>'


def cards(items: list[tuple[str, str, str]], columns: int = 3) -> str:
    return f'<div class="cards columns-{columns}">' + "".join(card(*item) for item in items) + "</div>"


def flow(items: list[tuple[str, str]]) -> str:
    return '<div class="flow">' + "".join(
        f'<div class="flow-node reveal"><b>{i + 1:02d}</b><strong>{title}</strong><small>{detail}</small></div>'
        for i, (title, detail) in enumerate(items)
    ) + "</div>"


def prompt_cards(items: list[tuple[str, str, str]]) -> str:
    result = ['<div class="prompt-list">']
    for number, title, prompt in items:
        result.append(
            '<article class="prompt-item reveal">'
            f'<span class="prompt-number">{escape(number)}</span>'
            f'<div><h2>{escape(title)}</h2><p>{escape(prompt.splitlines()[0])}</p></div>'
            '<div class="prompt-actions"><button type="button" class="view-prompt">내용 보기</button>'
            '<button type="button" class="copy-prompt">프롬프트 복사</button></div>'
            f'<template class="prompt-text">{escape(prompt.strip())}</template>'
            '</article>'
        )
    result.append('</div><p class="prompt-help">각 버튼은 해당 질문의 전체 문장만 복사합니다. ‘내용 보기’에서 복사 전 확인할 수 있습니다.</p>')
    return "".join(result)


add('cover', 'OPENING', '데이터 분석 및 시각화', '데이터에서 근거를 찾고, 설득력 있는 결과물로 공유하기',
    '<div class="cover-visual" aria-hidden="true"><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div><div class="orbit orbit-c"></div><div class="orbit-center"></div><span class="cover-dot dot-a"></span><span class="cover-dot dot-b"></span><span class="cover-dot dot-c"></span></div>',
    '강의 시작. 두 번의 만남에서 수강생이 문제를 정의하고 데이터를 살펴 인사이트를 작성한 뒤, HTML 결과물로 공유한다. 먼저 완성 예시를 보여주고 각 단계의 판단을 직접 해본다.')

add('toc', 'OPENING', '오늘부터 만들 결과', '완성본을 먼저 보고, 같은 순서를 자신의 데이터에 적용합니다.',
    cards([
        ('01', '프로젝트 결과 시연', '뷰티 트렌드와 통신사 이탈 분석의 목표와 결과물 형태를 확인합니다.'),
        ('02', '1일차 · 분석', '수집·EDA·전처리·시각화·인사이트와 텍스트 마이닝을 실습합니다.'),
        ('03', '2일차 · 공유', '분석 결과를 HTML로 구성하고 Agent 작업 환경에서 검토합니다.'),
    ]),
    '원고의 큰 흐름을 그대로 소개한다. 결과물 시연을 먼저 놓아 이후 개념 설명의 목적을 분명히 한다.')

add('chapter', '01 · 프로젝트 결과 시연', '프로젝트 결과 시연', '두 사례가 데이터에서 제안까지 어떻게 연결되는지 봅니다.')

add('content', '01 · 프로젝트 결과 시연', '2026 뷰티 트렌드 분석', '공공·소셜 데이터를 결합해 소비 흐름을 해석하는 프로젝트입니다.',
    '<div class="beauty-placeholder"><div><span class="eyebrow">BEAUTY PROJECT</span><h2>뷰티 결과물 추가 예정</h2><p>문제 정의 → 데이터 수집 → 트렌드 해석 → 시각화·제안</p></div><div class="placeholder-symbol">B</div></div><div class="callout">현재는 분석 자료만 준비돼 있습니다. 최종 시연 화면이 완성되면 이 위치에 연결합니다.</div>',
    '이 자리는 수강생에게 두 프로젝트가 있음을 보여주기 위한 자리다. 수치나 결론을 임의로 만들지 않는다. 결과물 완성 후 같은 위치에 화면과 링크를 추가한다.')

add('content', '01 · 프로젝트 결과 시연', '통신사 이탈 패턴 분석 및 제안', '가입 초기 이탈을 질문으로 정의하고, 여러 기록을 연결해 실행안을 만듭니다.',
    '<div class="demo-layout"><div class="demo-image"><img src="{{TELECOM_IMAGE}}" alt="통신사 고객 분석 결과 보고서 표지 미리보기"></div><div class="demo-text"><span class="eyebrow">GOOREUM MOBILE</span><h2>질문에서 실행까지</h2><ol><li>가입 초기 이탈이라는 분석 질문 선택</li><li>고객·회선·이용·상담 기록 연결</li><li>차이의 근거와 한계 확인</li><li>검증 가능한 조치 제안</li></ol><a class="primary-link" href="{{TELECOM_HREF}}" target="_blank" rel="noopener">분석 결과 HTML 열기 ↗</a></div></div>',
    '결과 보고서 전체를 읽기보다 분석 질문, 근거, 제안이 이어지는 구조를 짧게 시연한다. 실제 보고서는 별도 탭에서 연다. 이 자료의 사례는 강사 예시이며 수강생은 다른 질문을 선택할 수 있다.',
    '자료: 구름모바일 강사 예시 보고서')

add('content', '01 · 프로젝트 결과 시연', '이틀 동안 남길 산출물', '오늘의 분석 초안이 다음 시간의 HTML 결과물로 이어집니다.',
    '<div class="deliverables"><article class="deliverable reveal"><span>11.21 · 1일차</span><h2>분석 초안</h2><p>문제 정의 · 출처와 품질 점검 · EDA · 전처리 · 인사이트</p></article><div class="deliverable-arrow">→</div><article class="deliverable reveal"><span>11.28 · 2일차</span><h2>최종 결과물</h2><p>시각화 · 근거 설명 · 제안 · 한계가 포함된 HTML</p></article></div>',
    '두 날짜의 제출 수준을 구분해 설명한다. 1일차는 완성된 보고서보다 분석의 기준과 근거를 남기는 데 집중한다.')

add('chapter', '02 · 1일차 강의', '데이터 분석 및 인사이트', '분석 단계마다 무엇을 확인하고 남겨야 하는지 익힙니다.')

add('content', '02 · 데이터 분석 프로세스', '데이터 분석의 여섯 단계', '문제 정의에서 보고와 공유까지 하나의 질문을 따라갑니다.',
    flow([('문제 정의', '누구의 어떤 결정을 돕는가'), ('데이터 수집', '필요한 근거를 확보'), ('전처리', '기준과 형식을 정리'), ('탐색·분석', '차이와 패턴 확인'), ('인사이트', '의미와 한계 해석'), ('보고·공유', '행동으로 연결')]) + '<div class="callout">실무에서는 초기 EDA로 오류를 찾고 전처리한 뒤, 다시 탐색하는 과정을 반복합니다.</div>',
    '원고의 여섯 단계는 유지한다. 강의 순서는 EDA를 먼저 살피고 전처리로 돌아가는 형태이므로 선형 절차로만 오해하지 않도록 반복을 강조한다.')

add('content', '02 · 데이터 수집', '좋은 데이터는 질문에서 시작합니다', '파일을 먼저 모으기보다 분석 대상과 기간, 단위를 먼저 정합니다.',
    cards([('질문', '무엇을 비교할까?', '예: 지역별 인구 규모인가, 특정 연령의 비중인가?'), ('대상', '한 행은 무엇인가?', '사람·지역·회선·월 등 기록의 단위를 확인합니다.'), ('기준', '언제의 값인가?', '수집일과 기준일, 누락된 기간을 구분합니다.')]),
    '예시 데이터가 많아도 질문이 불분명하면 필요한 컬럼과 분석 단위가 정해지지 않는다. 수강생의 프로젝트 질문을 한 문장으로 받는다.')

add('content', '02 · 데이터 수집', '데이터 유형과 수집 경로', '형식과 출처가 다르면 품질을 확인하는 방법도 달라집니다.',
    '<div class="comparison"><article class="comparison-card reveal"><span>정형 데이터</span><h2>표로 읽는 기록</h2><p>CSV · 엑셀 · 데이터베이스</p><small>열 정의, 단위, 결측치를 확인</small></article><article class="comparison-card reveal"><span>비정형 데이터</span><h2>문장과 콘텐츠</h2><p>리뷰 · 댓글 · 이미지 · 영상</p><small>수집 범위, 중복, 맥락을 확인</small></article></div><div class="source-strip">내부 시스템 · 공공데이터 · 공식 API · 공개 웹 자료</div>',
    '내부·외부 출처를 대조한다. 웹 수집은 자료의 출처와 이용 조건을 확인한 뒤 진행한다. 여기서는 코드를 설명하기보다 프로젝트에서 어떤 데이터를 고를지 판단하게 한다.')

add('content', '02 · 데이터 수집', '수집 전에 확인할 네 가지', '출처와 기준을 기록해야 나중에 결과를 설명할 수 있습니다.',
    cards([('01', '출처', '어디에서 공개했으며 어떤 목적으로 생성됐는가?'), ('02', '기준 시점', '언제 측정한 데이터이고 얼마나 자주 바뀌는가?'), ('03', '파일 형식', 'CSV·JSON·API 중 무엇이며 어떻게 읽는가?'), ('04', '이용 범위', '수업 자료로 재배포할 수 있는가?')], 4) + '<div class="source-strip">예시: 공공데이터포털 · 서울열린데이터광장 · KOSIS · OECD Data</div>',
    '원고의 공공데이터 사이트 목록은 한 줄 예시로 압축한다. 수강생이 실제 데이터셋의 출처 URL과 기준일을 결과물에 남기게 한다.')

add('chapter', '03 · EDA', '탐색적 데이터 분석', '분석 전에 데이터의 모양과 품질을 먼저 읽습니다.')

add('content', '03 · EDA', 'EDA에서 먼저 묻는 질문', '요약 통계와 그래프는 데이터의 이상한 지점을 찾는 도구입니다.',
    cards([('01', '구조', '몇 행·몇 열이며 숫자와 문자는 어떻게 나뉘는가?'), ('02', '분포', '대표값과 퍼짐은 어떤가? 특정 구간에 몰렸는가?'), ('03', '품질', '빈 값·중복·타입 오류·극단값은 어디에 있는가?')]) + '<div class="callout">첫 탐색 → 수정할 기준 결정 → 전처리 → 다시 탐색</div>',
    'EDA의 목적은 무조건 그래프를 많이 만드는 것이 아니라 데이터가 어떤 질문에 답할 수 있는지 확인하는 것이다.')

add('content', '03 · EDA', '평균과 중앙값이 다르게 말할 때', '극단값 하나가 평균을 움직일 수 있습니다.',
    '<div class="stats-scene"><div class="value-row"><span>2</span><span>3</span><span>3</span><span>4</span><span class="outlier">28</span></div><div class="stat-pair"><div><small>평균</small><strong>8</strong><p>전체 합 ÷ 개수</p></div><div><small>중앙값</small><strong>3</strong><p>정렬한 가운데 값</p></div></div></div><div class="callout">최솟값·최댓값·표준편차·사분위수는 중심과 퍼짐을 함께 읽을 때 사용합니다.</div>',
    '2, 3, 3, 4, 28의 평균은 8, 중앙값은 3이다. 평균이 틀렸다는 뜻이 아니라 무엇을 대표하는지 질문해야 한다. 표준편차는 평균 주변의 퍼짐, 사분위수는 정렬된 위치를 나타낸다.')

add('content', '03 · EDA', '사분위수와 IQR', '중간 50%의 폭으로 극단값 후보를 살펴봅니다.',
    '<div class="iqr-visual"><div class="iqr-track"><span>최솟값</span><span>Q1</span><span>중앙값</span><span>Q3</span><span>최댓값</span><i class="iqr-box"></i></div><div class="iqr-formula"><strong>IQR = Q3 − Q1</strong><p>후보 범위: Q1 − 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과</p></div></div><div class="callout">이 범위 밖의 값은 확인할 후보입니다. 실제 오류인지 희귀한 관측인지 따로 판단합니다.</div>',
    '범위(max-min)는 양 끝값에 민감하다. IQR은 가운데 절반의 폭이다. 1.5배 규칙은 일반적 탐색 기준이며 삭제 규칙이 아니다.')

add('content', '03 · Spotify 실습', 'Spotify.csv를 먼저 읽어봅시다', '데이터셋의 지표를 정의하고 장르별 비교 기준을 확인합니다.',
    '<div class="metric-row"><div class="metric reveal"><strong>114,000</strong><span>행</span></div><div class="metric reveal"><strong>21</strong><span>열</span></div><div class="metric reveal"><strong>0.779</strong><span>kids 장르의 평균 danceability</span></div></div><div class="callout">높은 danceability는 이 데이터셋의 점수입니다. 장르의 음악적 우열이나 선호를 뜻하지 않습니다.</div>',
    '실습 데이터에서 직접 계산한 수치다. 각 장르는 1,000곡으로 구성되어 있지만 수강생이 계산 과정에서 건수를 확인하게 한다. kids가 상위라는 결과는 지표의 의미를 묻는 계기로 쓴다.',
    '자료: lecture/실습/Spotify.csv · examples.py')

spotify_prompts = [
    ('01', '컬럼 읽기', '첨부한 Spotify.csv의 컬럼 이름과 의미를 표로 정리해줘. 데이터에 없는 설명은 추정이라고 표시해줘.'),
    ('02', '변수 유형', '첨부한 Spotify.csv에서 수치형 컬럼과 범주형 컬럼을 구분해줘. 식별자처럼 숫자로 계산하면 안 되는 열도 표시해줘.'),
    ('03', '요약 통계', '첨부한 Spotify.csv의 수치형 컬럼별 건수, 평균, 중앙값, 최솟값, 최댓값, 표준편차를 표로 보여줘.'),
    ('04', 'danceability', '첨부한 Spotify.csv의 danceability에 대해 건수, 평균, 중앙값, 최솟값, 최댓값, 사분위수와 결측치를 알려줘.'),
    ('05', '장르별 비교', '첨부한 Spotify.csv에서 track_genre별 danceability의 평균과 중앙값을 비교해줘. 장르별 곡 수도 함께 보여줘.'),
    ('06', '상위 10개', '첨부한 Spotify.csv에서 평균 danceability가 높은 장르 10개를 정리해줘. 여기서 “춤추기 좋다”는 이 지표가 높다는 의미로만 해석해줘.'),
    ('07', '결측치', '첨부한 Spotify.csv에서 결측치가 있는 컬럼과 각각의 개수·비율을 알려줘.'),
    ('08', '이상치 후보', '첨부한 Spotify.csv에서 이상치 후보가 있는 수치형 컬럼을 찾아줘. 사용한 기준과 후보 수를 함께 적고 자동으로 삭제하지 마.'),
    ('09', '타입 점검', '첨부한 Spotify.csv에서 데이터 타입을 수정하거나 식별자로 다뤄야 할 컬럼을 알려줘. 변경 이유도 설명해줘.'),
]
add('content', '03 · Spotify 실습', '구조와 요약 통계 프롬프트', '각 질문을 복사해 실행하고, 나온 숫자의 기준을 확인합니다.', prompt_cards(spotify_prompts[:5]),
    '처음 다섯 질문은 컬럼 의미와 요약 통계의 기준을 세운다. 수강생은 AI가 실제 CSV를 읽었는지 행 수와 컬럼 수부터 대조한다.')
add('content', '03 · Spotify 실습', '비교와 품질 점검 프롬프트', '순위에는 계산 기준과 데이터 품질 확인이 함께 있어야 합니다.', prompt_cards(spotify_prompts[5:]),
    '장르 순위는 danceability 평균이라는 제한된 기준이다. 결측치와 타입 확인 결과를 나중 단계에 기록한다.')

add('chapter', '04 · 데이터 전처리', '데이터 전처리', '삭제나 대체보다 먼저, 왜 그 처리가 필요한지 설명합니다.')

add('content', '04 · 데이터 전처리', '정리할 대상과 결정 기준', '형식 오류·결측치·이상치 후보를 구분합니다.',
    cards([('형식', '표현 통일', '날짜·단위·문자 표기·범주 이름을 같은 기준으로 맞춥니다.'), ('결측', '빈 값의 이유', '누락·응답 없음·해당 없음 중 무엇인지 확인합니다.'), ('이상치', '극단값의 의미', '입력 오류인지 실제 드문 사례인지 확인합니다.')]) + '<div class="callout">전처리 기록: 무엇을 바꿨는가 → 왜 바꿨는가 → 몇 행이 영향을 받았는가</div>',
    '평균 대체나 삭제는 기본 동작이 아니다. 분석 목적과 결측 원인에 맞게 선택하며, 전후의 행 수와 분포를 비교한다.')

add('content', '04 · housing 실습', 'housing.csv의 품질을 점검합니다', '결측치 후보를 찾고 이상치의 처리 여부를 판단합니다.',
    '<div class="metric-row"><div class="metric reveal"><strong>20,640</strong><span>행</span></div><div class="metric reveal"><strong>10</strong><span>열</span></div><div class="metric reveal"><strong>207</strong><span>total_bedrooms 결측 행</span></div></div><div class="callout">207행은 전체의 약 1.00%입니다. 비율이 작아도 어떤 행에서 비어 있는지 확인해야 합니다.</div>',
    '실제 housing.csv에서 total_bedrooms만 207개 빈 값을 확인했다. 전처리를 할 때는 이 컬럼의 쓰임과 누락 패턴을 먼저 본다.',
    '자료: lecture/실습/housing.csv · examples.py')

housing_prompts = [
    ('01', '결측치 개수', '첨부한 housing.csv에서 결측치가 있는 컬럼과 각각의 개수·비율을 알려줘.'),
    ('02', '결측치 처리', '첨부한 housing.csv의 결측치를 어떻게 처리하면 좋을지 목적별 대안을 제시해줘. 각 대안의 행 수와 정보 손실을 비교해줘.'),
    ('03', '이상치 후보', '첨부한 housing.csv에서 이상치 후보가 있을 만한 수치형 컬럼을 찾아줘. 값의 범위와 가능한 이유를 설명해줘.'),
    ('04', 'IQR 기준', '첨부한 housing.csv의 수치형 컬럼에 IQR 기준을 적용해 이상치 후보 수와 비율을 알려줘. 후보를 자동으로 삭제하지 마.'),
    ('05', 'Z-Score 기준', '첨부한 housing.csv에서 Z-Score 절댓값이 3보다 큰 관측값을 컬럼별로 찾아줘. 평균과 표준편차에 극단값이 미치는 영향도 설명해줘.'),
    ('06', '상자그림', '첨부한 housing.csv의 주요 수치형 컬럼을 상자그림으로 보여줘. 컬럼별 단위 차이가 커서 읽기 어려우면 그래프를 분리해줘.'),
    ('07', '처리 결정', '첨부한 housing.csv에서 발견한 이상치 후보를 어떤 경우에 유지·수정·제외할지 기준을 제시해줘. 각 선택의 분석상 영향을 설명해줘.'),
]
add('content', '04 · housing 실습', '결측치와 IQR 프롬프트', '전처리의 출발점은 빈 값과 극단값의 규모 파악입니다.', prompt_cards(housing_prompts[:4]),
    '원고의 housing 프롬프트 번호가 2부터 시작해 1부터 다시 정리했다. 질문의 핵심 내용은 유지했다.')
add('content', '04 · housing 실습', 'Z-Score와 처리 판단 프롬프트', '서로 다른 탐지 기준을 비교한 뒤 처리 이유를 남깁니다.', prompt_cards(housing_prompts[4:]),
    'IQR과 Z-Score는 서로 다른 가정이 있다. 차이가 나면 어느 쪽이 정답인지보다 데이터 분포와 분석 목적을 확인한다.')

add('chapter', '05 · 데이터 시각화', '데이터 시각화', '그래프의 모양보다 먼저, 답할 질문을 정합니다.')

add('content', '05 · 데이터 시각화', '질문이 그래프를 결정합니다', '비교·분포·관계·시간 변화는 읽는 방법이 다릅니다.',
    cards([('비교', '막대그래프', '범주 사이 값의 크기와 순위를 보여줍니다.'), ('분포', '히스토그램·상자그림', '값이 몰린 곳과 극단값 후보를 봅니다.'), ('관계', '산점도', '두 수치가 함께 움직이는지 살펴봅니다.'), ('시간', '꺾은선 그래프', '날짜·월·연도에 따른 변화를 봅니다.')], 4) + '<div class="callout">연령대별 한 시점의 값은 시간 추세가 아니라 연령 분포입니다.</div>',
    '원고의 빠진 스크린샷을 차트 선택 도식으로 대체했다. 파이차트는 범주가 많을 때 비교하기 어려워 막대그래프를 우선한다.')

add('content', '05 · population 실습', '지역별 인구를 비교합니다', '전국 합계 행을 제외한 지역 단위 비교입니다.',
    '<div class="population-layout"><div class="bar-chart"><div><span>경기도</span><i style="width:100%"></i><b>1,371만</b></div><div><span>서울특별시</span><i style="width:68%"></i><b>933만</b></div><div><span>부산광역시</span><i style="width:24%"></i><b>325만</b></div><div><span>경상남도</span><i style="width:23%"></i><b>322만</b></div><div><span>인천광역시</span><i style="width:22%"></i><b>304만</b></div></div><div class="population-note"><strong>17개 시도</strong><p>‘전국’ 행은 합계이므로 지역 순위에 포함하지 않습니다.</p><small>인구 값은 제공된 CSV의 수치입니다. 기준일은 파일에 표시돼 있지 않아 별도 확인이 필요합니다.</small></div></div>',
    'population.csv는 cp949 인코딩이다. 숫자 값 끝 공백을 제거한다. 전국 행을 지역 비교에 다시 더하지 않도록 한다. 65세 이상은 10세 구간으로 정확히 구할 수 없음을 설명한다.',
    '자료: lecture/실습/population.csv · examples.py')

population_prompts = [
    ('01', '전체 인구', '첨부한 population.csv의 시도별 전체 인구수를 막대그래프로 보여줘. 전국 행은 별도로 표시해줘.'),
    ('02', '지역 순위', '첨부한 population.csv에서 전국 행을 제외하고 시도별 전체 인구수를 가로 막대그래프로 보여줘. y축은 시도명, x축은 인구 수(백만 명)이며 큰 순서로 정렬해줘.'),
    ('03', '전국 연령 분포', '첨부한 population.csv의 전국 행에서 전체_0~9세부터 전체_100세 이상까지 연령대별 인구를 순서대로 시각화해줘. 한 시점의 연령 분포라고 설명해줘.'),
    ('04', '서울 연령 구성', '첨부한 population.csv에서 서울특별시의 연령대별 인구 구성비를 보여줘. 전체_총인구수 열은 제외하고 범주가 많으므로 가로 막대그래프로 그려줘.'),
    ('05', '남녀 연령 분포', '첨부한 population.csv에서 남성과 여성의 연령대별 인구 분포를 비교해줘. 총인구수와 연령구간인구수 열은 제외하고 같은 연령 구간끼리 비교해줘.'),
    ('06', '20대 상위 지역', '첨부한 population.csv에서 전체_20~29세 인구가 많은 시도 상위 5개를 막대그래프로 그려줘. 전국 행은 제외해줘.'),
    ('07', '지역별 성비', '첨부한 population.csv에서 시도별 남녀 인구 비율을 100% 누적 막대그래프로 비교해줘. 전국 행은 제외해줘.'),
    ('08', '고령 인구 비중', '첨부한 population.csv에서 70세 이상 인구 비중을 시도별로 계산해 보여줘. 이 파일은 10세 구간이므로 65세 이상 비중은 정확히 계산할 수 없다고 명시해줘.'),
]
add('content', '05 · population 실습', '지역과 연령 분포 프롬프트', '전국 합계와 지역 값을 섞지 않는지 확인합니다.', prompt_cards(population_prompts[:4]),
    '원고의 파이차트 요청은 연령 구간이 많아 가로 막대로 바꿨다. 각 프롬프트는 첨부 파일명과 제외할 열을 명시해 단독으로 복사해도 실행 가능하다.')
add('content', '05 · population 실습', '성비와 고령 비중 프롬프트', '분모와 연령 구간을 명시해야 비율을 해석할 수 있습니다.', prompt_cards(population_prompts[4:]),
    '원고의 65세 이상 요청은 현 파일로 정확히 계산할 수 없어 70세 이상으로 바꿨다. 남녀 성비는 지역별 절대 규모보다 비율을 비교하는 100% 누적 막대가 적절하다.')

add('chapter', '06 · 인사이트 도출', '데이터 분석 및 인사이트', '관찰된 수치와 그 의미, 다음 행동을 구분합니다.')

add('content', '06 · 인사이트 도출', '관찰에서 인사이트로', '한 문장의 해석에는 근거와 한계가 함께 있어야 합니다.',
    '<div class="insight-flow"><article class="reveal"><span>관찰</span><h2>토요일 지출이 가장 많다</h2><p>표에서 직접 확인한 사실</p></article><article class="reveal"><span>해석</span><h2>주말 여가 소비와 관련될 수 있다</h2><p>가능한 설명. 다른 이유도 검토</p></article><article class="reveal"><span>확인</span><h2>요일별 이용자 수와 행사·계절을 대조</h2><p>주장을 검증할 추가 데이터</p></article></div>',
    '원고의 토요일 지출 예시를 사용한다. 인과관계처럼 단정하지 않고 관찰, 가능한 해석, 확인할 증거로 나눈다.')

add('content', '06 · 인사이트 도출', '세 가지 분석 관점', '비교·분포·비율은 서로 다른 질문에 답합니다.',
    cards([('01', '비교', '서울과 부산의 20~29세 인구는 얼마나 다른가?'), ('02', '분포', '연령대별 인구는 어느 구간에 몰려 있는가?'), ('03', '비율', '70세 이상은 각 지역 인구의 몇 %인가?')]) + '<div class="callout">“왜 그런가?”는 이 표만으로 확정하지 않고 가설과 추가 자료로 다룹니다.</div>',
    '원고의 추세 예시 중 연령대별 비교는 여러 시점의 변화가 아니므로 분포라고 고쳤다. 실제 시간 변화 데이터라면 추세라는 관점을 별도로 적용할 수 있다.')

insight_compare = [
    ('01', '두 지역 비교', '첨부한 population.csv에서 서울특별시와 부산광역시의 20~29세 인구수를 비교해줘. 두 값, 차이, 비교 기준을 먼저 보여줘.'),
    ('02', '상위 지역 차이', '첨부한 population.csv에서 전국 행을 제외하고 전체 인구가 가장 많은 시도와 두 번째 시도의 인구 차이를 알려줘.'),
    ('03', '가능한 설명', '첨부한 population.csv에서 경기도의 30~39세 인구수를 다른 시도와 비교해줘. 차이가 나는 이유는 이 파일만으로 단정하지 말고 가설과 추가로 필요한 데이터를 구분해줘.'),
    ('04', '지역별 60대', '첨부한 population.csv에서 지역별 60~69세 인구수를 비교해줘. 절대 수와 지역 전체 대비 비중을 구분해줘.'),
]
insight_distribution = [
    ('01', '연령별 모양', '첨부한 population.csv의 전국 행에서 연령대별 인구 분포를 순서대로 설명해줘. 이 자료는 한 시점의 분포이며 시간에 따른 변화가 아님을 명시해줘.'),
    ('02', '60세 이상 구간', '첨부한 population.csv의 전국 행에서 60~69세부터 100세 이상까지 구간별 인구가 어떻게 다른지 설명해줘.'),
    ('03', '증감 구간', '첨부한 population.csv의 전국 행에서 이웃한 연령 구간 사이 인구 수가 커지거나 작아지는 구간을 정리해줘.'),
    ('04', '인구 피라미드', '첨부한 population.csv에서 남녀 연령 구간을 사용해 인구 피라미드를 그려줘. 한 시점의 연령 구조만 해석하고 원인을 단정하지 마.'),
]
insight_ratio = [
    ('01', '40대 비중', '첨부한 population.csv의 전국 행에서 40~49세 인구가 전체 인구에서 차지하는 비중을 계산해줘. 분자와 분모를 표시해줘.'),
    ('02', '50대 비중 해석', '첨부한 population.csv의 전국 행에서 50~59세 비중을 계산해줘. 비중의 원인은 이 파일만으로 확정하지 말고 필요한 추가 자료를 알려줘.'),
    ('03', '60세 이상 비중', '첨부한 population.csv의 전국 행에서 60세 이상 인구 비중을 계산해줘. 60~69세부터 100세 이상까지의 열을 합산하고 기준을 밝혀줘.'),
    ('04', '상위 연령대', '첨부한 population.csv의 전국 행에서 연령대별 인구 비중이 높은 상위 3개 구간을 알려줘. 전체_총인구수 열은 연령 구간에서 제외해줘.'),
]
add('content', '06 · 인사이트 실습', '비교 프롬프트', '같은 지표를 같은 기준으로 비교합니다.', prompt_cards(insight_compare),
    '원고의 비교 질문을 유지하면서 수치와 추정 원인을 구분하도록 했다.')
add('content', '06 · 인사이트 실습', '연령 분포 프롬프트', '연령대 차이는 한 시점의 구조로 설명합니다.', prompt_cards(insight_distribution),
    '원고의 추세 예시는 시간 데이터가 아니므로 연령 분포라는 표현으로 고쳤다.')
add('content', '06 · 인사이트 실습', '비율 프롬프트', '비율마다 분자와 분모를 함께 적습니다.', prompt_cards(insight_ratio),
    '50대 비율이 높은 이유는 인구 표 하나로 단정할 수 없다. 원고의 의도를 유지하되 가설과 추가 근거를 구분한다.')

add('chapter', '07 · 텍스트 마이닝', '텍스트 마이닝', '짧은 영어 문장에서 감정과 자주 등장하는 표현을 살핍니다.')

add('content', '07 · 텍스트 마이닝', '이번 실습의 분석 범위', '감성분석.csv의 text 열 3,534개로 한 가지 흐름을 연습합니다.',
    flow([('원문 확인', '언어·길이·URL·중복'), ('문장 감성', 'VADER compound 점수'), ('라벨 저장', 'positive·negative·neutral'), ('표현 추출', '정제한 텍스트에서 빈도'), ('해석·검증', '분포와 오분류 확인')]) + '<div class="callout">토픽 모델링·NER·딥러닝 모델 비교는 이번 기초 실습의 범위에서 제외합니다.</div>',
    '사용자 원고에서 중복된 분석 절차와 기법 목록을 정리했다. 이 데이터는 영어의 짧은 SNS 문장이고 정답 라벨이 없으므로 가벼운 사전·규칙 기반 VADER 실습이 적절하다. 한국어 감성사전이나 한국어 사전학습 모델 비교는 이번 파일과 맞지 않는다.',
    '자료: lecture/실습/감성분석.csv · VADER 공식 프로젝트')

add('content', '07 · 텍스트 마이닝', 'VADER는 원문 전체를 평가합니다', '분류할 문장과 단어 빈도를 셀 텍스트는 역할이 다릅니다.',
    '<div class="vader-layout"><article class="vader-input reveal"><span>원문 text</span><p>at starbucks with my love. eff school. i have work later too.</p><strong>compound 0.6369 → positive</strong></article><article class="vader-output reveal"><span>별도로 만든 cleaned_text</span><p>의미 없는 URL·기능어를 줄여 단어와 표현을 집계합니다.</p><strong>문장 라벨을 단어마다 붙이지 않습니다</strong></article></div><div class="callout">positive ≥ 0.05 · negative ≤ −0.05 · 그 사이는 neutral</div>',
    '첨부 원고의 예시 문장을 공식 vaderSentiment 패키지로 직접 계산해 compound 0.6369를 확인했다. VADER가 문장 전체를 분류한 결과를 단어 각각의 감정으로 해석하면 안 된다. cleaned_text는 현재 CSV에 없으므로 실습에서 만든다.',
    '방법: cjhutto/vaderSentiment · 원문 예시 점수 검산')

add('content', '07 · 텍스트 마이닝', '감정 분포를 읽는 방법', '분류 결과는 모델의 판단이며 표본 확인으로 해석을 보강합니다.',
    '<div class="sentiment-chart"><div><span>positive</span><i style="width:48.61%"></i><b>1,718 · 48.61%</b></div><div><span>neutral</span><i style="width:25.86%"></i><b>914 · 25.86%</b></div><div><span>negative</span><i style="width:25.52%"></i><b>902 · 25.52%</b></div></div><div class="callout">각 그룹의 문장을 직접 읽고 반어·문맥·다중 감정으로 생긴 오분류를 기록합니다.</div>',
    '제공된 3,534문장을 VADER compound 기준으로 분류한 결과다. 비율 합계는 반올림으로 99.99%가 될 수 있다. 분포만으로 문장 속 감정의 진실을 단정하지 않는다.',
    '자료: lecture/실습/감성분석.csv · examples.py')

sentiment_prompts = [
    ('01', '감성 분류', '첨부한 감성분석.csv의 text 열은 짧은 영어 문장입니다. VADER로 원문 전체의 compound 점수를 계산하고, 0.05 이상은 positive, -0.05 이하는 negative, 그 사이는 neutral로 분류해 predicted_sentiment 열에 저장해줘. 빈 문장과 오류 처리 기준도 설명해줘.'),
    ('02', '분포 요약', '첨부한 감성분석.csv에 생성한 predicted_sentiment 열을 기준으로 positive, negative, neutral의 건수와 전체 대비 비율을 소수점 둘째 자리까지 표로 보여줘. 사용한 분모와 라벨 기준을 적어줘.'),
    ('03', '표현 추출', '첨부한 감성분석.csv에 predicted_sentiment 열을 만든 뒤, 별도 cleaned_text 열을 만들어 URL과 일반 기능어를 정리해줘. positive와 negative 그룹에서 상대적으로 두드러지는 단어·두 단어 표현을 각각 상위 10개 보여줘. 단어가 그 자체로 긍정·부정이라는 뜻은 아님을 명시해줘.'),
    ('04', '시각화와 검증', '첨부한 감성분석.csv의 predicted_sentiment 분포를 막대그래프로 보여줘. positive와 negative 그룹의 주요 표현은 가로 막대그래프로 비교해줘. 각 그룹에서 문장 표본을 몇 개 직접 확인해 오분류 사례와 해석 한계를 3~4줄로 요약해줘.'),
]
add('content', '07 · 텍스트 마이닝 실습', '감성 분석 프롬프트', '문장 분류 → 비율 → 표현 → 검증을 순서대로 실행합니다.', prompt_cards(sentiment_prompts),
    '원고의 세 묶음 프롬프트를 하나의 실습 흐름으로 정리했다. cleaned_text가 원본에 없다는 점을 분명히 하고 워드클라우드는 필수에서 제외했다. 가장 읽기 쉬운 막대그래프를 사용한다.')

add('chapter', '08 · 프로젝트 실습', '프로젝트 실습', '자신의 질문과 데이터로 오늘 배운 단계를 다시 실행합니다.')

add('content', '08 · 프로젝트 실습', '세 가지 데이터 출발점', '준비된 데이터에서 시작하거나 필요한 데이터를 직접 수집합니다.',
    cards([('통신사', '고객 이탈', '회선·이용·청구·상담 기록에서 하나의 질문을 선택합니다.'), ('뷰티', '2026 트렌드', '공공·소셜 자료에서 소비와 관심의 변화를 질문합니다.'), ('공공데이터', '자유 주제', '공식 출처에서 분석 질문에 맞는 데이터셋을 선택합니다.')]) + '<div class="callout">공유한 데이터 사용 또는 데이터 수집부터 시작 중 하나를 선택합니다.</div>',
    '현재 제공된 공공데이터 프로젝트 파일은 없으므로 수강생은 공식 출처에서 주제에 맞는 자료를 직접 고른다. 통신사는 테이블이 많으므로 입문자는 주제와 필요한 파일부터 좁힌다.')

add('content', '08 · 프로젝트 실습', '1일차 결과물 작성 틀', '분석 과정이 다른 사람에게도 재현되도록 기준을 남깁니다.',
    '<div class="worksheet">' + ''.join(f'<div class="reveal"><b>{i:02d}</b><strong>{a}</strong><span>{b}</span></div>' for i,(a,b) in enumerate([
        ('문제 정의','누구의 어떤 결정을 돕는가'),('데이터','출처·기간·분석 단위·주요 열'),('품질·전처리','결측·이상치와 처리 이유'),('EDA·시각화','질문에 답하는 표·그래프'),('인사이트','관찰·해석·한계·다음 확인')],1)) + '</div>',
    '최소한 문제 정의와 근거 있는 인사이트는 반드시 남긴다. 구체적인 제출물에는 데이터의 출처와 전처리 결정을 함께 포함하도록 보강했다.')

add('chapter', '09 · 2일차 시각화 및 AX', '시각화 및 AX', '분석 결과를 공유 가능한 HTML로 만들고 Agent 작업을 검토합니다.')

add('content', '09 · HTML 시각화', '최종 HTML의 읽는 순서', '결과를 처음 보는 사람이 질문부터 제안까지 따라갈 수 있어야 합니다.',
    flow([('질문', '무엇을 해결하나'), ('데이터', '무엇을 관찰했나'), ('핵심 그래프', '어떤 차이가 있나'), ('해석', '왜 중요하나'), ('제안', '무엇을 확인하며 실행하나')]) + '<div class="callout">그래프마다 제목·축·단위·분모·출처를 함께 둡니다.</div>',
    '통신사 시연 결과와 연결해 보여준다. 시각화는 장식이 아니라 질문에 답하는 근거다. 1일차 결과물을 재배치해 최종 보고서를 만든다.')

add('content', '09 · Agent 환경 구성', 'Agent에게 맡길 일과 확인할 일', '도구가 코드를 만들더라도 분석 기준과 결과 검토는 사람이 결정합니다.',
    '<div class="comparison"><article class="comparison-card reveal"><span>Agent 작업</span><h2>생성·반복</h2><p>데이터 읽기 코드 · 그래프 초안 · HTML 배치 · 오류 수정</p></article><article class="comparison-card reveal"><span>사람의 판단</span><h2>기준·검증</h2><p>분석 질문 · 제외 기준 · 수치 대조 · 과장된 해석 수정</p></article></div><div class="callout">작업 폴더와 접근 가능한 파일을 확인하고, 작은 단위로 요청한 뒤 결과를 실행해 봅니다.</div>',
    'AX는 특정 도구 이름보다 작업 흐름으로 설명한다. 수강생이 사용할 Agent 제품과 설치 방법이 확정되면 환경 설정 세부를 이 슬라이드 다음에 추가할 수 있다.')

add('content', '09 · 최종 산출물', '2일차 제출 전 확인', '보기 좋은 화면과 재현 가능한 분석은 함께 필요합니다.',
    cards([('01', '근거', '그래프의 값과 본문의 수치가 일치하는가?'), ('02', '읽기', '처음 보는 사람이 질문과 결론을 이해하는가?'), ('03', '재현', '데이터·코드·처리 기준을 다시 찾을 수 있는가?'), ('04', '한계', '모르는 것과 추가 검증할 것을 밝혔는가?')], 4),
    '최종 HTML에는 시각화뿐 아니라 근거와 분석 한계를 포함한다. 학생 간 발표에서도 이 네 항목으로 피드백한다.')

add('chapter', '10 · 환경 설정', '실습 자료 받기', 'GitHub에서 파일을 내려받고 강의 중 변경 사항을 갱신합니다.')

add('content', '10 · GitHub 설정', '처음 받기와 다음에 갱신하기', '복제는 한 번, 갱신은 이미 복제한 폴더에서 실행합니다.',
    '<div class="git-steps"><article class="reveal"><span>처음 한 번</span><pre>git clone https://github.com/develup-psy/data-analysis.git\ncd data-analysis</pre></article><article class="reveal"><span>자료가 갱신된 뒤</span><pre>git pull origin main</pre></article></div><div class="callout">처음에는 Git 설치를 확인합니다. GitHub에 강의 자료가 올라온 뒤 위 명령을 실행하세요.</div>',
    '원고의 mkdir 후 clone . 방식도 빈 폴더라면 가능하지만 초심자에게는 clone 후 cd가 더 단순하다. git pull은 첫 복제와 다르고 해당 저장소 폴더 안에서 실행한다. 공개 저장소의 첫 업로드 후 수강생 안내에 사용한다.',
    '저장소: github.com/develup-psy/data-analysis')

add('closing', 'CLOSING', '질문을 정하고, 근거를 남기세요', '데이터를 읽는 기준과 해석의 근거가 최종 결과물의 품질을 결정합니다.',
    '<div class="closing-line">문제 정의 <span>→</span> 분석 <span>→</span> 검증 <span>→</span> 공유</div><p class="closing-question">질문과 대화</p>',
    '마무리. 1일차에는 분석 질문과 근거가 있는 인사이트를 남기고, 2일차에는 그것을 읽기 쉬운 HTML로 정리한다. 수강생의 질문을 받는다.')
