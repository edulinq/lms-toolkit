import os
import typing

import edq.util.dirent
import edq.util.json
import quizcomp.constants
import quizcomp.group
import quizcomp.question.base
import quizcomp.quiz

import lms.model.assignments
import lms.model.base
import lms.model.query

QUESTIONS_DIRNAME: str = 'questions'

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
        'answers',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            question_type: typing.Union[quizcomp.question.base.QuestionType, None] = None,
            name: typing.Union[str, None] = None,
            prompt: typing.Union[str, None] = None,
            points: typing.Union[float, None] = None,
            answers: typing.Union[typing.List[typing.Any], typing.Dict[str, typing.Any], None] = None,
            group_id: typing.Union[str, None] = None,
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

        self.answers: typing.Union[typing.List[typing.Any], typing.Dict[str, typing.Any]] = answers
        """ Possible answers to this question. """

        self.group_id: typing.Union[str, None] = group_id
        """ The id of the group this question belongs to (in context of the chosen quiz). """

    def to_query(self) -> ResolvedQuestionQuery:
        """ Get a query representation of this question. """

        return ResolvedQuestionQuery(self)

    def get_label(self) -> str:
        """ Get the label for this question. """

        return f"{self.name} ({self.id})"

    # TEST - Supporting Files? Path Rewrites?
    def write(self, base_dir: str, force: bool = False) -> str:
        """
        Write this question to the given directory in Quiz Composer format and return the new directory for this question.
        If `force` is true, then any existing directory with the same name will be overwritten,
        otherwise an error will be raised.
        """

        base_dir = os.path.abspath(base_dir)

        dirname = self.get_label()
        out_dir = os.path.join(base_dir, dirname)

        if (os.path.exists(out_dir)):
            if (not force):
                raise ValueError(f"Path to write quiz question ('{dirname}') already exists: '{out_dir}'.")

            edq.util.dirent.remove(out_dir)

        edq.util.dirent.mkdir(out_dir)

        question = self._to_quizcomp_data()
        question.to_path(os.path.join(out_dir, quizcomp.constants.QUESTION_FILENAME))

        return out_dir

    def _to_quizcomp_data(self) -> quizcomp.question.base.Question:
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

class QuestionGroupQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS quiz question group.
    In general, a quiz question group can be queried by:
     - LMS Question Group ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedQuestionGroupQuery(lms.model.query.ResolvedBaseQuery, QuestionGroupQuery):
    """
    A QuestionGroupQuery that has been resolved (verified) from a real quiz question question instance.
    """

    _include_email = False

    def __init__(self,
            group: 'QuestionGroup',
            **kwargs: typing.Any) -> None:
        super().__init__(id = group.id, name = group.name, **kwargs)

class QuestionGroup(lms.model.base.BaseType):
    """
    A question group within a quiz.
    This allows a quiz to choose a specific number of questions for each part of the quiz,
    e.g., the group may have 10 questions, and 3 are chosen when the quiz is given/generated.
    """

    CORE_FIELDS = [
        'id',
        'name',
        'pick_count',
        'points',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            pick_count: typing.Union[int, None] = None,
            points: typing.Union[float, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("Quiz question groups must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this group. """

        self.name: typing.Union[str, None] = name
        """ The display name of this group. """

        self.pick_count: typing.Union[int, None] = pick_count
        """ The number of questions to choose for this group. """

        self.points: typing.Union[float, None] = points
        """ The number of points possible for this queston. """

    def to_query(self) -> ResolvedQuestionGroupQuery:
        """ Get a query representation of this question group. """

        return ResolvedQuestionGroupQuery(self)

    def get_label(self) -> str:
        """ Get the label for this group. """

        return f"{self.name} ({self.id})"

    def _to_quizcomp_data(self,
            all_questions: typing.List[Question],
            questions_rel_dir: str = QUESTIONS_DIRNAME,
            ) -> typing.Dict[str, typing.Any]:
        """
        Get a QuizComp representation of this group.
        The path to each question will be based on the base dir and the question's label.
        """

        group_question_paths = []
        for question in all_questions:
            if (self.id == question.group_id):
                path = os.path.join(questions_rel_dir, question.get_label())
                group_question_paths.append(path)

        return {
            'name': self.name,
            'pick_count': self.pick_count,
            'points': self.points,
            'questions': group_question_paths,
            'ids': {'lms': self.id},
        }

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

    def write(self, base_dir: str, groups: typing.List[QuestionGroup], questions: typing.List[Question], force: bool = False) -> str:
        """
        Write this quiz to the given directory in Quiz Composer format and return the new directory for this quiz.
        This will also write out all the questions to "questions" dir in the returned directory.
        If `force` is true, then any existing directory with the same name will be overwritten,
        otherwise an error will be raised.
        """

        base_dir = os.path.abspath(base_dir)

        dirname = f"{self.name} ({self.id})"
        out_dir = os.path.join(base_dir, dirname)

        if (os.path.exists(out_dir)):
            if (not force):
                raise ValueError(f"Path to write quiz ('{dirname}') already exists: '{out_dir}'.")

            edq.util.dirent.remove(out_dir)

        edq.util.dirent.mkdir(out_dir)

        quiz = self._to_quizcomp_data(groups, questions)
        edq.util.json.dump_path(quiz, os.path.join(out_dir, quizcomp.constants.QUIZ_FILENAME), sort_keys = False, indent = 4)

        questions_dir = os.path.join(out_dir, QUESTIONS_DIRNAME)
        for question in questions:
            question.write(questions_dir, force = force)

        return out_dir

    def _to_quizcomp_data(self, groups: typing.List[QuestionGroup], questions: typing.List[Question]) -> quizcomp.quiz.Quiz:
        """ Get a QuizComp representation of this quiz. """

        quizcomp_groups = [group._to_quizcomp_data(questions) for group in groups]

        return {
            'title': self.name,
            'description': self.description,
            'groups': quizcomp_groups,
            'ids': {'lms': self.id},
        }
