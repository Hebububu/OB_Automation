# 출고 자동화를 위한 레포지토리입니다.

## 개요
- 매번 반복되는 기기 제품 출고를 자동화하기 위함.

## 구현 방법 
- 관리용 태그를 추가함으로써 실제로 필요한 데이터만 필터링 (기기 출고)
- ~~스토어의 제품명은 상품 키워드 점수를 위해 매번 바뀔 가능성이 농후함. 우선은 DB에 상품명을 그대로 저장~~
- ~~제품명이 변경될때마다 수동으로 관리용 태그를 추가하는 방식으로 진행~~
- 이후에 제품 데이터를 유동적으로 마켓에서 불러오는 방식으로 관리용 태그를 직접 수정하지 않아도 되게 하기. (ERP 시스템과 병합할 예정)

- 확인해보니 스토어별 고유 상품 ID를 가져올 수 있었음. 고유 상품 ID와 관리용 태그 두개를 조합해서 자동화가 가능할 것 같음.
- 일단은 EMP에서 가져온 xlsx 데이터로 자동화 구현부터 시작.

## xlsx 데이터 구조
1. 판매사이트명
2. 판매사이트 상품코드
3. 판매자ID 
4. 상품명
5. 주문선택사항 (옵션 등)
6. 주문수량 

## 필요한 기능 
1. 판매 사이트명 별로 구분하여 데이터를 정렬
2. 판매 사이트명 별로 구분된 데이터를 판매자 ID 별로 다시 정렬
3. 정렬된 데이터에 관리용 태그를 추가하는 기능 (관리용 태그란, 정확한 제품명을 의미함.)
4. 관리용 태그가 있는 제품별로 데이터를 정렬하여 각 관리용 태그별로 몇개의 제품이 출고되었는지 확인하는 기능. 
5. 주문선택사항(옵션) 항목이 필요한 제품이 있을 수 있으니, xlsx로 정렬된 데이터를 내보내는 기능. 

## 고민해봐야 할 점
1. 이미 스토어별로 상품에 대하여 pgsql로 만들어둔 마진 테이블이 있다.. 이걸 그대로 사용하는게 좋을까, 아니면 임시로 SQLite로 출고 자동화 기능부터 만든 다음 데이터 구조를 다듬어서 기존의 ERP 시스템에 결합하는게 좋을까.. 
ㄴ SQLite로 일단 실사용 가능하게 구현하는게 좋을 것 같다. 


# 임시 디렉토리 구조도
```
📦OB_AUTOMATION
 ┣ 📂app
 ┃ ┣ 📂core
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂database
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂utils
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📂config
 ┃ ┗ 📜__init__.py
 ┣ 📂data
 ┃ ┣ 📂db
 ┃ ┃ ┗ 📜test.db
 ┃ ┣ 📂input
 ┃ ┃ ┗ 📜자동화.xlsx
 ┃ ┗ 📂output
 ┣ 📂scripts
 ┃ ┗ 📜__init__.py
 ┣ 📂tests
 ┃ ┗ 📜__init__.py
 ┣ 📜.gitignore
 ┣ 📜main.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
 ```

 ## 사용할 모듈
 - pandas(데이터 처리 구조를 구현하기 위함)
 - openpyxl (엑셀 파일 직접 조작)
 - SQlite(데이터베이스)
 - SQLAlchemy(ORM, 추후 pgSQL로 마이그레이션 고려)

## 구현 순서

### 1. 기본 데이터 처리
- xlsx 파서 구현 (app/core/parser.py)

#### parser.py
- 만들어야 할 기능들이 무엇이 있을까..
1. 초기화 (init)
2. 파일 읽기 (read_xslx)
3. 데이터 검증 (validate_data)
4. 플랫폼별 데이터 정렬 (sort_by_platform)
5. 판매자 ID 별 데이터 정렬 (sort_by_id)
6. 관리용 태그 기반 필터링 (filter_by_tag)
7. 출고 수량 집계 (count_ob)
8. 결과 내보내기 (export_xslx)

- 만들다 보니 추가한 기능
1. 판매 사이트별 주문 수량 합계 계산 (count_by_platform)
- 나중에 유용하게 쓸 거 같음. 
- 이거 디스코드 봇이랑 연동하면 좋을듯. 매일 출고 데이터 양 기록해서 주, 달, 년 식으로 그래프화 해서 보여주게끔 하기. 
- 이거 할려면 결국엔 pgsql로 넘어가야하네
2. 플랫폼, 판매자ID, 상품명 순서대로 데이터 정렬 (sort_by_platform_seller_product)
- 일단 ID별과 플랫폼별로 만들긴 했는데, 한번에 데이터 정렬하는 기능도 필요함. 

### 2. 데이터베이스 구조 구현
1. 데이터베이스는 platform, product_code, product_name, tag 4개의 컬럼으로 구성
2. DatabaseManager class를 통해 데이터베이스 관리.

3. CRUD 구현
- add_product (제품 추가)
- get_product (제품 조회)
- update_product_tag (태그 수정)
- delete_product (제품 삭제)

### 3. 관리용 태그 시스템 구현
- 태그 관리용 모듈 (app/core/tag_manager.py)
- filter_valid_tags 메소드 구현 (지정된 valid_tags와 일치하는 태그를 가진 제품만 필터링)
 
### 4. 출고 분석 기능 구현
- 출고 분석 모듈 (app/core/shipment_analyzer.py)
- 데이터 내보내기 (app/core/exporter.py)

### 5. CLI 인터페이스 구현
- main.py 