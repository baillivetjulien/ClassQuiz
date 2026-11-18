# SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie
#
# SPDX-License-Identifier: MPL-2.0

"""Agence fork: optional native slide content on quiz questions (baillivetjulien/leohoot#41)."""

import pytest
from pydantic import ValidationError

from classquiz.db.models import AgenceSlideLayout, QuizInput, QuizQuestion


def slide_question(slide):
    return {"question": "Enquête insertion", "time": "20", "type": "SLIDE", "answers": "{}", "slide": slide}


def test_slide_content_is_kept_through_validation_and_dump():
    question = QuizQuestion.model_validate(slide_question({"layout": "BIG_IMAGE", "title": "Enquête insertion 2025"}))
    assert question.slide.layout == AgenceSlideLayout.BIG_IMAGE
    assert question.model_dump(mode="json")["slide"] == {
        "layout": "BIG_IMAGE",
        "title": "Enquête insertion 2025",
        "text": None,
    }


def test_layout_defaults_to_title_text_image():
    question = QuizQuestion.model_validate(slide_question({"title": "Conseil", "text": "En présentiel\nÀ distance"}))
    assert question.slide.layout == AgenceSlideLayout.TITLE_TEXT_IMAGE
    assert question.slide.text == "En présentiel\nÀ distance"


def test_questions_without_slide_are_unchanged():
    question = QuizQuestion.model_validate(
        {"question": "Vrai ou faux ?", "time": "20", "type": "ABCD", "answers": [{"right": True, "answer": "Vrai"}]}
    )
    assert question.slide is None


def test_unknown_layout_is_rejected():
    with pytest.raises(ValidationError):
        QuizQuestion.model_validate(slide_question({"layout": "CAROUSEL"}))


def test_editor_input_keeps_slide_content():
    quiz = QuizInput.model_validate(
        {"title": "RDV Parents", "description": "", "questions": [slide_question({"layout": "TEXT", "title": "Bon à savoir"})]}
    )
    assert quiz.model_dump()["questions"][0]["slide"]["title"] == "Bon à savoir"
