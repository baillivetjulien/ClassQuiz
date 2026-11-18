# SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie
#
# SPDX-License-Identifier: MPL-2.0

"""Agence fork helpers, kept out of the upstream modules to ease merges."""

from typing import Protocol

from classquiz.db.models import QuizQuestion


class _HasQuestions(Protocol):
    questions: list[QuizQuestion]


def agence_slide_payload(game_data: _HasQuestions, index: int) -> dict:
    """Message sent to the teams' phones when the host shows a slide (baillivetjulien/leohoot#42):
    the slide title and its source links, so the phones can display them as clickable links."""
    question = game_data.questions[index]
    title = question.slide.title if question.slide and question.slide.title else question.question
    return {
        "question_index": index,
        "title": title,
        "sources": [source.model_dump() for source in question.sources or []],
    }
