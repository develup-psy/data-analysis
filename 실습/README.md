# 강의 실습 데이터와 재현 코드

발표 자료의 수치 예시는 이 폴더의 CSV에서 계산했습니다. `examples.py`는 각 실습의 집계 기준을 확인하는 작은 코드입니다.

```bash
python3 -m pip install -r requirements.txt
python3 examples.py spotify
python3 examples.py housing
python3 examples.py population
python3 examples.py sentiment
```

| 파일 | 강의 용도 | 읽을 때 확인할 점 |
| --- | --- | --- |
| `Spotify.csv` | 구조 파악, 요약 통계, 장르별 비교 | `danceability`는 데이터셋의 지표이며 음악에 대한 주관적 평가와 동일하지 않습니다. |
| `housing.csv` | 결측치와 이상치 후보 검토 | `total_bedrooms`에 빈 값이 있습니다. 이상치 후보는 확인 후 처리합니다. |
| `population.csv` | 지역·연령별 시각화 | `cp949` 인코딩이며 `전국` 행은 지역 비교에서 제외합니다. 65세 이상은 이 파일의 10세 단위 구간으로 정확히 계산할 수 없습니다. |
| `감성분석.csv` | 영어 짧은 문장 감성 분석 | 원본 열은 `text` 하나입니다. `predicted_sentiment`와 `cleaned_text`는 실습에서 생성합니다. |

감성 분석 예시는 [VADER 원본 프로젝트](https://github.com/cjhutto/vaderSentiment)의 방식에 따라 원문 전체의 `compound` 점수로 문장 라벨을 만듭니다. 단어 빈도는 그 다음에 별도로 정제한 텍스트에서 계산합니다. 라벨은 모델의 판단이므로 일부 원문을 직접 읽고 분류 오류를 확인해야 합니다.
