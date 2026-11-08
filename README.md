# 0202 Works

Jjang의 비공개 작업 대시보드 → https://onleeyoo.github.io/0202-works/
데이터는 비밀번호로 암호화되어 `index.html` 안에만 들어 있다. 평문(`_src/items.json`)은 절대 커밋하지 않는다.

## 업데이트 방법 (Claude용)

```
git clone https://github.com/onleeyoo/0202-works && cd 0202-works
python3 _src/works.py decrypt <비밀번호>      # -> _src/items.json (gitignore)
# _src/items.json 수정
python3 _src/works.py build <비밀번호>        # -> index.html
git add index.html && git commit -m "update dashboard" && git push
```

## 항목 규칙

- `area`(카테고리): `프리미어 플러그인` | `0202PD 웹·서비스`(화면엔 "0202PD", 인스타 콘텐츠·계정 운영 포함) | `블로그`
- 페이지는 카테고리 → 주제 → 상태(진행중/대기/아이디어/완료) → 항목 번호 트리로 보여준다
- `topic`(주제): 카테고리 안의 주제. **채팅별이 아니라 주제별로** 묶는다. 여러 채팅에서 같은 주제를 다뤘으면 같은 topic.
  - 플러그인 예: 0202Transition, 0202Swatch, 0202VideoHelper, Korean Typewriter, 새 플러그인 아이디어, 배포·운영
  - 0202PD 예: 콘텐츠 기획(릴스·캐러셀·미분류), 계정 운영, 유튜브 트렌드 사이트, 영상 분석 서비스, 효과음 정리, 밈 트렌드 리포트
  - 기존 topic이 맞으면 그걸 쓰고, 새 제품·서비스일 때만 새 topic을 만든다.
- `kind`(선택): 0202PD `콘텐츠 기획` 주제 안에서 `릴스` | `캐러셀` | `미분류`(형식 미정 아이디어). kind가 있는 주제는 상태 대신 kind로 묶여 보인다.
- `title`: 주제 안의 할 일 (주제 이름은 반복하지 않음). `next`: 다음 할 일 한 줄.
- `detail`(선택): 대본·기획안 전문(줄바꿈 그대로). 페이지에서 "대본·기획 보기"로 펼쳐진다. 대본이나 기획을 써둔 항목엔 최종본을 넣는다.
- `status`: `진행중` | `대기`(결정·확인 필요) | `아이디어` | `완료`
- `updated`: 마지막으로 논의한 날짜 (YYYY-MM-DD)
- 바꾼 항목엔 `changed`(오늘 날짜) + `change`(`추가` / `상태 변경` / `내용 수정`)를 넣는다. 페이지에 이틀간 태그로 보인다.
- 항목은 지우지 않는다(끝나면 `완료`). 새 id는 기존 최대값 + 1, 두 자리 문자열.
