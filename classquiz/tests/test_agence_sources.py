# SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie
#
# SPDX-License-Identifier: MPL-2.0

"""Agence fork: source links on slides and questions (baillivetjulien/leohoot#42)."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from classquiz.agence import agence_slide_payload
from classquiz.db.models import QuizQuestion
from classquiz.socket_server.models import ReturnQuestion

ONISEP = {"label": "Les formations en apprentissage", "url": "https://www.onisep.fr/apprentissage"}


def question(**extra):
    return {"question": "Quel âge ?", "time": "20", "type": "ABCD", "answers": [{"right": True, "answer": "15 ans"}], **extra}


def slide(**extra):
    return {"question": "Conseil", "time": "20", "type": "SLIDE", "answers": "{}", **extra}


def test_sources_are_kept():
    q = QuizQuestion.model_validate(question(sources=[ONISEP]))
    assert q.model_dump()["sources"] == [ONISEP]


def test_sources_are_optional():
    assert QuizQuestion.model_validate(question()).sources is None


@pytest.mark.parametrize(
    "url", ["javascript:alert(1)", "ftp://example.org/file", "www.onisep.fr", "https://", "data:text/html,x"]
)
def test_only_http_links_are_accepted(url):
    with pytest.raises(ValidationError):
        QuizQuestion.model_validate(question(sources=[{"label": "Lien", "url": url}]))


def test_blank_label_is_rejected():
    with pytest.raises(ValidationError):
        QuizQuestion.model_validate(question(sources=[{"label": "   ", "url": "https://onisep.fr"}]))


def test_at_most_ten_sources():
    with pytest.raises(ValidationError):
        QuizQuestion.model_validate(question(sources=[ONISEP] * 11))


def test_sources_reach_the_phones_with_the_question():
    q = QuizQuestion.model_validate(question(sources=[ONISEP]))
    sent = ReturnQuestion(
        **{**q.model_dump(), "answers": [{"answer": "15 ans", "color": None}], "type": q.type}
    ).model_dump()
    assert sent["sources"] == [ONISEP]


def test_slide_payload_for_the_phones():
    game = SimpleNamespace(
        questions=[
            QuizQuestion.model_validate(question()),
            QuizQuestion.model_validate(
                slide(slide={"layout": "TITLE_TEXT_IMAGE", "title": "Des conseils individualisés"}, sources=[ONISEP])
            ),
        ]
    )
    assert agence_slide_payload(game, 1) == {
        "question_index": 1,
        "title": "Des conseils individualisés",
        "sources": [ONISEP],
    }


def test_slide_payload_falls_back_on_the_question_text():
    game = SimpleNamespace(questions=[QuizQuestion.model_validate(slide())])
    assert agence_slide_payload(game, 0) == {"question_index": 0, "title": "Conseil", "sources": []}
