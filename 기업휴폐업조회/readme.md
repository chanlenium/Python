국세청_사업자등록정보 진위확인 및 상태조회 서비스
https://www.data.go.kr/data/15081808/openapi.do#tab_layer_detail_function

참고사이트 : Convert curl commands to Python, JavaScript and more
https://curlconverter.com/

배치 시점 : 매월 1일에 API를 호출하여 직전월 말일 기준의 테이블을 생성

# 알고리즘
1. CORP_BIZ_DATA 테이블에서 사업자번호(BRNO) 컬럼값을 중복제거하여 추출하여 API를 호출할 준비
2. 사업자번호로 구성된 파일을 읽어서 국세청_사업자등록정보 진위확인 및 상태조회 서비스 API를 호출<br/>
국세청 API 서비스 특성상 한번에 100개 기업만 조회 가능<br/>
![brno](https://github.com/chanlenium/Python/blob/main/%EA%B8%B0%EC%97%85%ED%9C%B4%ED%8F%90%EC%97%85%EC%A1%B0%ED%9A%8C/img/%EC%82%AC%EC%97%85%EC%9E%90%EB%B2%88%ED%98%B8.JPG)

3. 결과값을 받아옴<br/>
결과값 : b_stt_cd (01:정상, 02:휴업, 03:폐업)<br/>

4. API호출 시점(매월 1일)에 해당하는 "년월-1월"값을 기준년월(ggYm)에 저장하고, 이를 GG_YM 컬럼으로 추가하여 결과테이블 생성<br/>
일례로 2024년 4월 1일에 API를 호출했다면 이 결과 값의 기준년월(ggYm) 값은 202403임 (샘플 코드에는 이 내용이 반영되어있지는 않음)
![result](https://github.com/chanlenium/Python/blob/main/%EA%B8%B0%EC%97%85%ED%9C%B4%ED%8F%90%EC%97%85%EC%A1%B0%ED%9A%8C/img/%ED%9C%B4%ED%8F%90%EC%97%85%EC%A1%B0%ED%9A%8C%20%EA%B2%B0%EA%B3%BC.JPG)
