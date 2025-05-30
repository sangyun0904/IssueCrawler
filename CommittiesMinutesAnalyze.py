import fitz  # PyMuPDF
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_sentences_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    # 페이지별 텍스트 수집
    for page in doc:
        full_text += page.get_text()

    # 문장 단위 분리 (한글 회의록 특성상 줄바꿈 포함)
    sentences = re.split(r'(?<=[.?!])\s+', full_text.strip())

    return sentences

# 사용 예시
pdf_path = "제22대국회 제422회(임시회) 제1차 보건복지위원회(전체회의) (2025.02.14.).pdf"
sentences = extract_sentences_from_pdf(pdf_path)

# 결과 출력
# for i, sentence in enumerate(sentences[:10], 1):
    # print(f"{i}. {sentence}")

def extract_speaker_statements(text):
    # "◯발언자 내용" 패턴 인식
    pattern = r"◯([^\n]+?) (.*?)\n"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

# 사용 예시
# doc = fitz.open(pdf_path)
# text = "".join([page.get_text() for page in doc])
# speaker_statements = extract_speaker_statements(text)

# for speaker, statement in speaker_statements[:5]:
    # print(f"{speaker.strip()} ➜ {statement.strip()[:100]}...")

def filter_important_sentences(sentences):
    text_block = "\n".join(f"- {s}" for s in sentences[:10])  # 한 번에 20문장씩

    prompt = f"""
        다음은 국회 회의록의 문장들이야. 이 중에서 **핵심 정보가 담긴 중요 문장만** 골라서 출력해줘.

        {text_block}
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    
    return response.output_text

if __name__ == "__main__":
    # PDF 파일 경로
    pdf_path = "제22대국회 제422회(임시회) 제1차 보건복지위원회(전체회의) (2025.02.14.).pdf"
    
    # PDF에서 문장 추출
    sentences = extract_sentences_from_pdf(pdf_path)
    
    # 중요 문장 필터링
    important_sentences = filter_important_sentences(sentences)
    
    # 결과 출력
    print("중요 문장:")
    print(important_sentences)