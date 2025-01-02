# Stethoscope AI 프로젝트

## 📕 프로젝트 소개

이 프로젝트는 피지오넷 데이터를 기반으로 심장음 및 폐음 녹음하여 청진 데이터를 수집하는 프로젝트 입니다. `filter.py`는 사용자와 비슷한 데이터셋을 필터링하며, `main.py`는 신호를 처리하고 비교 분석하는 주요 프로그램입니다. `stethoscope.py`는 데이터를 수집하는 데 사용됩니다.

## 📑 목차

- [프로젝트 소개](#프로젝트-소개)
- [주요 기능](#주요-기능)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [필터링 및 신호 분석](#필터링-및-신호-분석)
- [실시간 신호 분석](#실시간-신호-분석)
- [출처](#출처)
- [기여자](#기여자)

## 📌 주요 기능

- **데이터 필터링**  
  `filter.py`는 피지오넷의 수많은 데이터셋 중 자신의 신체 스펙과 가장 비슷한 데이터를 추출출합니다.

- **주파수 분석 및 시각화**  
  `main.py`는 FFT(빠른 푸리에 변환)를 사용하여 신호를 주파수 영역에서 분석하고, 상관계수, 신호 대 잡음비(SNR), 주파수 대역 정확도를 계산하여 결과를 출력합니다.

- **실시간 데이터 처리**  
  `stethoscope.py`는 임베디드 시스템을 통해 청진 데이터를 녹음합니다.

## 📥 설치 방법

이 프로젝트를 설치하고 실행하려면 아래 단계를 따르세요:

1. **필수 라이브러리 설치**

    ```shell
    pip install numpy==1.20.3
    pip install scipy==1.7.3
    pip install matplotlib==3.4.3
    pip install opencv-python==4.9.0.80
    pip install pyserial==3.5
    pip install pydub==0.25.1
    pip install seaborn==0.12.2
    pip install pandas==1.5.3
    https://ffmpeg.org/download.html ffmeg 다운로드
    ```
    이 프로젝트는 Python 3.11.4에서 테스트되었습니다.

## 🛠 사용 순서
filter.py에서 데이터셋 선별 -> stethoscope에서 청진음 데이터 수집 -> main.py에서 피지오넷 데이터셋과 비교교

### 필터링 및 신호 분석

1. **`filter.py`** 파일은 피지오넷의 수많은 심음데이터 중 사용자와 비슷한 신체 스펙을 가진 데이터셋을 걸러내는 역할을 합니다.

2. **`stethoscope.py`** 아두이노에서 수집한 청진음 데이터를 실시간으로 필터링 및 처리하여 WAV 또는 MP3 파일로 저장합니다.
    주요 함수:
    - **밴드패스 필터**: `butter_bandpass_filter` 20Hz에서 120Hz 범위의 주파수 대역을 필터링하여 장기 소리를 강조합니다.
    - **이동 평균 필터**: `moving_average_filter` 신호를 부드럽게 처리하여 잡음을 줄이고 신호를 정리합니다.
    - **다이나믹 레인지 압축**: `dynamic_range_compression` 신호의 강한 부분을 압축하여 다이나믹 레인지를 줄이고, 소리를 강조합니다.

3. **`main.py`** 파일은 신호 분석을 수행하고, FFT 분석을 통해 사용자와 참조 신호 간의 주파수 대역 정확도 및 상관계수를 계산합니다.
    주요 함수:
    - **밴드패스 필터**: `bandpass_filter` 함수는 20Hz에서 120Hz까지의 주파수를 필터링합니다. 이 주파수 대역은 일반적인 심장음 및 폐음의 주요 주파수 대역에 해당합니다.
    - **SNR 계산**: `calculate_snr` 함수는 신호와 잡음의 비율을 계산하여, 신호 품질을 평가합니다.
    - **주파수 대역 정확도 계산**: `frequency_band_accuracy` 함수는 사용자 신호와 참조 신호의 FFT 비교를 통해 정확도를 계산합니다.

### **하드웨어**

- **MAX9814**: [Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX9814.pdf)
  - MAX9814는 자동 게인 조정(AGC)을 제공하는 마이크 증폭기로, 아날로그 오디오 신호를 증폭하여 Arduino에서 읽을 수 있도록 도와줍니다.
  
- **ADS1115**: [Datasheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf?ts=1734622495127&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252Fko-kr%252FADS1115)
  - ADS1115는 16비트 아날로그-디지털 변환기(ADC)로, 고정밀 아날로그 신호를 디지털로 변환하는 데 사용됩니다. Arduino와 I2C 인터페이스를 통해 연결하여 사용합니다.

- **Breakout Microphone**: [DataSheet](https://cdn.sparkfun.com/datasheets/Sensors/Sound/CEM-C9745JAD462P2.54R.pdf)
  - Breakout Microphone은 소리 신호를 아날로그 전압으로 변환하여 Arduino로 전달하는 작은 전자 장치입니다.

### **데이터셋**
본 프로젝트에서는 아래와 같은 데이터셋을 사용하여 피지오넷의 심음과 직접 청진한 청진데이터와 비교하여 직접 제작한 청진기의 성능을 비교합니다.
  
- **circor-heart-sound**: 
  - https://physionet.org/content/circor-heart-sound/1.0.3/ 소아 심장 잡음 감지 및 분류 연구를 위해 0~21세 환자들의 5272개 심장 소리 녹음을 포함한 세계 최대 규모의 청진 데이터셋.

## 👥 기여자

- **[202336900 유연준]**: 웹 프론트, 백엔드 구축 및 전체 총괄
- **[202336889 김윤민]**: 하드웨어 설계
- **[202336905 이성준]**: 하드웨어 구현 및 README.md 작성
- **[202336915 하정진]**: 발표 및 기획
- **[202336886 김민준]**: 발표 및 기획
