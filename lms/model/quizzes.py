import os
import typing

import edq.util.dirent
import quizcomp.constants
import quizcomp.question.base
import quizcomp.question.essay

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
            answers: typing.Union[typing.List[typing.Any], None] = None,
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

        if (answers is None):
            answers = []

        self.answers: typing.List[typing.Any] = answers
        """ Possible answers to this question. """

    def to_query(self) -> ResolvedQuestionQuery:
        """ Get a query representation of this question. """

        return ResolvedQuestionQuery(self)

    # TEST - Clean HTML
    # TEST - Supporting Files? Path Rewrites?
    # TEST - Many formats.
    # TEST - Answers
    def write(self, base_dir: str, force: bool = False) -> str:
        """
        Write this question to the given directory in Quiz Composer format and return the new directory for this question.
        If `force` is true, then any existing directory with the same name will be overwritten,
        otherwise an error will be raised.
        """

        base_dir = os.path.abspath(base_dir)

        dirname = f"{self.name} ({self.id})"
        out_dir = os.path.join(base_dir, dirname)

        if (os.path.exists(out_dir)):
            if (not force):
                raise ValueError(f"Path to write quiz question ('{dirname}') already exists: '{out_dir}'.")

            edq.util.dirent.remove(out_dir)

        edq.util.dirent.mkdir(out_dir)

        question = self._to_quizcomp()
        question.to_path(os.path.join(out_dir, quizcomp.constants.QUESTION_FILENAME))

        return out_dir

    def _to_quizcomp(self) -> quizcomp.question.base.Question:
        """ Get a QuizComp representation of this question. """

        data = {
            'question_type': str(self.question_type),
            'name': self.name,
            'prompt': self.prompt,
            'points': self.points,
            'ids': {'lms': self.id},
            'answers': self.answers,
        }

        question = quizcomp.question.base.Question.from_dict(data)
        question.validate()

        return question

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
