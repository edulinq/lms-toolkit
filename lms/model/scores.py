import typing

import edq.util.json
import edq.util.time

import lms.model.assignments
import lms.model.base
import lms.model.users

class ScoreFragment(edq.util.json.DictConverter):
    """ A small subset of information about a score. """

    def __init__(self,
            score: typing.Union[float, None] = None,
            comment: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        self.score: typing.Union[float, None] = score
        """
        The numeric score.
        A None value indicates that the score should be cleared.
        """

        self.comment: typing.Union[str, None] = comment
        """ An optional comment for this score. """

class AssignmentScore(lms.model.base.BaseType):
    """
    The score assignment to a student for an assignment (or scorable object).
    """

    CORE_FIELDS = [
        'id', 'user_query', 'assignment_query', 'score', 'submission_date', 'graded_date', 'comment',
    ]

    def __init__(self,
            id: typing.Union[str, None] = None,
            score: typing.Union[float, None] = None,
            submission_date: typing.Union[edq.util.time.Timestamp, None] = None,
            graded_date: typing.Union[edq.util.time.Timestamp, None] = None,
            comment: typing.Union[str, None] = None,
            assignment_query: typing.Union[lms.model.assignments.AssignmentQuery, None] = None,
            user_query: typing.Union[lms.model.users.UserQuery, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this score. """

        self.assignment_query: typing.Union[lms.model.assignments.AssignmentQuery, None] = assignment_query
        """ The assignment associated with this score. """

        self.user_query: typing.Union[lms.model.users.UserQuery, None] = user_query
        """ The user associated with this score. """

        self.score: typing.Union[float, None] = score
        """ The assignment score. """

        self.submission_date: typing.Union[edq.util.time.Timestamp, None] = submission_date
        """ The datetime that the submission that received this score was submitted. """

        self.graded_date: typing.Union[edq.util.time.Timestamp, None] = graded_date
        """ The datetime that the submission that received this score was graded. """

        self.comment: typing.Union[str, None] = comment
        """ A comment attached to this score. """

    def to_fragment(self) -> ScoreFragment:
        """ Get a score fragment from this assignment score. """

        return ScoreFragment(score = self.score, comment = self.comment)

class Gradebook(lms.model.base.BaseType):
    """
    A gradebook that contains scores for a set of users and assignments.
    """

    CORE_FIELDS = [
        'assignments', 'users', '_entries',
    ]

    def __init__(self,
            assignments: typing.List[lms.model.assignments.AssignmentQuery],
            users: typing.List[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.assignments: typing.List[lms.model.assignments.AssignmentQuery] = assignments
        """ The assignments represented in this gradebook. """

        self.users: typing.List[lms.model.users.UserQuery] = users
        """ The users represented in this gradebook. """

        self._entries: typing.Dict[str, AssignmentScore] = {}
        """ The scores held by this gradebook. """

    def _make_key(self, assignment_query: lms.model.assignments.AssignmentQuery, user_query: lms.model.users.UserQuery) -> str:
        """ Create a key for this gradebook entry. """

        return f"{assignment_query.id}::{user_query.id}"

    def get(self,
            assignment_query: lms.model.assignments.AssignmentQuery,
            user_query: lms.model.users.UserQuery,
            ) -> typing.Union[AssignmentScore, None]:
        """ Get the target gradebook entry. """

        found_assignment = None
        for assignment in self.assignments:
            if (assignment.match(assignment_query)):
                found_assignment = assignment
                break

        if (found_assignment is None):
            return None

        found_user = None
        for user in self.users:
            if (user.match(user_query)):
                found_user = user
                break

        if (found_user is None):
            return None

        return self._entries.get(self._make_key(found_assignment, found_user), None)

    def get_scores_by_assignment(self,
            ) -> typing.Dict[
                lms.model.assignments.AssignmentQuery,
                typing.Dict[lms.model.users.UserQuery, AssignmentScore]]:
        """ Get all entries indexed by assignment. """

        results: typing.Dict[
                lms.model.assignments.AssignmentQuery,
                typing.Dict[lms.model.users.UserQuery, AssignmentScore]] = {}

        for assignment in self.assignments:
            results[assignment] = {}

            for user in self.users:
                key = self._make_key(assignment, user)
                if (key not in self._entries):
                    continue

                results[assignment][user] = self._entries[key]

        return results

    def add(self, score: AssignmentScore) -> None:
        """
        Add the score to this gradebook.
        If the user or assignment is not already in this gradebook, raise an exception.

        The gradebook takes ownership of the score.
        """

        found_assignment = None
        for assignment in self.assignments:
            if (assignment.match(score.assignment_query)):
                found_assignment = assignment
                break

        if (found_assignment is None):
            raise ValueError(f"Could not match gradebook assignment to score's assignment '{score.assignment_query}'.")

        found_user = None
        for user in self.users:
            if (user.match(score.user_query)):
                found_user = user
                break

        if (found_user is None):
            raise ValueError(f"Could not match gradebook user to score's user '{score.user_query}'.")

        # Update the score's queries.
        score.assignment_query = found_assignment
        score.user_query = found_user

        self._entries[self._make_key(found_assignment, found_user)] = score

    def update_queries(self,
            assignment_queries: typing.List[lms.model.assignments.ResolvedAssignmentQuery],
            user_queries: typing.List[lms.model.users.ResolvedUserQuery],
            ) -> None:
        """ Update any assignment/user queries with the supplied ones (matching on ID). """

        assignment_map = {query.id: query for query in assignment_queries}
        user_map = {query.id: query for query in user_queries}

        self.assignments = [assignment_map.get(assignment.id, assignment) for assignment in self.assignments]
        self.users = [user_map.get(user.id, user) for user in self.users]

        for score in self._entries.values():
            if (score.assignment_query is not None):
                score.assignment_query = assignment_map.get(score.assignment_query.id, score.assignment_query)

            if (score.user_query is not None):
                score.user_query = user_map.get(score.user_query.id, score.user_query)

    def as_text_rows(self,
            skip_headers: bool = False,
            pretty_headers: bool = False,
            separator: str = ': ',
            empty_value: str = '',
            **kwargs: typing.Any) -> typing.List[str]:
        rows: typing.List[str] = []
        for user in sorted(self.users):
            # Add in a user separator.
            if (len(rows) > 0):
                rows.append('')

            rows.append(f"User{separator}{user}")

            for assignment in sorted(self.assignments):
                score = self.get(assignment, user)

                text = empty_value
                if (score is not None):
                    text = str(score.score)

                rows.append(f"{assignment}{separator}{text}")

        return rows

    def get_headers(self,
            pretty_headers: bool = False,
            **kwargs: typing.Any) -> typing.List[str]:
        return ['User'] + [str(query) for query in sorted(self.assignments)]

    def as_table_rows(self,
            empty_value: str = '',
            **kwargs: typing.Any) -> typing.List[typing.List[str]]:
        rows = []
        for user in sorted(self.users):
            row = [str(user)]
            for assignment in sorted(self.assignments):
                score = self.get(assignment, user)

                text = empty_value
                if (score is not None):
                    text = str(score.score)

                row.append(text)

            rows.append(row)

        return rows

    def as_json_dict(self,
        include_extra_fields: bool = False,
            **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        """
        Get a dict representation of this object meant for display as JSON.
        (Note that we are not returning JSON, just a dict that is ready to be converted to JSON.)
        Calling this method differs from passing this object to json.dumps() (or any sibling),
        because this method may not include all fields, may flatten or alter fields, and will order fields differently.
        """

        scores = []
        for assignment in sorted(self.assignments):
            row = []
            for user in sorted(self.users):
                score: typing.Any = self.get(assignment, user)
                if (score is not None):
                    score = score.as_json_dict(include_extra_fields = include_extra_fields, **kwargs)

                row.append(score)

            scores.append(row)

        return {
            'assignments': self.assignments,
            'users': self.users,
            'scores_assignment_user': scores,
        }

    def __len__(self) -> int:
        return len(self._entries)
