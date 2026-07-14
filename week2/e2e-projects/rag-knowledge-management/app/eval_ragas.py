import asyncio
import json
import pandas as pd
import requests

from ragas import evaluate
from ragas import SingleTurnSample, EvaluationDataset
from langchain_openai import ChatOpenAI
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.run_config import RunConfig

from .logger import get_logger

logger = get_logger(__name__)

oai_llm = ChatOpenAI(model="gpt-4o-mini")
logger.info("ChatOpenAI initialized for RAGAS evaluation: model=gpt-4o-mini")

def load_jsonl(path):
    logger.info("Loading test data from: %s", path)
    with open(path, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    logger.info("Loaded %d test Q&A pairs", len(lines))
    return lines

def print_eval_res(eval_result):
    scores = eval_result.scores
    eval_str = ' | Q | '
    for k in scores[0].keys():
        eval_str = eval_str + str(k) + ' | '
    logger.info("Evaluation results table header: %s", eval_str)
    print(eval_str)
    for i, score in enumerate(scores):
        eval_str = ' | ' + str(i + 1) + ' | '
        for k in score.keys():
            eval_str = eval_str + str(score[k]) + ' | '
        print(eval_str)
    res = eval_result.to_pandas()
    means = res.mean(numeric_only=True).to_dict()
    logger.info("RAGAS averages: %s", means)
    print("\n📈 Averages:")
    for k, v in means.items():
        print(f"- {k}: {v:.3f}")

async def evaluate_rag_system(test_path="../seed/qna_test.json"):
    logger.info("=" * 60)
    logger.info("RAGAS EVALUATION STARTED")
    logger.info("=" * 60)

    test_data = load_jsonl(test_path)
    results = []

    for idx, item in enumerate(test_data):
        question = item["question"]
        reference_answer = item["answer"]
        logger.info("[%d/%d] Evaluating: question='%s'", idx + 1, len(test_data), question)

        url = 'http://localhost:8000/ask'
        myobj = {'question': question}
        logger.debug("POST %s with question='%s'", url, question)
        res = requests.post(url, json=myobj).json()
        answer, contexts = res['answer'], res['contexts']
        logger.info("Got answer (first 100 chars): %s...", answer[:100] if answer else "(empty)")
        logger.info("Retrieved %d context(s)", len(contexts))

        results.append(SingleTurnSample(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts,
            reference=reference_answer
        ))
        logger.debug("Sample %d appended to evaluation dataset", idx + 1)

    logger.info("Creating EvaluationDataset with %d samples", len(results))
    ds = EvaluationDataset(results)

    metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
    logger.info("Metrics to evaluate: %s", [m.name for m in metrics])

    run_config = RunConfig(max_workers=16, timeout=30)
    logger.info("Running RAGAS evaluation (max_workers=16, timeout=30s)...")
    eval_result = evaluate(dataset=ds, metrics=metrics, llm=oai_llm, run_config=run_config)
    logger.info("RAGAS evaluation complete")

    print("RAGAS Evals Results")
    print_eval_res(eval_result)

    logger.info("=" * 60)
    logger.info("RAGAS EVALUATION FINISHED")
    logger.info("=" * 60)


if __name__ == "__main__":
    logger.info("Starting RAGAS evaluation script")
    asyncio.run(evaluate_rag_system())
