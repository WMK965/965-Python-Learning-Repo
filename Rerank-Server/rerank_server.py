import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import CrossEncoder
import torch

# === 配置区域 ===
MODEL_PATH = "BAAI/bge-reranker-base"  # 模型名称，会自动下载
PORT = 9997                             # 服务端口
# ================

app = FastAPI()

print(f"正在加载模型 {MODEL_PATH}，请稍候...")
# 检测是否有显卡
device = "cuda" if torch.cuda.is_available() else "cpu"
# 加载模型
model = CrossEncoder(MODEL_PATH, device=device, trust_remote_code=True)
print(f"模型加载完成！运行在: {device}")

class RerankRequest(BaseModel):
    model: str = "bge-reranker-base"
    query: str
    documents: list[str]
    top_n: int = None

@app.post("/v1/rerank")
async def rerank(request: RerankRequest):
    if not request.documents:
        return {"results": []}
    
    # 构造 (Query, Doc) 对
    pairs = [[request.query, doc] for doc in request.documents]
    
    # 推理打分
    scores = model.predict(pairs)
    
    # 格式化结果
    results = []
    for idx, score in enumerate(scores):
        results.append({
            "index": idx,
            "relevance_score": float(score),
            "document": {
                "text": request.documents[idx]
            }
        })
    
    # 排序 (分数从高到低)
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # 截取 top_n
    if request.top_n:
        results = results[:request.top_n]
        
    return {
        "model": request.model,
        "results": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)