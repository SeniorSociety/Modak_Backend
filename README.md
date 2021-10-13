# 모닥불(ModakFire) 소개

<br>

### **액티브 시니어를 위한 지역 기반 커뮤니티**

<br>

**기획서** [**[Link]**](https://docs.google.com/document/d/136YOXGBK_PrPL4G3J9W8oy0888f45thhphWWxeoCrqM/edit?usp=sharing)

- 개요, 타겟, 기능, 개선 사항 등의 기획문서입니다.
- 문서는 지속적으로 업데이트되고 있습니다.

**Workflow** [**[Link]**](https://www.figma.com/file/lhoMVBbDJclwdIhpG8uONm/%EB%AA%A8%EB%8B%A5%EB%B6%88-sketch?node-id=2%3A474)

- 사이트의 전반적인 기능을 가시화한 Workflow입니다.
- 시니어 마케팅 기획자와 위클리 미팅을 통해서 Workflow를 최적화하고 Figma로 작성했습니다.
<br>

### 타겟

- 초기 타겟은 경제력을 보유하고 새로운 인프라를 경험하는 것에 대한 거부감이 낮은 액티브 시니어

<br>

### 목표

- 네임카드를 통해 상대방의 정보를 확인하고 관심 분야의 오프라인 모임으로의 확장

<br>

### 타 커뮤니티 플랫폼과의 차별점

- 네임카드란 다른 유저에게 자신의 이력, 정보 등을 제공하는 이력 카드
- 네임카드 컨텐츠를 제공하여 다른 커뮤니티보다 깊은 유대감 형성이 가능하며 소속감을 느낄 수 있다.

<br>

### 배경

- 현대의학의 발전으로 인간의 수명이 증가하면서 2,000년대 부터 대한민국은 ‘100세 시대’라는 타이틀로 현대를 표현해왔다. 특히 베이비부머 세대가 노인 연령에 모두 도달하는 2030년에는 50대 이상의 인구가 전체 인구의 40% 도달하게 된다. 이에 따라 전세계적으로 시니어 비즈니스 시장에 대한 관심과 성장은 계속해서 가파르게 증가하고 있다.

- 과거의 노인의 특징에서 벗어난 ‘액티브 시니어’들의 등장으로 기술친화적이며 활발한 활동을 즐기는 구성원들이 증가하고 있다. 이를 통해, 현재 액티브 시니어들에게 최적화된 커뮤니티 플랫폼의 필요성을 확인했다.

<br>

## 개발 인원 및 기간

<br>

- 개발기간 : 2021/8/30 ~ 2021/9/30
- 개발 인원 : 프론트엔드 4명, 백엔드 3명
<br>

## 버전 관리

![Flowchart_(1)](https://user-images.githubusercontent.com/84912594/137124523-b5fed45f-810e-460c-9a45-86d334806047.jpeg)


Branch는 Gitflow 방식을 따라 5가지로 분류했습니다.
<br>
다만 테스트 서버를 별도로 두고 있지 않기 때문에, release 브랜치를 기준으로 서버에 배포됩니다.
<br>
CI/CD Pipeline도 Release branch와 연결해두었습니다.
<br>

## AWS Architecture Diagram

<br>
<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/AWS+Architecture+Diagram.jpg"></div>
<br>

- VPC를 Front, Back, DB로 분리하여 내부 접속을 제외하고 사용자가 Back, DB에 접근할 수 없도록 설계했습니다.
- 서버, Jenkins용 EC2는 Private Subnet 내에 만들고, 별도의 점프 호스트인 Bastion을 두어 ssh 접속 외의 외부 접속을 방지했습니다.
- Front, Back 서버 EC2를 각각 2개씩 만들어, 하나의 서버가 다운되어도 다른 서버가 유지될 수 있도록 로드밸런스로 연결했습니다.
- Cloud Watch를 통해 오류 로그를 수집하고, 특정 임계값에 도달했을 경우 AWS Chatbot을 통해 Slack에 아래와 같은 알람이 울리도록 설정했습니다.

<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/CloudWatch_Alarm.png"></div>

<br>

## Jenkins PipeLine

<br>
<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/Jenkins+Pipeline.jpg"></div>
<br>

특정 branch에 Merge되었을 때, Webhook을 기점으로 Pipeline이 시작됩니다.

<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/Jenkins+Start.png"></div><br>

이후 Stage에서 실패했을 경우, 실패 메세지와 함께 중단됩니다.

<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/Jenkins+Failed.png"></div><br>

마지막 Stage 배포까지 완료되었을 경우, 아래 슬랙 메세지가 전달됩니다.

<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/Jenkins+Finished.png"></div>

<br>

## S3 Cronjob

S3에 호스팅을 하면서 발생하는 쓸모없는 이미지들을 지워주는 작업이 추가로 필요하게 되었습니다. <br>
이를 위해 boto3와 python sqlalchemy을 바탕으로 작업을 해주는 스크립트를 작성하고, Jenkins를 이용하여 Cronjob을 실행시켰습니다.

![cronjob](https://user-images.githubusercontent.com/84912594/137124088-d3a2bc59-decd-49f3-a695-863c92715880.jpg)

<br>

## Figma

[LINK](https://www.figma.com/file/lhoMVBbDJclwdIhpG8uONm/%EB%AA%A8%EB%8B%A5%EB%B6%88-sketch?node-id=2%3A474)

<br>

## Modeling

<div align=center><img src="https://modakfire-static.s3.ap-northeast-2.amazonaws.com/readme/Modeling.png"></div>

<br>

## 구현 기능

### 메인

- 전체 갤러리 리스트 표시
- 인기 갤러리 및 인기 게시물 표시

<br>

### 게시물 리스트

- 최신순, 인기순으로 게시물 정렬
- 댓글 등록/수정/삭제
- 유저 네임카드 조회

<br>

### 게시글 작성

- 게시글 등록과 함께 이미지는 AWS S3에 저장
- DB에는 해당 이미지 오브젝트 URL 저장

<br>

### 회원가입 & 로그인

- 카카오, 네이버 소셜 로그인 API를 통한 유효성 검사
- JWT 토큰 발행 후, 사이트 내 로그인 수행 또는 회원가입 페이지
- 로그인 데코레이터
- 회원 정보 수정 / 탈퇴

<br>

### 마이페이지

- 내가 좋아요을 누른 게시물 리스트 확인
- 내가 댓글을 작성한 게시물 리스트 확인
- 네임카드 수정

<br>

### 네임카드

Card (명함)

- 명함 형식으로 사진, 이름, 슬로건, 이메일, 로컬지역 등의 간단한 정보 저장

History (이력)

- 유저의 이력을 타임 라인으로 작성
- 년도, 타이틀, 서브타이틀로 구성 (ex 2021년, 이사장 , 해오름 재단 영등포)

Introduce (소개&관심분야)

- 유저의 소개 및 관심분야를 자유롭게 텍스트로 작성

<br>

<br>

## **사용 기술 스택**

Backend : Python, Django, MySql, Postman, AWS, Docker, Jenkins

### Reference

이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
