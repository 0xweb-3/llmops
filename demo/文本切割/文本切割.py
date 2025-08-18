import re
from typing import List
from langchain.tools import BaseTool
from sentence_transformers import SentenceTransformer, util

# Load MiniLM Chinese model
# 推荐使用 "paraphrase-multilingual-MiniLM-L12-v2" （支持中文）
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def initial_split(text: str) -> List[str]:
    """Split text by Chinese punctuation into candidate sentences"""
    sentences = re.split(r'([。！？；])', text)
    result = []
    buf = ""
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]
        if sentence.strip():
            result.append(sentence.strip())
    return result


def semantic_segmentation(text: str, threshold: float = 0.75) -> List[str]:
    """Segment text into semantically coherent chunks using MiniLM embeddings"""
    sentences = initial_split(text)
    if not sentences:
        return [text]

    # Encode with MiniLM
    embeddings = model.encode(sentences, convert_to_tensor=True)

    result = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = util.cos_sim(embeddings[i - 1], embeddings[i]).item()
        # If similarity is high, merge with previous sentence
        if sim > threshold:
            result[-1] += sentences[i]
        else:
            result.append(sentences[i])
    return result


# LangChain Tool
class ChineseSemanticSplitTool(BaseTool):
    name = "chinese_semantic_split"
    description = "Split Chinese text into semantically coherent chunks for TTS or NLP tasks"

    def _run(self, text: str) -> List[str]:
        return semantic_segmentation(text)

    async def _arun(self, text: str) -> List[str]:
        raise NotImplementedError("Async not supported yet.")


# === Example Usage ===
if __name__ == "__main__":
    tool = ChineseSemanticSplitTool()
    novel_text = "他望着远方的山峦，心中充满了希望。可是，夜幕即将降临，他必须找到栖身之所。风声在耳边呼啸，仿佛在催促他加快脚步。"

    chunks = tool.run(novel_text)
    print("切分结果：")
    for c in chunks:
        print("-", c)
