국세청_사업자등록정보 진위확인 및 상태조회 서비스
https://www.data.go.kr/data/15081808/openapi.do#tab_layer_detail_function

참고사이트 : Convert curl commands to Python, JavaScript and more
https://curlconverter.com/

배치 시점 : 매월 1일에 API를 호출하여 직전월 말일 기준의 테이블을 생성

# 알고리즘
1. CORP_BIZ_DATA 테이블에서 사업자번호(BRNO) 컬럼값을 중복제거하여 추출하여 API를 호출할 준비
2. 사업자번호로 구성된 파일을 읽어서 국세청_사업자등록정보 진위확인 및 상태조회 서비스 API를 호출
![poster](../img/사업자번호.jpg)
4. 결과값을 받아옴
결과값 : b_stt_cd (1:정상, 2:휴업, 3:폐업)

5. API호출 시점(매월 1일)에 해당하는 "년월-1월"값을 기준년월(ggYm)에 저장하고, 이를 GG_YM 컬럼으로 추가하여 결과테이블 생성
일례로 2024년 4월 1일에 API를 호출했다면 이 결과 값의 기준년월(ggYm) 값은 202403임 (샘플 코드에는 이 내용이 반영되어있지는 않음)
