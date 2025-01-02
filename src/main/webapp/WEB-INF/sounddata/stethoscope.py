import serial
import wave
import os  # 파일 삭제를 위한 라이브러리
import numpy as np
from scipy.signal import butter, lfilter
from scipy.ndimage import uniform_filter1d
from pydub import AudioSegment  # MP3 변환을 위한 라이브러리

# 시리얼 포트 설정
ser = serial.Serial('COM3', 115200, timeout=1)

# 대역 필터 설정 (장기 소리 강조: 20Hz ~ 120Hz 범위)
def butter_bandpass_filter(data, lowcut=20, highcut=120, fs=4000, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# 이동 평균 필터 (잡음 제거 후 소리 부드럽게 처리)
def moving_average_filter(data, window_size=5):
    return uniform_filter1d(data, size=window_size)

# 다이나믹 레인지 압축 (소리 강조)
def dynamic_range_compression(audio_data, threshold=0.1, ratio=4):
    audio_data = np.array(audio_data)
    compressed_audio = np.copy(audio_data)

    # 압축 적용 (임계값 이상으로 강한 신호만 압축)
    above_threshold = np.abs(audio_data) > threshold
    compressed_audio[above_threshold] = np.sign(audio_data[above_threshold]) * (threshold + (np.abs(audio_data[above_threshold]) - threshold) / ratio)

    return compressed_audio

# 데이터 수집 및 WAV 파일로 저장
def record_audio(save_as_mp3=False):
    wav_filename = input("(이름-생년월일 8자리-남/여-주민등록번호 뒷자리) 파일명을 입력해주세요 : ") + ".wav"

    print("Sending 'start' to Arduino...")
    ser.write(b"start\n")  # 'start' 명령 전송
    print("Waiting for Arduino response...")

    audio_data = []
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"Arduino says: {response}")

            if response == "Recording started...":
                print("Recording started")
            elif response == "Recording finished":
                print("Recording finished")
                break
            elif response.isdigit() or (response.startswith('-') and response[1:].isdigit()):
                audio_data.append(int(response))  # 아두이노에서 전송된 오디오 데이터 수집

    # 데이터를 numpy 배열로 변환 및 스케일링
    audio_array = np.array(audio_data, dtype=np.float32)
    audio_array /= np.max(np.abs(audio_array))  # 노멀라이제이션

    # 잡음 제거 및 필터링
    filtered_audio = butter_bandpass_filter(audio_array)  # 대역 통과 필터 (20Hz ~ 120Hz)
    smoothed_audio = moving_average_filter(filtered_audio)  # 이동 평균 필터
    emphasized_audio = dynamic_range_compression(smoothed_audio)  # 다이나믹 레인지 압축 (장기 소리 강조)

    # WAV 파일로 저장
    with wave.open(wav_filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # 모노 채널
        wav_file.setsampwidth(2)  # 샘플 폭 2바이트
        wav_file.setframerate(4000)  # 샘플링 레이트
        wav_file.writeframes((emphasized_audio * 32767).astype(np.int16).tobytes())
    print(f"Recording saved as '{wav_filename}'")

    # MP3로 변환 및 WAV 파일 삭제
    if save_as_mp3:
        mp3_filename = wav_filename.replace(".wav", ".mp3")
        convert_to_mp3(wav_filename, mp3_filename)
        # os.remove(wav_filename)  # WAV 파일 삭제
        # print(f"WAV file '{wav_filename}' deleted.")

def convert_to_mp3(wav_file, mp3_file):
    """WAV 파일을 MP3로 변환"""
    sound = AudioSegment.from_wav(wav_file)
    sound.export(mp3_file, format="mp3")
    print(f"Recording saved as '{mp3_file}'")

# 사용자 입력에 따라 WAV 또는 MP3로 저장
def main():
    print("Press Enter to start communication with Arduino...")
    input()
    print("Sending 'start' to Arduino...")
    record_audio(save_as_mp3=True)  # MP3 변환 여부를 True로 설정

# 메인 실행
if __name__ == "__main__":
    main()

# 시리얼 포트 닫기
ser.close()
