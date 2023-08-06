from api.mapper.algos.fuzzywuzzy import FuzzyWuzzy
from api.mapper.algos.fw_with_openai4 import FWWithOpenAI4
from api.mapper.algos.jw_with_openai4 import JWWithOpenAI4
from api.mapper.algos.openai import OpenAI
from api.mapper.algos.openaiGPT4 import OpenAIGPT4
from api.mapper.algos.rapidfuzz import RapidFuzz
from api.mapper.algos.stringmetric import Stringmetric
from api.mapper.algos.jw_with_openai import JWWithOpenAI
from api.mapper.algos.recursive_harmonization import RecursiveDataHarmonizer

def ai_merge(key, df1, df2):
    ########### AI code goes here ############
    openAI = OpenAI(key)
    text = openAI.invoke(df1, df2)
    ########### AI code ends here ############
    return text

def ai4_merge(key, df1, df2):
    ########### AI code goes here ############
    openAI4 = OpenAIGPT4(key)
    text = openAI4.invoke(df1, df2)
    ########### AI code ends here ############
    return text


def fuzzy_merge(key, df1, df2):
    fuzzywuzzy = FuzzyWuzzy()
    text = fuzzywuzzy.invoke(df1, df2)

    return text


def rapid_fuzzy_merge(key, df1, df2):
    fuzz = RapidFuzz()
    text = fuzz.invoke(df1, df2)

    return text


def stringmetric_merge(key, df1, df2):
    stringmetric = Stringmetric()
    text = stringmetric.invoke(df1, df2)

    return text


def stringmetric_with_chatgpt_merge(key, df1, df2):
    jw_with_openai = JWWithOpenAI(key)
    text = jw_with_openai.invoke(df1, df2)
    return text


def stringmetric_with_gpt4_merge(key, df1, df2):
    jw_with_openai = JWWithOpenAI4(key)
    text = jw_with_openai.invoke(df1, df2)
    return text


def fuzzywuzzy_with_gpt4_merge(key, df1, df2):
    fw_with_openai = FWWithOpenAI4(key)
    text = fw_with_openai.invoke(df1, df2)
    return text

def recursive_algo(key, df1, df2):
    rec_algo = RecursiveDataHarmonizer(key)
    text = rec_algo.harmonize_data(df1, df2)
    return text
