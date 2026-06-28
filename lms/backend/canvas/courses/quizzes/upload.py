import os
import re
import typing

import edq.util.hash
import quizcomp.model.answer
import quizcomp.model.config
import quizcomp.model.group
import quizcomp.model.question
import quizcomp.model.quiz

import lms.backend.canvas.common
import lms.backend.canvas.courses.quizzes.common
import lms.model.assignments
import lms.model.constants

CREATE_FOLDER_ENDPOINT: str = "/api/v1/courses/{course_id}/folders"
GET_FOLDER_ENDPOINT: str = "/api/v1/courses/{course_id}/folders/by_path{canvas_path}"
HIDE_FOLDER_ENDPOINT: str = "/api/v1/folders/{folder_id}"
LIST_ASSIGNMENT_GROUPS_ENDPOINT: str = "/api/v1/courses/{course_id}/assignment_groups?per_page={page_size}"
UPLOAD_FILE_ENDPOINT: str = "/api/v1/courses/{course_id}/files"
UPLOAD_GROUP_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/groups"
UPLOAD_QUESTION_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/questions"
UPLOAD_QUIZ_METADATA_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes"

CANVAS_QUIZCOMP_BASEDIR: str = '/quiz-composer'
CANVAS_QUIZCOMP_QUIZ_DIRNAME: str = 'quizzes'

QUIZ_TYPE_ASSIGNMENT: str = 'assignment'

QUESTION_TYPE_MAP: typing.Dict[quizcomp.model.constants.QuestionType, str] = {
    # Direct Mappings
    quizcomp.model.constants.QuestionType.ESSAY: 'essay_question',
    quizcomp.model.constants.QuestionType.FIMB: 'fill_in_multiple_blanks_question',
    quizcomp.model.constants.QuestionType.MATCHING: 'matching_question',
    quizcomp.model.constants.QuestionType.MA: 'multiple_answers_question',
    quizcomp.model.constants.QuestionType.MCQ: 'multiple_choice_question',
    quizcomp.model.constants.QuestionType.MDD: 'multiple_dropdowns_question',
    quizcomp.model.constants.QuestionType.NUMERICAL: 'numerical_question',
    quizcomp.model.constants.QuestionType.TEXT_ONLY: 'text_only_question',
    quizcomp.model.constants.QuestionType.TF: 'true_false_question',
    # Indirect Mappings
    quizcomp.model.constants.QuestionType.FITB: 'short_answer_question',
    quizcomp.model.constants.QuestionType.SA: 'essay_question',
}

def request(
        backend: typing.Any,
        course_id: int,
        quiz: quizcomp.model.quiz.Quiz,
        ) -> lms.model.assignments.Assignment:
    """
    Upload a quiz.

    This is a process that takes many steps.
     1) Upload Quiz Files
     2) Upload Quiz Metadata
     3) Upload Quiz Question Groups (first create question groups and then upload questions).
    """

    _upload_quiz_images(backend, course_id, quiz)

    assignment_group_id = _fetch_assignment_group(backend, course_id, quiz)

    quiz_metadata = _upload_quiz_metadata(backend, course_id, quiz, assignment_group_id)

    for group in quiz.get_groups():
        _upload_group(backend, course_id, int(quiz_metadata.id), group)

    _restore_image_sources(quiz)

    return quiz_metadata

def _fetch_assignment_group(
        backend: typing.Any,
        course_id: int,
        quiz: quizcomp.model.quiz.Quiz,
        ) -> typing.Union[int, None]:
    """ Get the assignment group ID for this quiz, or None if nothing is found. """

    if (quiz.assignment_group is None):
        return None

    url = backend.server + LIST_ASSIGNMENT_GROUPS_ENDPOINT.format(course_id = course_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'name': quiz.assignment_group,
        }
        backend.not_found('assignment group', identifiers)

        return None

    for raw_object in raw_objects:
        if (raw_object.get('name', None) == quiz.assignment_group):
            return int(raw_object['id'])

    return None

def _upload_quiz_metadata(
        backend: typing.Any,
        course_id: int,
        quiz: quizcomp.model.quiz.Quiz,
        assignment_group_id: typing.Union[int, None],
        ) -> lms.model.assignments.Assignment:
    """ Upload the base quiz metadata, which we can then attach questions to. """

    quiz_type = QUIZ_TYPE_ASSIGNMENT
    if ((quiz.practice is None) or (quiz.practice is True)):
        quiz_type = lms.backend.canvas.courses.quizzes.common.QUIZ_TYPE_PRACTICE

    description = quiz.description.to_canvas()
    if (quiz.version is not None):
        description = f"<p>{description}</p><br /><hr /><p>Version: {quiz.version}</p>"

    raw_hide_results = None
    if (quiz.hide_results is not None):
        if (quiz.hide_results is not quizcomp.model.quiz.HideResultsBehavior.NEVER_HIDE):
            raw_hide_results = quiz.hide_results.value

    raw_scoring_policy = None
    if (quiz.scoring_policy is not None):
        raw_scoring_policy = quiz.scoring_policy.value

    data = {
        'quiz[title]': quiz.get_name(),
        'quiz[description]': description,
        'quiz[quiz_type]': quiz_type,
        'quiz[published]': (quiz.publish is True),
        'quiz[assignment_group_id]': assignment_group_id,
        'quiz[time_limit]': quiz.time_limit_mins,
        'quiz[allowed_attempts]': quiz.allowed_attempts,
        # Canvas wants a string instead of a bool here (despite documentation).
        'quiz[show_correct_answers]': str((quiz.show_correct_answers is not False)).lower(),
        'quiz[hide_results]': raw_hide_results,
        # Canvas wants a string instead of a bool here (despite documentation).
        'quiz[shuffle_answers]': str(quiz.get_config(quizcomp.model.config.OPTION_SHUFFLE_ANSWERS)).lower(),
        'quiz[scoring_policy]': raw_scoring_policy,
    }

    url = backend.server + UPLOAD_QUIZ_METADATA_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_data = typing.cast(typing.Dict[str, typing.Any],
            lms.backend.canvas.common.make_post_request(url, headers = headers, data = data))

    return lms.model.assignments.Assignment(
        id = str(raw_data['id']),
        name = quiz.get_name(),
        description = quiz.description.to_md(),
    )

def _upload_group(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        group: quizcomp.model.group.Group,
        ) -> None:
    """ Upload a question group (including all questions) for an existing quiz. """

    data = {
        'quiz_groups[][name]': group.get_name(),
        'quiz_groups[][pick_count]': group.pick_count,
        'quiz_groups[][question_points]': group.get_child_points(),
    }

    url = backend.server + UPLOAD_GROUP_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_data = typing.cast(typing.Dict[str, typing.Any],
            lms.backend.canvas.common.make_post_request(url, headers = headers, data = data))

    group_id = raw_data['quiz_groups'][0]['id']

    for (i, question) in enumerate(group.children):
        _upload_question(backend, course_id, quiz_id, group_id, question, i)

def _upload_question(
        backend: typing.Any,
        course_id: int,
        quiz_id: int,
        group_id: int,
        question: quizcomp.model.question.Question,
        index: int,
        ) -> None:
    """ Create a question within the given quiz/group. """

    data = _create_question_json(group_id, question, index)

    url = backend.server + UPLOAD_QUESTION_ENDPOINT.format(course_id = course_id, quiz_id = quiz_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)

def _create_question_json(
        group_id: int,
        question: quizcomp.model.question.Question,
        index: int,
        ) -> typing.Dict[str, typing.Any]:
    """ Create a dict that represent a question for a Canvas API request. """

    name = question.get_name()

    custom_header = question.get_config(quizcomp.model.config.OPTION_CUSTOM_HEADER)
    if (custom_header is not None):
        name = custom_header

    data = {
        'question[question_type]': QUESTION_TYPE_MAP[question.question_type],
        'question[question_name]': name,
        'question[quiz_group_id]': group_id,
        # The actual points is taken from the group,
        # but put in a one here so people don't get scared when they see a zero.
        'question[points_possible]': 1,
        'question[position]': index,
        'question[question_text]': question.prompt.to_canvas(),
    }

    if (question.feedback is not None):
        if (question.feedback.general is not None):
            data['question[neutral_comments_html]'] = question.feedback.general.to_canvas()

        if (question.feedback.correct is not None):
            data['question[correct_comments_html]'] = question.feedback.correct.to_canvas()

        if (question.feedback.incorrect is not None):
            data['question[incorrect_comments_html]'] = question.feedback.incorrect.to_canvas()

    _serialize_answers(data, question)

    return data

def _serialize_answers(
        data: typing.Dict[str, typing.Any],
        question: quizcomp.model.question.Question,
        ) -> None:
    """ Convert a question's answers to Canvas JSON and insert it into the give dict. """

    if (question.question_type is quizcomp.model.constants.QuestionType.ESSAY):
        # Text-based questions have no answers in canvas.
        pass
    elif (question.question_type is quizcomp.model.constants.QuestionType.FIMB):
        _serialize_fimb_answers(data, typing.cast(quizcomp.model.answer.MultiplePartTextAnswers, question.answers))
    elif (question.question_type is quizcomp.model.constants.QuestionType.FITB):
        answers = quizcomp.model.answer.MultiplePartTextAnswers(parts = {'': typing.cast(quizcomp.model.answer.TextAnswers, question.answers)})
        _serialize_fimb_answers(data, answers)
    elif (question.question_type is quizcomp.model.constants.QuestionType.MATCHING):
        _serialize_matching_answers(data, typing.cast(quizcomp.model.answer.MatchingAnswers, question.answers))
    elif (question.question_type is quizcomp.model.constants.QuestionType.MA):
        _serialize_choice_answers(data, typing.cast(quizcomp.model.answer.ChoiceAnswers, question.answers), False)
    elif (question.question_type is quizcomp.model.constants.QuestionType.MCQ):
        _serialize_choice_answers(data, typing.cast(quizcomp.model.answer.ChoiceAnswers, question.answers), False)
    elif (question.question_type is quizcomp.model.constants.QuestionType.MDD):
        _serialize_mdd_answers(data, typing.cast(quizcomp.model.answer.MultiplePartChoiceAnswers, question.answers))
    elif (question.question_type is quizcomp.model.constants.QuestionType.NUMERICAL):
        _serialize_numeric_answers(data, typing.cast(quizcomp.model.answer.NumericAnswers, question.answers))
    elif (question.question_type is quizcomp.model.constants.QuestionType.SA):
        # Text-based questions have no answers in canvas.
        pass
    elif (question.question_type is quizcomp.model.constants.QuestionType.TEXT_ONLY):
        # Text-based questions have no answers in canvas.
        pass
    elif (question.question_type is quizcomp.model.constants.QuestionType.TF):
        _serialize_choice_answers(data, typing.cast(quizcomp.model.answer.ChoiceAnswers, question.answers), True)
    else:
        raise ValueError(f"Unknown question type: '{question.question_type.value}'.")

def _serialize_choice_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.ChoiceAnswers,
        use_text: bool,
        blank_id: typing.Union[str, None] = None,
        start_index: int = 0,
        ) -> None:
    """ Serialize choice-based answers. """

    for (i, choice) in enumerate(answers.choices):
        index = start_index + i

        weight = 0
        if (choice.correct):
            weight = 100

        data[f"question[answers][{index}][answer_weight]"] = weight

        if (use_text):
            text = choice.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)
            data[f"question[answers][{index}][answer_text]"] = text
        else:
            html = choice.text.to_canvas()
            data[f"question[answers][{index}][answer_html]"] = html

        if (blank_id is not None):
            data[f"question[answers][{index}][blank_id]"] = blank_id

        if ((choice.feedback is not None) and (choice.feedback.general is not None)):
            data[f"question[answers][{index}][answer_comment_html]"] = choice.feedback.general.to_canvas()

def _serialize_fimb_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.MultiplePartTextAnswers,
        ) -> None:
    """ Serialize FIMB-like answers. """

    index = 0

    for (key, answer) in answers.parts.items():
        for option in answer.options:
            data[f"question[answers][{index}][blank_id]"] = key
            data[f"question[answers][{index}][answer_weight]"] = 100
            data[f"question[answers][{index}][answer_text]"] = option.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)

            if ((option.feedback is not None) and (option.feedback.general is not None)):
                data[f"question[answers][{index}][answer_comment_html]"] = option.feedback.general.to_canvas()

            index += 1

def _serialize_matching_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.MatchingAnswers,
        ) -> None:
    """ Serialize matching answers. """

    for (i, (left, right)) in enumerate(answers.pairs):
        data[f"question[answers][{i}][answer_match_left]"] = left.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)
        data[f"question[answers][{i}][answer_match_right]"] = right.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)

        if ((left.feedback is not None) and (left.feedback.general is not None)):
            data[f"question[answers][{i}][answer_comment_html]"] = left.feedback.general.to_canvas()

    if (len(answers.distractors) > 0):
        distractors = [
            distractor.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)
            for distractor
            in answers.distractors
        ]
        data["question[matching_answer_incorrect_matches]"] = "\n".join(distractors)

def _serialize_mdd_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.MultiplePartChoiceAnswers,
        ) -> None:
    """ Serialize MDD answers. """

    index = 0

    for (key, choices) in answers.parts.items():
        _serialize_choice_answers(data, choices, True, blank_id = key, start_index = index)
        index += len(choices.choices)

def _serialize_numeric_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.NumericAnswers,
        ) -> None:
    """ Serialize numeric answers. """

    # Note that the keys/constants for numerical answers are different than what the documentation says:
    # https://canvas.instructure.com/doc/api/quiz_questions.html#QuizQuestion

    for (i, option) in enumerate(answers.options):
        data[f"question[answers][{i}][answer_weight]"] = 100
        data[f"question[answers][{i}][numerical_answer_type]"] = option.type.value + '_answer'

        if (option.type is quizcomp.model.answer.NumericAnswerType.EXACT):
            data[f"question[answers][{i}][answer_exact]"] = option.value
            data[f"question[answers][{i}][answer_error_margin]"] = option.margin
        elif (option.type is quizcomp.model.answer.NumericAnswerType.RANGE):
            data[f"question[answers][{i}][answer_range_start]"] = option.min
            data[f"question[answers][{i}][answer_range_end]"] = option.max
        elif (option.type is quizcomp.model.answer.NumericAnswerType.PRECISION):
            data[f"question[answers][{i}][answer_approximate]"] = option.value
            data[f"question[answers][{i}][answer_precision]"] = option.precision
        else:
            raise ValueError(f"Unknown numerical option type: '{option.type.value}'.")

        if ((option.feedback is not None) and (option.feedback.general is not None)):
            data[f"question[answers][{i}][answer_comment_html]"] = option.feedback.general.to_canvas()

def _upload_quiz_images(
        backend: typing.Any,
        course_id: int,
        quiz: quizcomp.model.quiz.Quiz,
        ) -> None:
    """ Upload quiz images. """

    parent_dir_id = None

    for document in quiz.collect_all_documents():
        for image_token in document.collect_images():
            source = image_token.attrGet('src')
            if (source is None):
                continue

            # Skip remote images.
            if (re.match(r'^http(s)?://', source)):
                continue

            path = source
            if (not os.path.isabs(path)):
                path = os.path.join(document.context.base_dir, path)

            path = os.path.abspath(path)
            if (not os.path.isfile(path)):
                raise ValueError(f"Found an image within the quiz that does not exist on disk: '{path}' ('{source}').")

            # Get a hash of the original source to avoid name conflicts.
            source_hash = edq.util.hash.sha256_hex(source)

            (basename, ext) = os.path.splitext(os.path.basename(path))
            canvas_filename = f"{basename}_{source_hash}{ext}"

            # For a specific path for this object within the canvas course.
            canvas_path = '/'.join([
                CANVAS_QUIZCOMP_BASEDIR,
                CANVAS_QUIZCOMP_QUIZ_DIRNAME,
                quiz.name,
                canvas_filename,
            ])

            image_token.attrSet('original_src', source)
            image_token.attrSet('src', canvas_path)

            # Ensure that a parent directory exists for these quiz resources.
            if (parent_dir_id is None):
                parent_dir_id = _ensure_folder(backend, course_id, os.path.dirname(canvas_path))

            _upload_file(backend, course_id, path, parent_dir_id, canvas_path)

def _restore_image_sources(quiz: quizcomp.model.quiz.Quiz) -> None:
    """ Replace any modified image sources with their original source. """

    for document in quiz.collect_all_documents():
        for image_token in document.collect_images():
            original_source = image_token.attrGet('original_src')
            if (original_source is None):
                continue

            image_token.attrSet('src', str(original_source))
            image_token.attrs.pop('original_src', None)

def _ensure_folder(
        backend: typing.Any,
        course_id: int,
        canvas_path: str,
        ) -> int:
    """ Ensure that a Canvas folder exists and fetch its ID. """

    folder_id = _get_folder(backend, course_id, canvas_path)
    if (folder_id is not None):
        return folder_id

    folder_id = _create_folder(backend, course_id, canvas_path)

    # Canvas will not hide created parents.
    _hide_folder(backend, course_id, CANVAS_QUIZCOMP_BASEDIR)

    return folder_id

def _get_folder(
        backend: typing.Any,
        course_id: int,
        canvas_path: str,
        ) -> typing.Union[int, None]:
    """ Get a Canvas folder ID (if it exists). """

    url = backend.server + GET_FOLDER_ENDPOINT.format(course_id = course_id, canvas_path = canvas_path)
    headers = backend.get_standard_headers()

    raw_object = lms.backend.canvas.common.make_get_request(url, headers = headers)
    if ((raw_object is None) or (len(raw_object) == 0)):
        return None

    return int(raw_object[-1]['id'])

def _create_folder(
        backend: typing.Any,
        course_id: int,
        canvas_path: str,
        ) -> int:
    """ Create a folder in Canvas. """

    name = os.path.basename(canvas_path)
    parent_path = os.path.dirname(canvas_path)

    data = {
        'name': name,
        'parent_folder_path': parent_path,
        # Canvas wants a string here despite the documentation saying it is a bool.
        'hidden': 'true',
    }

    url = backend.server + CREATE_FOLDER_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_object = typing.cast(typing.Dict[str, typing.Any],
            lms.backend.canvas.common.make_post_request(url, headers = headers, data = data, raise_on_404 = True))
    return int(raw_object['id'])

def _hide_folder(
        backend: typing.Any,
        course_id: int,
        canvas_path: str,
        ) -> None:
    """ Ensure that a Canvas folder (specified by path) is hidden. """

    folder_id = _get_folder(backend, course_id, canvas_path)
    if (folder_id is None):
        raise ValueError(f"Could not find Canvas folder to hide: '{canvas_path}'.")

    data = {
        # Canvas wants a string here despite the documentation saying it is a bool.
        'hidden': 'true',
    }

    url = backend.server + HIDE_FOLDER_ENDPOINT.format(folder_id = folder_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    lms.backend.canvas.common.make_put_request(url, headers = headers, data = data, raise_on_404 = True)

def _upload_file(
        backend: typing.Any,
        course_id: int,
        path: str,
        parent_dir_id: int,
        canvas_path: str,
        ) -> int:
    """ Upload a file to the specified Canvas path. """

    upload_url, upload_params = _init_file_upload(backend, course_id, path, parent_dir_id, canvas_path)
    return _upload_file_contents(backend, path, upload_url, upload_params)

def _init_file_upload(
        backend: typing.Any,
        course_id: int,
        path: str,
        parent_dir_id: int,
        canvas_path: str,
        ) -> typing.Tuple[str, typing.Dict[str, typing.Any]]:
    """
    Prepare to upload a file to Canvas.
    Return the Canvas-returned upload URL and upload params.
    """

    data = {
        'name': os.path.basename(canvas_path),
        'size': os.stat(path).st_size,
        'parent_folder_id': parent_dir_id,
        'on_duplicate': 'overwrite',
    }

    url = backend.server + UPLOAD_FILE_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_object = typing.cast(typing.Dict[str, typing.Any],
            lms.backend.canvas.common.make_post_request(url, headers = headers, data = data))

    return (raw_object['upload_url'], raw_object['upload_params'])

def _upload_file_contents(
        backend: typing.Any,
        path: str,
        upload_url: str,
        upload_params: typing.Dict[str, typing.Any],
        ) -> int:
    """ Upload the actual file contents to Canvas. """

    files = {
        'file': open(path, 'rb'),  # pylint: disable=consider-using-with
    }

    headers = backend.get_standard_headers()
    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_object = typing.cast(typing.Dict[str, typing.Any],
            lms.backend.canvas.common.make_post_request(upload_url, headers = headers, data = upload_params, files = files))
    return int(raw_object['id'])
