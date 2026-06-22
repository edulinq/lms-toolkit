import typing

import quizcomp.model.answer
import quizcomp.model.config
import quizcomp.model.group
import quizcomp.model.question
import quizcomp.model.quiz

# TEST
import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.constants
import lms.model.quizzes

LIST_ASSIGNMENT_GROUPS_ENDPOINT: str = "/api/v1/courses/{course_id}/assignment_groups?per_page={page_size}"
UPLOAD_GROUP_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/groups"
UPLOAD_QUESTION_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes/{quiz_id}/questions"
UPLOAD_QUIZ_METADATA_ENDPOINT: str = "/api/v1/courses/{course_id}/quizzes"

# TEST
BASE_ENDPOINT = "/api/v1/courses/{course_id}/quizzes"

# TEST - Assignment Group

# TEST - Quiz type

# TEST - Return Quiz Metadata

QUIZ_TYPE_ASSIGNMENT: str = 'assignment'
QUIZ_TYPE_PRACTICE: str = 'practice_quiz'

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
        ) -> lms.model.quizzes.QuizMetadata:
    """
    Upload a quiz.

    This is a process that takes many steps.
     1) Upload Quiz Files
     2) Upload Quiz Metadata
     3) Upload Quiz Question Groups (first create question groups and then upload questions).
    """

    # TEST
    _upload_quiz_files(backend, course_id, quiz)

    assignment_group_id = _fetch_assignment_group(backend, course_id, quiz)

    quiz_metadata = _upload_quiz_metadata(backend, course_id, quiz, assignment_group_id)

    for group in quiz.get_groups():
        _upload_group(backend, course_id, int(quiz_metadata.id), group)

    return quiz_metadata

def _upload_quiz_files(
        backend: typing.Any,
        course_id: int,
        quiz: quizcomp.model.quiz.Quiz,
        ) -> None:
    """ Upload quiz files (like images). """

    # TEST

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
        ) -> lms.model.quizzes.QuizMetadata:
    """ Upload the base quiz metadata, which we can then attach questions to. """

    quiz_type = QUIZ_TYPE_ASSIGNMENT
    if ((quiz.practice is None) or (quiz.practice is True)):
        quiz_type = QUIZ_TYPE_PRACTICE

    description = quiz.description.to_canvas()
    if (quiz.version is not None):
        description = f"<p>{description}</p><br /><hr /><p>Version: {quiz.version}</p>"

    raw_hide_results = None
    if (quiz.hide_results is not None):
        if (hide_results is not quizcomp.model.quiz.HideResultsBehavior.NEVER_HIDE):
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
        # TEST - Previous version did a str() and lower() on this.
        'quiz[show_correct_answers]': quiz.show_correct_answers,
        'quiz[hide_results]': raw_hide_results,
        # TEST - Previous version did a str() and lower() on this.
        'quiz[shuffle_answers]': quiz.get_config(quizcomp.model.config.OPTION_SHUFFLE_ANSWERS),
        'quiz[scoring_policy]': raw_scoring_policy,
    }

    url = backend.server + UPLOAD_QUIZ_METADATA_ENDPOINT.format(course_id = course_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    raw_data = lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)

    return lms.model.quizzes.QuizMetadata(id = str(raw_data['id']), name = quiz.get_name())

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

    raw_data = lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)

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

    # TEST
    print('---')
    import edq.util.json
    print(edq.util.json.dumps(data, indent = 4))
    print('---')

    lms.backend.canvas.common.make_post_request(url, headers = headers, data = data)

    # TEST
    print('TEST - Success')

def _create_question_json(
        group_id: int,
        question: quizcomp.model.question.Question,
        index: int,
        ) -> typing.Dict[str, typing.Any]:
    """ Create a dict that represent a question for a Canvas API request. """

    question_type = QUESTION_TYPE_MAP[question.question_type]

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

    if (isinstance(question.answers, quizcomp.model.answer.ChoiceAnswers)):
        _serialize_choice_answers(data, question.answers, False)
    else:
        raise ValueError(f"Unknown answers type '{type(question.answers)}' for question type '{question.question_type.value}'.")

    ''' TEST
    if (question.question_type in [quizcomp.model.constants.QuestionType.ESSAY, quizcomp.model.constants.QuestionType.SA]):
        # In Canvas, short answer questions also get mapped to the essay Canvas type.
        # Essay questions have no answers.
        pass
    elif (question.question_type == quizcomp.model.constants.QuestionType.FIMB):
        _serialize_fimb_answers(data, question, instance)
    elif (question.question_type == quizcomp.model.constants.QuestionType.FITB):
        _serialize_fimb_answers(data, question, instance)
    elif (question.question_type == quizcomp.model.constants.QuestionType.MATCHING):
        _serialize_matching_answers(data, question, instance)
    elif (question.question_type == quizcomp.model.constants.QuestionType.NUMERICAL):
        _serialize_numeric_answers(data, question.answers, instance)
    elif (question.question_type == quizcomp.model.constants.QuestionType.TEXT_ONLY):
        # Text-Only questions have no answers.
        pass
    elif (isinstance(question.answers, list)):
        use_text = (question.question_type == quizcomp.model.constants.QuestionType.TF)
        _serialize_answer_list(data, question.answers, instance, use_text = use_text)
    elif (isinstance(question.answers, dict)):
        count = 0
        for key, item in question.answers.items():
            _serialize_answer_list(data, item['values'], instance,
                    start_index = count, blank_id = key, use_text = True)
            count += len(item['values'])
    else:
        raise ValueError(f"Unknown answers type '{type(question.answers)}'.")
    '''

def _serialize_choice_answers(
        data: typing.Dict[str, typing.Any],
        answers: quizcomp.model.answer.ChoiceAnswers,
        use_text: bool,
        blank_id: typing.Union[str, None] = None,
        ) -> None:
    """ Serialize choice-based answers. """

    for (i, choice) in enumerate(answers.choices):
        weight = 0
        if (choice.correct):
            weight = 100

        data[f"question[answers][{i}][answer_weight]"] = weight

        if (use_text):
            text = choice.text.to_text(text_allow_special_text = True, text_allow_all_characters = True)
            data[f"question[answers][{i}][answer_text]"] = text
        else:
            html = choice.text.to_canvas()
            data[f"question[answers][{i}][answer_html]"] = html

        if (blank_id is not None):
            data[f"question[answers][{i}][blank_id]"] = blank_id

        if ((choice.feedback is not None) and (choice.feedback.general is not None)):
            data[f"question[answers][{i}][answer_comment_html]"] = choice.feedback.general.to_canvas()










# TEST

def _serialize_answer_list(
        data: typing.Dict[str, typing.Any],
        answers: typing.List[typing.Any],
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        start_index: int = 0,
        blank_id: typing.Union[str, None] = None,
        use_text: bool = False,
        ) -> None:
    """ Clean a list of answers for Canvas. """

    for (i, answer) in enumerate(answers):
        _serialize_answer(data, answer, start_index + i, instance,
            blank_id = blank_id, use_text = use_text)

def _serialize_answer(
        data: typing.Dict[str, typing.Any],
        answer: typing.Any,
        index: int,
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        blank_id: typing.Union[str, None] = None,
        use_text: bool = False,
        ) -> None:
    """ Clean answer data for Canvas. """

    weight = 0
    if (answer.is_correct()):
        weight = 100

    data[f"question[answers][{index}][answer_weight]"] = weight

    if (use_text):
        text = answer.document.to_text(text_allow_special_text = True, text_allow_all_characters = True)
        data[f"question[answers][{index}][answer_text]"] = text
    else:
        html = answer.document.to_canvas(canvas_instance = instance, pretty = False)
        data[f"question[answers][{index}][answer_html]"] = html

    if (blank_id is not None):
        data[f"question[answers][{index}][blank_id]"] = blank_id

    if (answer.feedback is not None):
        feedback_html = answer.feedback.document.to_canvas(canvas_instance = instance, pretty = False)
        data[f"question[answers][{index}][answer_comment_html]"] = feedback_html

def _serialize_matching_answers(
        data: typing.Dict[str, typing.Any],
        question: quizcomp.model.question.Question,
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        ) -> None:
    """ Concert the answers for a matching-type question to Canvas API data. """

    for i in range(len(question.answers['matches'])):
        left_content = question.answers['matches'][i]['left'].document.to_text(text_allow_special_text = True, text_allow_all_characters = True)
        right_content = question.answers['matches'][i]['right'].document.to_text(text_allow_special_text = True, text_allow_all_characters = True)

        data[f"question[answers][{i}][answer_match_left]"] = left_content
        data[f"question[answers][{i}][answer_match_right]"] = right_content

        if (question.answers['matches'][i]['left'].feedback is not None):
            text = question.answers['matches'][i]['left'].feedback.document.to_canvas(canvas_instance = instance, pretty = False)
            data[f"question[answers][{i}][answer_comment_html]"] = text

    if (len(question.answers['distractors']) > 0):
        distractors = [
            distractor.document.to_text(text_allow_special_text = True, text_allow_all_characters = True)
            for distractor
            in question.answers['distractors']
        ]
        data["question[matching_answer_incorrect_matches]"] = "\n".join(distractors)

def _serialize_fimb_answers(
        data: typing.Dict[str, typing.Any],
        question: quizcomp.model.question.Question,
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        ) -> None:
    """ Concert the answers for a FIMB-type question to Canvas API data. """

    index = 0

    for item in question.answers.values():
        key_text = item['key'].document.to_text()

        for i in range(len(item['values'])):
            value_text = item['values'][i].document.to_text(text_allow_special_text = True, text_allow_all_characters = True)

            data[f"question[answers][{index}][blank_id]"] = key_text
            data[f"question[answers][{index}][answer_weight]"] = 100
            data[f"question[answers][{index}][answer_text]"] = value_text

            if (item['values'][i].feedback is not None):
                feedback_text = item['values'][i].feedback.document.to_canvas(canvas_instance = instance, pretty = False)
                data[f"question[answers][{index}][answer_comment_html]"] = feedback_text

            index += 1

def _serialize_numeric_answers(
        data: typing.Dict[str, typing.Any],
        answers: typing.List[typing.Any],
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        ) -> None:
    """ Concert the answers for a numeric-type question to Canvas API data. """

    # Note that the keys/constants for numerical answers are different than what the documentation says:
    # https://canvas.instructure.com/doc/api/quiz_questions.html#QuizQuestion

    for (i, answer) in enumerate(answers):
        data[f"question[answers][{i}][answer_weight]"] = 100
        data[f"question[answers][{i}][numerical_answer_type]"] = answer.type + '_answer'

        if (answer.type == quizcomp.model.answer.NumericAnswerType.EXACT):
            data[f"question[answers][{i}][answer_exact]"] = answer.value
            data[f"question[answers][{i}][answer_error_margin]"] = answer.margin
        elif (answer.type == quizcomp.model.answer.NumericAnswerType.RANGE):
            data[f"question[answers][{i}][answer_range_start]"] = answer.min
            data[f"question[answers][{i}][answer_range_end]"] = answer.max
        elif (answer.type == quizcomp.model.answer.NumericAnswerType.PRECISION):
            data[f"question[answers][{i}][answer_approximate]"] = answer.value
            data[f"question[answers][{i}][answer_precision]"] = answer.precision
        else:
            raise ValueError(f"Unknown numerical answer type: '{answer.type}'.")

        if (answer.feedback is not None):
            feedback_text = answer.feedback.document.to_canvas(canvas_instance = instance, pretty = False)
            data[f"question[answers][{i}][answer_comment_html]"] = feedback_text

def upload_file(path: str, canvas_path: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> str:
    """ Upload a file to Canvas and fetch its ID. """

    parent_id = ensure_folder(os.path.dirname(canvas_path), instance)
    upload_url, upload_params = _init_file_upload(path, canvas_path, parent_id, instance)
    file_id = _upload_file_contents(path, upload_url, upload_params)

    return file_id

def _init_file_upload(
        path: str,
        canvas_path: str,
        parent_id: str,
        instance: quizcomp.uploader.instance.CanvasInstanceInfo,
        ) -> typing.Tuple[str, typing.Dict[str, typing.Any]]:
    """ Prepare to upload a file to Canvas. """

    canvas_name = os.path.basename(canvas_path)

    size = os.stat(path).st_size

    data = {
        'name': canvas_name,
        'size': size,
        'parent_folder_id': parent_id,
        'on_duplicate': 'overwrite',
    }

    response = requests.request(
        method = "POST",
        url = f"{instance.base_url}/api/v1/courses/{instance.course_id}/files",
        headers = instance.base_headers(),  # type: ignore[arg-type]
        data = data)
    response.raise_for_status()

    response = response.json()

    upload_url = response['upload_url']
    upload_params = response['upload_params']

    return upload_url, upload_params

def _upload_file_contents(path: str, upload_url: str, upload_params: typing.Dict[str, typing.Any]) -> str:
    """ Upload the actual file contents to Canvas. """

    files = {
        'file': open(path, 'rb'),  # pylint: disable=consider-using-with
    }

    response = requests.request(
        method = "POST",
        url = upload_url,
        data = upload_params,
        files = files)
    response.raise_for_status()

    file_id = None

    location = response.headers.get('Location', None)
    if (location is not None):
        file_id = os.path.basename(urllib.parse.urlparse(location).path)
    else:
        # The location was not present in the header, check for a JSON body.
        try:
            body = response.json()
            file_id = str(body['id'])
        except Exception:
            pass

    if (file_id is None):
        raise ValueError(f"Could not find id for uploaded file in response from Canvas: '{path}'.")

    return str(file_id)

def ensure_folder(canvas_path: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> str:
    """ Ensure that a Canvas folder exists and fetch its ID. """

    folder_id = get_folder(canvas_path, instance)
    if (folder_id is not None):
        return folder_id

    folder_id = create_folder(canvas_path, instance)

    # Canvas will not hide created parents.
    hide_folder(CANVAS_QUIZCOMP_BASEDIR, instance)

    return folder_id

def get_folder(canvas_path: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> typing.Union[str, None]:
    """ Get a Canvas folder ID (if it exists). """

    # The canvas path should be absolute.
    response = requests.request(
        method = "GET",
        url = f"{instance.base_url}/api/v1/courses/{instance.course_id}/folders/by_path{canvas_path}",
        headers = instance.base_headers())  # type: ignore[arg-type]

    if (response.status_code == 404):
        return None

    response.raise_for_status()

    return str(response.json()[-1]['id'])

def create_folder(canvas_path: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> str:
    """ Create a folder in Canvas. """

    name = os.path.basename(canvas_path)
    parent_path = os.path.dirname(canvas_path)

    data = {
        'name': name,
        'parent_folder_path': parent_path,
        # Canvas wants a string here despite the documentation saying it is a bool.
        'hidden': 'true',
    }

    response = requests.request(
        method = "POST",
        url = f"{instance.base_url}/api/v1/courses/{instance.course_id}/folders",
        headers = instance.base_headers(),  # type: ignore[arg-type]
        data = data)
    response.raise_for_status()

    return str(response.json()['id'])

def hide_folder(canvas_path: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> None:
    """ Ensure that a Canvas folder (specified by path) is hidden. """

    folder_id = get_folder(canvas_path, instance)
    if (folder_id is None):
        raise ValueError(f"Could not find Canvas folder to hide: '{canvas_path}'.")

    hide_folder_id(folder_id, instance)

def hide_folder_id(folder_id: str, instance: quizcomp.uploader.instance.CanvasInstanceInfo) -> None:
    """ Ensure that a Canvas folder (specified by ID) is hidden. """

    data = {
        # Canvas wants a string here despite the documentation saying it is a bool.
        # TODO(eriq): Make a bug request?
        'hidden': 'true',
    }

    response = requests.request(
        method = "PUT",
        url = f"{instance.base_url}/api/v1/folders/{folder_id}",
        headers = instance.base_headers(),  # type: ignore[arg-type]
        data = data)
    response.raise_for_status()
