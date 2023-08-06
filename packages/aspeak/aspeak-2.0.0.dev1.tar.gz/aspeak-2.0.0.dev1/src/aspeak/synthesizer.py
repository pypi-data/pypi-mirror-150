from typing import Union

import azure.cognitiveservices.speech as speechsdk
import requests

from .token import Token
from .urls import voice_list_url


class Synthesizer:
    def __init__(self, audio_config: speechsdk.audio.AudioOutputConfig = None, locale: str = 'en-US',
                 voice: Union[str, None] = None, audio_format: speechsdk.SpeechSynthesisOutputFormat = None):
        self._current_token = Token()
        self._audio_config = audio_config or speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self._cfg = self._base_speech_config()
        self._voice = voice
        self._locale = locale
        self._cfg.speech_synthesis_language = locale
        self._format = audio_format
        if voice is not None:
            self._cfg.speech_synthesis_voice_name = voice
        if self._format is not None:
            self._cfg.set_speech_synthesis_output_format(self._format)
        self._synthesizer_cache = speechsdk.SpeechSynthesizer(speech_config=self._cfg,
                                                              audio_config=self._audio_config)

    @property
    def _token(self) -> Token:
        if self.expired:
            self.renew()
        return self._current_token

    @property
    def expired(self) -> bool:
        return self._current_token.expired()

    @property
    def _config(self) -> speechsdk.SpeechConfig:
        if self.expired:
            self.renew()
        return self._cfg

    @property
    def _synthesizer(self) -> speechsdk.SpeechSynthesizer:
        if self.expired:
            self.renew()
        return self._synthesizer_cache

    def renew(self) -> None:
        self._current_token.renew()
        self._cfg = self._base_speech_config()
        self._cfg.speech_synthesis_language = self._locale
        if self._voice is not None:
            self._cfg.speech_synthesis_voice_name = self._voice
        if self._format is not None:
            self._cfg.set_speech_synthesis_output_format(self._format)
        self._synthesizer_cache = speechsdk.SpeechSynthesizer(speech_config=self._cfg, audio_config=self._audio_config)

    def _base_speech_config(self) -> speechsdk.SpeechConfig:
        return speechsdk.SpeechConfig(auth_token=self._token.token, region=self._token.region)

    def get_voice_list(self) -> list:
        r = requests.get(voice_list_url(self._token.region),
                         headers={'Authorization': 'Bearer ' + self._token.token})
        return r.json()

    def text_to_speech(self, text: str) -> speechsdk.SpeechSynthesisResult:
        return self._synthesizer.speak_text_async(text).get()

    def ssml_to_speech(self, ssml: str) -> speechsdk.SpeechSynthesisResult:
        return self._synthesizer.speak_ssml_async(ssml).get()
