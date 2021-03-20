# eurasian-otter
Synology file automate moving application

특정 폴더에 있는 파일(source)을 특정 위치(target)에 tag명의 폴더를 생성해 파일을 이동 시켜주는 어플리케이션이다. 

# How to Install
1. DSM 제어판 > 모든 패키지 > Python3를 설치함.
2. 적당히 script를 돌릴 위치에 소스파일을 다운로드 한다.   
    - ssh를 사용하는 경우 `wget https://github.com/fennec-fox/eurasian-otter/archive/refs/heads/main.zip` 를 해도 된다.
3. 압축을 푼다. `7z x main.zip`
4. ./install.sh를 수행한다.
   - pip를 자동으로 설치
   - python3에 필요한 pyYAML 모듈을 자동으로 설치
5. configuration.yaml을 자신에게 맞게 수정한다.
   ```
      config:
         path:
            source: download station이 파일을 받는 위치이다.
            target: dlna를 설정한 위치 혹은 파일을 이동 시키고 싶은 위치
         media-types:
            video: 이동 시킬 파일의 확장자명 '|'를 이용해 더 추가 한다.
         operations:
            file:
               action: copy or move source 위치에 원본 파일을 두고 복사를 하거나 아예 이동을 시키는 옵션이다.Cancel Changes
               overwrite: true or false 만약 target path에 이미 동일한 이름의 파일이 있는 경우 덮어쓰기 할지 정한다.
      tags:
         simple:이동 or 복사시킬 파일명을 정한다 , 를 이용해 나열한다.                
   ```
6. ./start.sh를 이용해서 정상적으로 동작하는지 확인한다.
7. DSM 스케줄러에 등록한다.

### Command Line Install
```sh
wget https://github.com/fennec-fox/eurasian-otter/archive/refs/heads/main.zip
7z x main.zip
cd eurasian-otter-main/
./install.sh
vi configuration.yaml
./start.sh
```

### 주의사항
- DSM 스케줄러에 등록 시 다음과 같이 등록을 해야 한다.
  - `cd /파일이 있는 절대경로/eurasian-otter-main && ./start.sh`
