## 시소(SeniorSociety) 소개

**<div align=center> 시니어를 위한 인천 지역 기반 커뮤니티</div>**
<div align=center>
인천 지역 내 액티브 시니어를 대상으로,<br>
다양한 주제의 갤러리에서 소통할 수 있는 커뮤니티를 구현했습니다.<br><br>
커머스, 이벤트의 기능을 추가하여 기본적인 게시판 커뮤니티를 넘어 <br>
지역 Hub 커뮤니티로 거듭나는 것이 시소의 목표입니다.
<br><br>
개발은 초기 세팅부터 전부 직접 구현했으며, <br>
아래 데모 영상에서 보이는 부분은 실제 사용할 수 있는 서비스로 개발한 것입니다.<br></div>
<br>

## 개발 인원 및 기간

- 개발기간 : 2021/8/30 ~ 2021/9/30
- 개발 인원 : 프론트엔드 4명, 백엔드 3명
<br>


## Modeling✏️
URL : https://aquerytool.com/aquerymain/index/?rurl=994af4d3-5b54-4022-ab39-2e2b36eac916& <br>
Password : 8md41d

## 구현 페이지

### 메인

### 게시물 리스트

### 게시물

## 구현 기능

### 메인
- 전체 갤러리 리스트 표시
- 인기 갤러리 및 인기 게시물 표시

### 게시물 리스트
- 최신순, 인기순으로 게시물 정렬
- 댓글 등록/수정/삭제
- 유저 네임카드 조회

### 게시글 작성
- 게시글 등록과 함께 이미지는 AWS S3에 저장, DB에는 해당 이미지 오브젝트 URL 저장

### 회원가입 & 로그인
- 카카오, 네이버 소셜 로그인 API를 통한 유효성 검사
- JWT 토큰 발행 후, 사이트 내 로그인 수행 또는 회원가입 페이지
- 로그인 데코레이터
- 회원 정보 수정 / 탈퇴

<br>

## **사용 기술👍**
Frontend : <br>
Backend  : Python, Django, MySql, Postman, AWS, Docker


### Reference
이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
