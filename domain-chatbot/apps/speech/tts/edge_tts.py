import logging
import os
import subprocess

from ..utils.uuid_generator import generate

logger = logging.getLogger(__name__)

edge_voices = [
    # 中文音色
    {"id": "zh-CN-XiaoxiaoNeural", "name": "晓晓 (中文女声)"},
    {"id": "zh-CN-XiaoyiNeural", "name": "晓伊 (中文女声)"},
    {"id": "zh-CN-YunjianNeural", "name": "云健 (中文男声)"},
    {"id": "zh-CN-YunxiNeural", "name": "云希 (中文男声)"},
    {"id": "zh-CN-YunxiaNeural", "name": "云霞 (中文女声)"},
    {"id": "zh-CN-YunyangNeural", "name": "云扬 (中文男声)"},
    {"id": "zh-CN-liaoning-XiaobeiNeural", "name": "晓北 (东北话)"},
    {"id": "zh-CN-shaanxi-XiaoniNeural", "name": "晓妮 (陕西话)"},
    {"id": "zh-HK-HiuGaaiNeural", "name": "曉佳 (粤语女声)"},
    {"id": "zh-HK-HiuMaanNeural", "name": "曉曼 (粤语女声)"},
    {"id": "zh-HK-WanLungNeural", "name": "雲龍 (粤语男声)"},
    {"id": "zh-TW-HsiaoChenNeural", "name": "曉臻 (台湾女声)"},
    {"id": "zh-TW-HsiaoYuNeural", "name": "曉雨 (台湾女声)"},
    {"id": "zh-TW-YunJheNeural", "name": "雲哲 (台湾男声)"},

    # 日语音色 - 女声
    {"id": "ja-JP-NanamiNeural", "name": "Nanami (日语女声-明亮欢快)"},
    {"id": "ja-JP-AoiNeural", "name": "Aoi (日语女声-好奇活泼)"},
    {"id": "ja-JP-MayuNeural", "name": "Mayu (日语女声-生动明亮)"},
    {"id": "ja-JP-ShioriNeural", "name": "Shiori (日语女声-温柔)"},

    # 日语音色 - 男声
    {"id": "ja-JP-KeitaNeural", "name": "Keita (日语男声-随性)"},
    {"id": "ja-JP-DaichiNeural", "name": "Daichi (日语男声-稳重)"},
    {"id": "ja-JP-NaokiNeural", "name": "Naoki (日语男声-成熟)"},

    # 英语音色 - 美国
    {"id": "en-US-JennyNeural", "name": "Jenny (美式女声-温暖)"},
    {"id": "en-US-AriaNeural", "name": "Aria (美式女声-自然)"},
    {"id": "en-US-GuyNeural", "name": "Guy (美式男声-稳重)"},
    {"id": "en-US-DavisNeural", "name": "Davis (美式男声-活力)"},
    {"id": "en-US-JaneNeural", "name": "Jane (美式女声-专业)"},
    {"id": "en-US-JasonNeural", "name": "Jason (美式男声-友好)"},
    {"id": "en-US-SaraNeural", "name": "Sara (美式女声-柔和)"},
    {"id": "en-US-MichelleNeural", "name": "Michelle (美式女声-友好)"},
    {"id": "en-US-AshleyNeural", "name": "Ashley (美式女声-甜美)"},
    {"id": "en-US-AmberNeural", "name": "Amber (美式女声-活泼)"},
    {"id": "en-US-AnaNeural", "name": "Ana (美式女声-热情)"},
    {"id": "en-US-EmmaNeural", "name": "Emma (美式女声-年轻)"},
    {"id": "en-US-MonicaNeural", "name": "Monica (美式女声-成熟)"},
    {"id": "en-US-CoraNeural", "name": "Cora (美式女声-清晰)"},

    # 英语音色 - 英国
    {"id": "en-GB-SoniaNeural", "name": "Sonia (英式女声-优雅)"},
    {"id": "en-GB-LibbyNeural", "name": "Libby (英式女声-清脆)"},
    {"id": "en-GB-MaisieNeural", "name": "Maisie (英式女声-欢快)"},
    {"id": "en-GB-RyanNeural", "name": "Ryan (英式男声-绅士)"},
    {"id": "en-GB-ThomasNeural", "name": "Thomas (英式男声-成熟)"},
    {"id": "en-GB-BellaNeural", "name": "Bella (英式女声-温柔)"},
    {"id": "en-GB-HollieNeural", "name": "Hollie (英式女声-明亮)"},
    {"id": "en-GB-OliviaNeural", "name": "Olivia (英式女声-专业)"},

    # 英语音色 - 澳大利亚
    {"id": "en-AU-NatashaNeural", "name": "Natasha (澳式女声-清晰)"},
    {"id": "en-AU-WilliamNeural", "name": "William (澳式男声-强劲)"},
    {"id": "en-AU-AnnetteNeural", "name": "Annette (澳式女声-友好)"},
    {"id": "en-AU-FreyaNeural", "name": "Freya (澳式女声-自然)"},

    # 英语音色 - 爱尔兰
    {"id": "en-IE-EmilyNeural", "name": "Emily (爱尔兰女声-温暖)"},
    {"id": "en-IE-ConnorNeural", "name": "Connor (爱尔兰男声-友好)"},

    # 英语音色 - 加拿大
    {"id": "en-CA-ClaraNeural", "name": "Clara (加拿大女声-清晰)"},
    {"id": "en-CA-LiamNeural", "name": "Liam (加拿大男声-自然)"}
]


class Edge():

    def remove_html(self, text: str):
        # TODO 待改成正则
        new_text = text.replace('[', "")
        new_text = new_text.replace(']', "")
        return new_text

    def create_audio(self, text: str, voiceId: str):
        new_text = self.remove_html(text)
        pwdPath = os.getcwd()
        file_name = generate() + ".mp3"
        filePath = pwdPath + "/tmp/" + file_name
        dirPath = os.path.dirname(filePath)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        if not os.path.exists(filePath):
            # 用open创建文件 兼容mac
            open(filePath, 'a').close()

        subprocess.run(["edge-tts", "--voice", voiceId, "--text", new_text,
                        "--write-media", str(filePath)])

        return file_name
