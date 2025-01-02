import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from scipy.fft import fft
from scipy.stats import pearsonr

# 1. 저역통과 필터 설정 (20-120Hz)
def bandpass_filter(data, lowcut=20, highcut=120, fs=4000, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# 2. 신호 대 잡음비 (SNR) 계산
def calculate_snr(signal, noise):
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# 3. 주파수 대역 정확도 계산
def frequency_band_accuracy(user_fft, ref_fft, threshold=0.05):
    user_norm = user_fft / np.max(user_fft)
    ref_norm = ref_fft / np.max(ref_fft)
    diff = np.abs(user_norm - ref_norm)
    accuracy = 100 * np.mean(diff < threshold)
    return accuracy

# 4. 데이터 로드 및 전처리
def load_and_preprocess(file_path, fs=4000):
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # 스테레오 데이터를 모노로 변환
    if sample_rate != fs:
        raise ValueError("샘플링 레이트가 다릅니다. 통일된 샘플링 레이트를 사용하세요.")
    data = bandpass_filter(data, fs=fs)
    data = data / np.max(np.abs(data))  # 노멀라이제이션
    return data

# 5. FFT 분석
def compute_fft(data, fs, target_length=None):
    if target_length:
        data = data[:target_length]  # 데이터 길이 맞춤
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1/fs)
    fft_magnitude = np.abs(fft(data)[:len(freqs)])
    return freqs, fft_magnitude

# 6. 메인 함수
def main(user_file, reference_file):
    fs = 4000  # 샘플링 레이트

    # 사용자 신호와 참조 신호 로드
    user_data = load_and_preprocess(user_file, fs)
    reference_data = load_and_preprocess(reference_file, fs)

    # 두 신호의 길이를 맞춤
    min_length = min(len(user_data), len(reference_data))
    user_data = user_data[:min_length]
    reference_data = reference_data[:min_length]

    # FFT 비교
    freqs, user_fft = compute_fft(user_data, fs, min_length)
    _, ref_fft = compute_fft(reference_data, fs, min_length)

    # SNR 계산
    noise = user_data - reference_data  # 가정: 참조 데이터가 노이즈 없는 신호
    snr = calculate_snr(user_data, noise)

    # 상관계수 계산
    correlation, _ = pearsonr(user_data, reference_data)

    # 주파수 대역 정확도
    freq_accuracy = frequency_band_accuracy(user_fft, ref_fft)

    # 결과 출력
    print("/n=== 결과 분석 ===")
    print(f"{'평가 항목':<20}{'제작 청진기':<15}")
    print("-" * 50)
    print(f"{'상관계수':<20}{correlation:.4f}")
    print(f"{'SNR (dB)':<20}{snr:.2f}")
    print(f"{'주파수 대역 정확도':<20}{freq_accuracy:.2f} %")

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(freqs, user_fft, label="User FFT")
    plt.plot(freqs, ref_fft, label="Reference FFT", alpha=0.7)
    plt.title("Frequency Spectrum Comparison")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(user_data, label="User Signal")
    plt.plot(reference_data, label="Reference Signal", alpha=0.7)
    plt.title("Time Domain Signal Comparison")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.tight_layout()
    plt.show()

# 파일 경로 입력
user_file = "유연준-20041008-가슴-3117782.wav"
reference_file = "the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data/50017_PV.wav"
main(user_file, reference_file)
