# 프로젝트 밥피엔스
# GIT_COMMIT_CONVENTION

## 설정
```
로컬에 설정
cd bobpience_config
ln -sf local.py settings.py
Product 설정
cd bobpience_config
ln -sf prod.py settings.py
```
or
```
로컬에 설정
cd bobpience_config
mklink settings.py local.py
Product 설정
cd bobpience_config
mklink settings.py prod.py
```

<aside>
💡 ***확정된 내용 아니고 수정해도되니 언제든 태클 요망***

</aside>

## 커밋 메시지 & 브랜치 컨벤션

<aside>
✅

### 1. 커밋 유형 지정

- 커밋 유형은 영어 대문자로 작성하기
- 새로 생성하는 브랜치명도 종류에 따라 아래와 같은 키워드를 사용한다. 예)    Feat/"브랜치명"
    
    | 커밋 유형 | 의미 | 깃모지 검색 |
    | --- | --- | --- |
    | Feat | 새로운 기능 추가 | ✨ :sparkles: |
    | Fix | 버그를 고친 경우 | 🐛 :bug: |
    | Docs | 문서 수정 | 📝 :memo: |
    | Refactor | 코드 리팩토링 | ♻️ :recycle: |
    | Chore | 패키지 매니저 수정, 그 외 기타 수정 ex) .gitignore | 📦 :package: |
    | Design | CSS 등 사용자 UI 디자인 변경 | 🎨 :art: |
    | Change | 파일명 변경, 파일 삭제 등 기타 | 🔧 :wrench: |
    | Test | 테스트 코드, 리팩토링 테스트 코드 추가 | 🤡 :clown_face: |
    |  |  |  |
    


### 2. 제목과 본문을 빈행으로 분리

- 커밋 유형 이후 제목과 본문은 한글로 작성하여 내용이 잘 전달될 수 있도록 할 것
- 본문에는 변경한 내용과 이유 설명 (어떻게보다는 무엇 & 왜를 설명)

### 3. 제목 첫 글자는 대문자로, 끝에는 `.` 금지

### 4. 제목은 영문 기준 50자 이내로 할 것

### 5. 자신의 코드가 직관적으로 바로 파악할 수 있다고 생각하지 말자

### 6. 여러가지 항목이 있다면 글머리 기호를 통해 가독성 높이기

```
- 변경 내용 1
- 변경 내용 2
- 변경 내용 3
```

</aside>

### 규칙에 맞는 좋은 커밋메시지를 작성해야 하는 이유

- 팀원과의 소통
- 편리하게 과거 추적 가능
- 나중에 실무에서 익숙해지기 위해



### 한 커밋에는 한 가지 문제만!

- 추적 가능하게 유지해주기
- 너무 많은 문제를 한 커밋에 담으면 추적하기 어렵다.

### CLI에서 커밋 메시지 여러 줄로 작성하는 방법

<aside>
✅ **쌍따옴표를 닫지 말고 개행하며 작성 → 다 작성한 후에 쌍따옴표를 닫으면 작성 완료**

```bash
git commit -m "FEAT: 회원가입 기능 추가

- 회원가입 기능 추가"
```
</aside>
