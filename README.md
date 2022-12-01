# statsu

Simple GUI Tool for Pandas DataFrame

## About
본 프로젝트는 Pandas의 DataFrame을 PySide6 기반으로 데이터 표시 및 편집까지 가능한 GUI 툴입니다. 코드 실행 중 콘솔 창 대신 GUI를 통해 시각적으로 확인하고 싶거나 사용자가 직접 편집하고 싶은 경우 활용 가능합니다.

## Installation

설치는 본 소스로부터 직접 설치하면 됩니다. 소스 다운로드나 git clone을 사용해서 컴퓨터에 저장 후 설치해도 되고 간편하게는 다음과 같이 pip를 이용해서 Github으로부터 설치할 수 있습니다.
```
git clone https://github.com/ysb06/statsu.git
cd {your project path}
pip install {statsu source path}
```

```
pip install git+https://github.com/ysb06/statsu.git
```

추후 PyPI에 등록하여 설치가 가능하도록 할 계획입니다.

## Usage

콘솔 창에 다음과 같이 입력하여 간단한 테스트를 할 수 있습니다.

```
python debug_run.py
```
실행 후 엑셀 파일이나 CSV파일로부터 데이터를 불러 올 수도 있습니다.

보거나 편집하고자 하는 DataFrame을 입력으로 넣어서도 볼 수 있습니다. 편집 후에는 저장 후 닫으면 편집된 결과도 받을 수 있습니다.

```Python
import pandas as pd
from statsu import show

df = pd.DataFrame({
    'a':[3.2, 'AAA', 9], 
    'b':[441, 3, 1.2], 
    'c':[0.6, 'DTD', 32]})

result = show(df)
```

## More Info.

### Issues, feedback and pull requests are welcome.

추가적으로 다른 아이디어나 의견 그리고 Pull Request는 언제든 주시면 가능한한 빨리 반영할 수 있도록 하겠습니다.

### 프로젝트 지향점

본 프로젝트의 시작은 개인 프로젝트였으며 현재는 DataFrame 조작을 위한 가장 기본적인 기능만 구현하고 있습니다. 가장 중요한 목적은 DataFrame Viewer지만 여기에 저의 필요에 따라 그래프나 통계 분석과 같은 기능들을 추가할 계획입니다.

[PandasGUI](https://github.com/adamerose/PandasGUI)가 본 프로젝트보다 기능이 더 많지만 본 프로젝트는 가능한 작고 쉽게 분할 가능한 코드를 통해 여러 프로젝트에 쉽게 활용되는 것을 지향합니다.

### Etc.

Code motivated by [PandasGUI](https://github.com/adamerose/PandasGUI). The code in the past commit includes PandasGUI code.