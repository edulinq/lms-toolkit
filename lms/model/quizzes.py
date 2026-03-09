import typing

import quizcomp.question.base

import lms.model.assignments
import lms.model.base
import lms.model.query

class QuestionQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS quiz question.
    In general, a quiz question can be queried by:
     - LMS Question ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedQuestionQuery(lms.model.query.ResolvedBaseQuery, QuestionQuery):
    """
    A QuestionQuery that has been resolved (verified) from a real quiz question instance.
    """

    _include_email = False

    def __init__(self,
            question: 'Question',
            **kwargs: typing.Any) -> None:
        super().__init__(id = question.id, name = question.name, **kwargs)

class Question(lms.model.base.BaseType):
    """
    A question within a quiz.
    """

    CORE_FIELDS = [
        'id',
        'question_type',
        'name',
        'prompt',
        'points',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            question_type: typing.Union[quizcomp.question.base.QuestionType, None] = None,
            name: typing.Union[str, None] = None,
            prompt: typing.Union[str, None] = None,
            points: typing.Union[float, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("Quiz questions must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this question. """

        if (question_type is None):
            raise ValueError("Quiz questions must have a type.")

        self.question_type: quizcomp.question.base.QuestionType = question_type
        """ The type of this question (multiple choice, essay, etc). """

        self.name: typing.Union[str, None] = name
        """ The display name of this question. """

        self.prompt: typing.Union[str, None] = prompt
        """ The prompt of this question. """

        self.points: typing.Union[float, None] = points
        """ The number of points possible for this queston. """

    def to_query(self) -> ResolvedQuestionQuery:
        """ Get a query representation of this question. """

        return ResolvedQuestionQuery(self)

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
