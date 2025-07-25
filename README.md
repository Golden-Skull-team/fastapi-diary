# fastapi-diary

## ERD
<img width="874" height="522" alt="erd" src="https://github.com/user-attachments/assets/16efc066-b711-4774-b61a-e99153feccbe" />

| 테이블명     | 설명                                         | 필드                                                         |
|--------------|----------------------------------------------|--------------------------------------------------------------|
| diaries      | 유저가 작성한 일기 정보를 저장할 테이블입니다. | - 유저 정보<br>- 제목<br>- 내용<br>- 감정 요약(AI 분석 결과)<br>- 기분 (기쁨, 슬픔, 분노, 피곤, 짜증, 무난)<br>- 작성일자<br>- 수정일자 |
| users        | 커스텀 유저 모델을 저장할 테이블입니다.        | - 이메일 (로그인 시 사용)<br>- 비밀번호<br>- 닉네임<br>- 이름<br>- 전화번호<br>- 마지막 로그인<br>- 스태프 여부<br>- 관리자 여부<br>- 계정 활성화 여부<br>- 생성일<br>- 수정일 |
| tags         | 일기에 사용된 태그를 관리하는 테이블입니다.      | - 태그 ID<br>- 태그명                                         |
| diary_tags   | 일기와 태그의 관계를 관리하는 테이블입니다.     | - 일기 ID<br>- 태그 ID                                         |

## 회원가입 / 로그인 / 로그아웃 Flowchart
<img width="625" height="796" alt="image" src="https://github.com/user-attachments/assets/c02ba607-c95b-4820-b1e2-08d85eb0e537" />
