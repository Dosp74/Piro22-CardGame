# 숫자 카드 게임

## 📌 프로젝트 개요
유저 간에 숫자 카드 대결을 진행하는 게임

게임을 통해 점수를 획득하거나 잃으며, 누적 점수에 따라 랭킹이 매겨짐

## 🎮 게임 흐름

1. **회원가입**

![Image](https://github.com/user-attachments/assets/14fbe5b8-a817-4764-9008-b92e84547cad)

   - Django 기본 로그인을 위한 회원가입이 가능함
2. **로그인**

![Image](https://github.com/user-attachments/assets/88830167-e44e-42de-a34f-a6630523ad45)

   - Django 기본 로그인 또는 소셜 로그인(카카오) 중 선택
3. **공격하기** (유저 `n`이 유저 `m`을 선택하여 공격)

   - 1~10 사이의 숫자 중 랜덤으로 5개가 제공됨
   - 그중 하나를 선택하여 상대 유저 `m`에게 게임을 걸 수 있음
4. **게임 요청 확인** (유저 `m`이 로그인 후 확인)

   - `m`이 로그인하여 게임 리스트에서 `n`이 보낸 도전을 확인
   - `m` 또한 숫자 카드를 선택하여 반격할 수 있음
5. **대결 결과 확인**

   - 랜덤하게 결정된 승리 조건에 따라 자신의 카드 숫자만큼 점수 획득/차감
   - 숫자가 같으면 무승부 (점수 변동 없음)
6. **게임 전적 관리**

   - 진행 중인 게임은 취소 가능 (`n`이 상대의 반격 전 취소 가능)
   - 종료된 게임은 결과 확인 가능
7. **랭킹 시스템**

   - 모든 게임에서 획득/차감된 점수를 합산하여 랭킹으로 표시

---

## 📝 기능 상세

### 🏠 1. 메인 페이지
- **로그인 전**: 일반 로그인 또는 소셜 로그인 선택 가능

![Image](https://github.com/user-attachments/assets/e86ce581-08e9-4bea-a0ea-f15675d23573)
- **로그인 후**: 유저의 게임 진행 현황 및 시작 버튼 제공

![Image](https://github.com/user-attachments/assets/080210b1-4a34-42ae-b60c-67d4d6489760)

### 🎯 2. 공격하기 페이지 (start 버튼 클릭)
- 랜덤 숫자 카드 5개 제공, 그중 하나 선택

![Image](https://github.com/user-attachments/assets/98c973ae-c34f-4fa4-a284-6e88b633804b)
- 공격할 상대 유저 선택 가능

![Image](https://github.com/user-attachments/assets/cb123c89-56b7-4a5c-a974-93bae135839b)

### 📜 3. 게임 전적 페이지 (게임 리스트)
- 진행 중인 게임: 상대가 반격하지 않았다면 취소 가능
- 반격 가능 게임: 상대가 도전한 게임을 확인 후 반격 가능
- 종료된 게임: 결과 확인 가능

![Image](https://github.com/user-attachments/assets/38ef78ac-256b-4a77-8363-bed01fdce7e2)

### 🔎 4. 게임 정보 페이지 (게임 상세 정보)
- 진행 중인 게임

![Image](https://github.com/user-attachments/assets/711c903b-0392-410c-8c42-93f78d3ce9e2)
- 반격 대기 중인 게임

![Image](https://github.com/user-attachments/assets/c2a05cc7-8cd5-4cb0-8ddb-b00097a6060e)
- 완료된 게임의 결과

![Image](https://github.com/user-attachments/assets/c92e4043-a496-43d7-980f-205ce92104fa)

### ⚔️ 5. 반격하기 페이지

![Image](https://github.com/user-attachments/assets/67f976d9-926b-4a78-9858-b6b29a37b4f7)
- 반격 완료 후 즉시 결과 확인 가능

![Image](https://github.com/user-attachments/assets/b3a14cd8-4f35-4197-b32a-43114b1e842c)
- 반격 버튼이 사라지고 게임 결과가 표시되는 것을 확인할 수 있음

![Image](https://github.com/user-attachments/assets/45812193-3401-422a-a4a7-bacdaf4ff368)

### 🏆 6. 랭킹 보기 페이지
- 모든 유저의 누적 점수를 기준으로 랭킹화

![Image](https://github.com/user-attachments/assets/02dcabcb-7017-425f-89bc-d9a83cbe2ae3)

---

## 🛠 기술 스택
- **Frontend**: HTML, CSS
- **Backend**: Python, Django
- **Database**: SQLite3
- **Authentication**: Django Allauth (소셜 로그인 포함)

## 🚀 추가 기능 및 확장 가능성
- **게임 룰 커스터마이징** (예: 특정 숫자 범위, 카드 개수 변경 등)
- **아이템 시스템** (점수를 사용하여 특수 아이템 구매 및 사용)
- **친구 시스템** (지인과 게임 신청 및 대결 가능)

## 📢 프로젝트 정보
- **피로그래밍 22기 4주차 팀 과제**

### 역할
- 장재훈: 카카오 로그인 기능, 랭킹 페이지 구현
- 김재원, 한종서: main(list) 페이지, 대결 기능, 반격 기능 구현, 게임 결과 렌더링
- 이주원: CSS
- 조주영: 로그인, 회원가입, 인트로 페이지 구현, background_img 디자인

### 협업 툴
- 디스코드
- 노션: https://www.notion.so/17dac03cf605801f80dceab36ba287cb
- 피그마: https://www.figma.com/board/DUlnWj2UA2OtRGSBQ8jARc?fuid=1450356499984093506&prev-plan-id=1450356501760392765&prev-plan-type=team&prev-selected-view=recentsAndSharing
