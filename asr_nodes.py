import folder_paths
import os
import tempfile
import torchaudio
from typing import Optional
from faster_whisper import WhisperModel
import torch

models_dir = folder_paths.models_dir
model_path = os.path.join(models_dir, "TTS", "Belle-whisper-large-v3-zh-punct-ct2")
cache_dir = folder_paths.get_temp_directory()

def cache_audio_tensor(
    cache_dir,
    audio_tensor,
    sample_rate: int,
    filename_prefix: str = "cached_audio_",
    audio_format: Optional[str] = ".wav"
) -> str:
    try:
        with tempfile.NamedTemporaryFile(
            prefix=filename_prefix,
            suffix=audio_format,
            dir=cache_dir,
            delete=False 
        ) as tmp_file:
            temp_filepath = tmp_file.name
        
        torchaudio.save(temp_filepath, audio_tensor, sample_rate)

        return temp_filepath
    except Exception as e:
        raise Exception(f"Error caching audio tensor: {e}")

def convert_subtitle_format(data):
  lines = []
  for entry in data:
    # We only need the start timestamp for this format
    start_time_seconds = entry['timestamp'][0]
    text = entry['text']

    # Convert seconds to minutes, seconds, and milliseconds
    # Work with total milliseconds to avoid floating point issues
    total_milliseconds = int(start_time_seconds * 1000)

    minutes = total_milliseconds // (1000 * 60)
    remaining_milliseconds = total_milliseconds % (1000 * 60)
    seconds = remaining_milliseconds // 1000
    milliseconds = remaining_milliseconds % 1000

    # Format the timestamp string as [MM:SS.mmm]
    # Use f-string formatting with zero-padding
    timestamp_str = f"[{minutes:02d}:{seconds:02d}.{milliseconds:03d}]"

    # Combine timestamp and text
    line = f"{timestamp_str}{text}"
    lines.append(line)

  # Join all lines with a newline character
  return "\n".join(lines)

class ASRZhRun:
    def __init__(self):
        self.model_cache = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = "default"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamps_type": (["none", "segment", "word"], {"default": "word"}),
                "max_num_words_per_page": ("INT", {"default": 24, "min": 1, "max": 50}),
                "dtype": (["default", "float16", "int8_float16", "int8_cpu"], {"default": "default"}),
                "unload_model": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "json_text", "subtitle_text")
    FUNCTION = "run_inference"
    CATEGORY = "🎤MW/MW-ASR-zh"

    def run_inference(
        self,
        audio,
        timestamps_type="none",
        max_num_words_per_page=24,
        dtype="default",
        unload_model=True,
    ):
        audio_file = cache_audio_tensor(
            cache_dir,
            audio["waveform"].squeeze(0),
            audio["sample_rate"],
        )

        self.dtype = dtype
        if dtype == "int8_cpu":
            self.device = "cpu"
            self.dtype = "int8"

        if self.model_cache is None:
            print(f"Loading ASR model from: {model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}. Please check paths.")
            
            self.model_cache = WhisperModel(model_path, device=self.device, compute_type=self.dtype)

        segments, info = self.model_cache.transcribe(audio_file, word_timestamps=True)
        segments = list(segments)
        if unload_model:
            self.model_cache = None
            torch.cuda.empty_cache()

        texts = "".join([segment.text for segment in segments])

        if timestamps_type == "none":
            return (texts, "", "")
        elif timestamps_type == "word":
            json_text = self.split_into_sentences(segments, max_num_words_per_page)
            subtitle_text = convert_subtitle_format(json_text)
            return (texts, str(json_text), subtitle_text)
        else:
            json_text = [{"timestamp": [i.start, i.end], "text": i.text} for i in segments]
            subtitle_text = convert_subtitle_format(json_text)
            return (texts, str(json_text), subtitle_text)

    def split_into_sentences(self, segments, max_num_words_per_page):
        sentences = []
        current_sentence =  {"timestamp": None, "text": ""}
        
        num_words = 0
        for segment in segments:
            for word in segment.words:
                if current_sentence["timestamp"] is None:
                    current_sentence["timestamp"] = []
                    current_sentence["timestamp"].append(round(word.start, 2))
                current_sentence["text"] += word.word

                num_words += 1
                # 如果遇到句号或问号，结束当前句子
                if word.word.endswith(("。", "，", "、", "：", "；", "？", "！", 
                                          "”", "’", "）", "——", "……", "》", ".", 
                                          ",", ";", ":", "?", "!", ")", "--", "…")):
                    num_words = 0
                    current_sentence["timestamp"].append(round(word.end, 2))
                    current_sentence["text"] = current_sentence["text"].strip()
                    sentences.append(current_sentence)
                    current_sentence = {"timestamp": None, "text": ""}

                elif num_words > max_num_words_per_page:
                    num_words = 0
                    current_sentence["timestamp"].append(round(word.end, 2))
                    current_sentence["text"] = current_sentence["text"].strip()
                    sentences.append(current_sentence)
                    current_sentence = {"timestamp": None, "text": ""}
        
        # 处理未结束的句子
        if current_sentence["text"]:
            current_sentence["timestamp"].append(round(word.end, 2))
            current_sentence["text"] = current_sentence["text"].strip()
            sentences.append(current_sentence)
        
        return sentences


NODE_CLASS_MAPPINGS = {
    "ASRZhRun": ASRZhRun,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ASRZhRun": "自动中文语音识别",
}