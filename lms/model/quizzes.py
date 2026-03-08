import typing

import lms.model.assignments
import lms.model.base
import lms.model.query

class QuizQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS quiz.
    In general, a quiz can be queried by:
     - LMS Quiz ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedQuizQuery(lms.model.query.ResolvedBaseQuery, QuizQuery):
    """
    A QuizQuery that has been resolved (verified) from a real quiz instance.
    """

    _include_email = False

    def __init__(self,
            quiz: 'Quiz',
            **kwargs: typing.Any) -> None:
        super().__init__(id = quiz.id, name = quiz.name, **kwargs)

class Quiz(lms.model.assignments.Assignment):
    """
    A quiz within a course.
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

    def to_query(self) -> ResolvedQuizQuery:  # type: ignore[override]
        """ Get a query representation of this quiz. """

        return ResolvedQuizQuery(self)
