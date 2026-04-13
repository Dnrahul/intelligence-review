"""Data export utilities — CSV, Excel, and JSON output for review analysis results."""

import csv
import io
import json
import logging
import os
from pathlib import Path
from typing import List

import pandas as pd

from app.models.schemas import AnalyzeResponse, ReviewData

logger = logging.getLogger(__name__)

DATA_DIR = Path("data")


def _reviews_to_records(reviews: List[ReviewData]) -> List[dict]:
    """Convert ReviewData list to flat dictionaries for tabular export."""
    return [
        {
            "ID": review.id,
            "Author": review.author,
            "Rating": review.rating,
            "Date": review.date or "",
            "Title": review.title or "",
            "Review Text": review.text,
            "Verified Purchase": "Yes" if review.verified else "No",
            "Helpful Votes": review.helpful_count,
            "Sentiment": review.sentiment.value if review.sentiment else "",
            "Sentiment Score": review.sentiment_score,
            "Key Phrases": " | ".join(review.key_phrases) if review.key_phrases else "",
        }
        for review in reviews
    ]


def to_dataframe(reviews: List[ReviewData]) -> pd.DataFrame:
    """Convert review data to a clean Pandas DataFrame."""
    return pd.DataFrame(_reviews_to_records(reviews))


def to_json(response: AnalyzeResponse) -> str:
    """Serialize the full analysis response to formatted JSON."""
    return response.model_dump_json(indent=2)


def to_csv(reviews: List[ReviewData]) -> str:
    """Export reviews to a human-readable CSV string."""
    try:
        df = to_dataframe(reviews)
        output = io.StringIO()
        df.to_csv(output, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
        return output.getvalue()
    except Exception as e:
        logger.error(f"Failed to export to CSV: {e}")
        # Fallback: manual CSV generation
        if not reviews:
            return "ID,Author,Rating,Date,Title,Review Text,Verified Purchase,Helpful Votes,Sentiment,Sentiment Score,Key Phrases\n"
        
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerow(["ID", "Author", "Rating", "Date", "Title", "Review Text", "Verified Purchase", "Helpful Votes", "Sentiment", "Sentiment Score", "Key Phrases"])
        
        for review in reviews:
            try:
                writer.writerow([
                    review.id or "",
                    review.author or "",
                    review.rating or "",
                    review.date or "",
                    review.title or "",
                    review.text or "",
                    "Yes" if review.verified else "No",
                    review.helpful_count or 0,
                    review.sentiment.value if review.sentiment else "",
                    review.sentiment_score or "",
                    " | ".join(review.key_phrases) if review.key_phrases else "",
                ])
            except Exception as e:
                logger.warning(f"Failed to write review {review.id}: {e}")
                continue
        
        return output.getvalue()


def save_results(response: AnalyzeResponse) -> None:
    """
    Persist analysis results to disk in three formats:
      - data/results.json   — full structured response
      - data/reviews.csv    — flat tabular view of all reviews
      - data/reviews.xlsx   — Excel workbook with summary + reviews sheets
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. JSON — full structured output
    json_path = DATA_DIR / "results.json"
    try:
        json_path.write_text(to_json(response), encoding="utf-8")
        logger.info(f"Saved JSON results → {json_path}")
    except Exception as exc:
        logger.error(f"Failed to save JSON: {exc}")

    # 2. CSV — flat review records
    csv_path = DATA_DIR / "reviews.csv"
    try:
        csv_path.write_text(to_csv(response.reviews), encoding="utf-8")
        logger.info(f"Saved CSV results → {csv_path}")
    except Exception as exc:
        logger.error(f"Failed to save CSV: {exc}")

    # 3. Excel — multi-sheet workbook
    xlsx_path = DATA_DIR / "reviews.xlsx"
    try:
        _save_excel(response, xlsx_path)
        logger.info(f"Saved Excel results → {xlsx_path}")
    except Exception as exc:
        logger.error(f"Failed to save Excel: {exc}")


def _save_excel(response: AnalyzeResponse, path: Path) -> None:
    """Write a polished Excel workbook with a summary sheet and a reviews sheet."""
    with pd.ExcelWriter(path, engine="openpyxl") as writer:

        # Sheet 1: Executive Summary
        summary = response.summary
        summary_data = {
            "Field": [
                "Product", "Source URL", "Analyzed At",
                "Total Reviews", "Overall Sentiment", "Sentiment Score",
                "Average Rating", "Positive Reviews", "Negative Reviews",
                "Neutral/Mixed Reviews", "Summary", "Recommendation",
                "Key Strengths", "Key Weaknesses",
            ],
            "Value": [
                response.product_name or "N/A",
                response.source_url,
                response.analyzed_at,
                summary.total_reviews,
                summary.overall_sentiment.value.capitalize(),
                f"{summary.overall_score:+.2f}",
                f"{summary.average_rating:.1f}/5" if summary.average_rating else "N/A",
                summary.positive_count,
                summary.negative_count,
                summary.neutral_count,
                summary.summary_text,
                summary.recommendation,
                " | ".join(summary.strengths),
                " | ".join(summary.weaknesses),
            ],
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)

        # Sheet 2: Individual Reviews
        reviews_df = to_dataframe(response.reviews)
        reviews_df.to_excel(writer, sheet_name="Reviews", index=False)

        # Sheet 3: Themes (if any)
        if response.themes:
            themes_data = [
                {
                    "Theme": t.name,
                    "Review Count": t.count,
                    "Sentiment": t.sentiment.value.capitalize(),
                    "Sample Quotes": " | ".join(t.sample_quotes),
                }
                for t in response.themes
            ]
            pd.DataFrame(themes_data).to_excel(writer, sheet_name="Themes", index=False)
