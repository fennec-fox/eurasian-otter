# eurasian-otter
synology file automate moving application

# Install
1. DSM 제어판 > 모든 패키지 > Python3를 설치함.
2. 적당히 script를 돌릴 위치에 소스파일을 다운로드 한다.   
    - ssh를 사용하는 경우 `wget https://github.com/fennec-fox/eurasian-otter/archive/refs/heads/main.zip` 를 해도 된다.
3. 압축을 푼다.
4. ./install.sh를 수행한다.
5. configuration.yaml을 자신에게 맞게 수정한다.
6. ./start.sh를 이용해서 정상적으로 동작하는지 확인한다.
7. DSM 스케줄러에 등록한다.
