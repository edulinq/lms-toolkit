import logging
import re
import typing

import lms.model.assignments
import lms.model.scores
import lms.model.users

T = typing.TypeVar('T')

class APIBackend():
    """
    API backends provide a unified interface to an LMS.

    Note that instead of using an abstract class,
    methods will raise a NotImplementedError by default.
    This will allow child backends to fill in as much functionality as they can,
    while still leaving gaps where they are incomplete or impossible.
    """

    def __init__(self,
            server: str,
            **kwargs: typing.Any) -> None:
        self.server: str = server
        """ The server this backend will connect to. """

    # Core Methods

    def not_found(self, label: str, identifiers: typing.Dict[str, typing.Any]) -> None:
        """
        Called when the backend was unable to find some object.
        This will only be called when a requested object is not found,
        e.g., a user requested by ID is not found.
        This is not called when a list naturally returns zero results,
        or when a query does not match any items.
        """

        logging.warning("Object not found: '%s'. Identifiers: %s.", label, identifiers)

    # API Methods

    def courses_assignments_get(self,
            course_id: str,
            assignment_queries: typing.List[lms.model.assignments.AssignmentQuery],
            **kwargs: typing.Any) -> typing.Sequence[lms.model.assignments.Assignment]:
        """
        Get the specified assignments associated with the given course.
        """

        if (len(assignment_queries) == 0):
            return []

        # Check if at least one of the queries requires resolution.
        # If resolution is required, then just list the assignments and match the queries.
        if (any(query.requires_resolution() for query in assignment_queries)):
            return self.courses_assignments_resolve_and_list(course_id, assignment_queries, **kwargs)

        # If there are multiple queries, then just list the assignments and match the queries.
        if (len(assignment_queries) > 1):
            return self.courses_assignments_resolve_and_list(course_id, assignment_queries, **kwargs)

        # If there is just one query, then fetch it.
        result = self.courses_assignments_fetch(course_id, typing.cast(str, assignment_queries[0].id), **kwargs)
        if (result is None):
            return []

        return [result]

    def courses_assignments_fetch(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.assignments.Assignment, None]:
        """
        Fetch a single assignment associated with the given course.
        Return None if no matching assignment is found.
        """

        raise NotImplementedError('courses_assignments_fetch')

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.assignments.Assignment]:
        """
        Get the assignments associated with the given course.
        """

        raise NotImplementedError('courses_assignments_list')

    def courses_assignments_resolve_and_list(self,
            course_id: str,
            assignment_queries: typing.List[lms.model.assignments.AssignmentQuery],
            **kwargs: typing.Any) -> typing.Sequence[lms.model.assignments.Assignment]:
        """
        List the course assignments and then match the given queries.
        """

        assignments = self.courses_assignments_list(course_id, **kwargs)

        matches = []
        for assignment in assignments:
            for query in assignment_queries:
                if (query.match(assignment)):
                    matches.append(assignment)
                    break

        return matches

    def courses_assignments_scores_get(self,
            course_id: str,
            assignment_query: lms.model.assignments.AssignmentQuery,
            user_queries: typing.List[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> typing.Sequence[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given assignment query and user queries.
        """

        if (len(user_queries) == 0):
            return []

        scores = self.courses_assignments_scores_resolve_and_list(course_id, assignment_query)

        matches = []
        for score in scores:
            for user_query in user_queries:
                if (user_query.match(score.user_query)):
                    matches.append(score)

        return matches

    def courses_assignments_scores_fetch(self,
            course_id: str,
            assignment_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.scores.AssignmentScore, None]:
        """
        List the score associated with the given assignment and user.
        """

        raise NotImplementedError('courses_assignments_scores_fetch')

    def courses_assignments_scores_list(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given assignment.
        """

        raise NotImplementedError('courses_assignments_scores_list')

    def courses_assignments_scores_resolve_and_list(self,
            course_id: str,
            assignment_query: lms.model.assignments.AssignmentQuery,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given assignment query.
        In addition to resolving the assignment query,
        users will also be resolved into their full version
        (instead of the reduced version usually returned with scores).
        """

        matched_assignments = self.courses_assignments_get(course_id, [assignment_query], **kwargs)
        if (len(matched_assignments) == 0):
            return []

        target_assignment = matched_assignments[0]

        scores = self.courses_assignments_scores_list(course_id, target_assignment.id, **kwargs)
        if (len(scores) == 0):
            return []

        users = self.courses_users_list(course_id, **kwargs)
        users_map = {user.id: user for user in users}

        for score in scores:
            score.assignment_query = target_assignment.to_query()

            if ((score.user_query is not None) and (score.user_query.id in users_map)):
                score.user_query = users_map[score.user_query.id].to_query()

        return scores

    def courses_users_get(self,
            course_id: str,
            user_queries: typing.List[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> typing.Sequence[lms.model.users.CourseUser]:
        """
        Get the specified users associated with the given course.
        """

        if (len(user_queries) == 0):
            return []

        # Check if at least one of the queries requires resolution.
        # If resolution is required, then just list the users and match the queries.
        if (any(query.requires_resolution() for query in user_queries)):
            return self.courses_users_resolve_and_list(course_id, user_queries, **kwargs)

        # If there are multiple queries, then just list the users and match the queries.
        if (len(user_queries) > 1):
            return self.courses_users_resolve_and_list(course_id, user_queries, **kwargs)

        # If there is just one query, then fetch it.
        result = self.courses_users_fetch(course_id, typing.cast(str, user_queries[0].id), **kwargs)
        if (result is None):
            return []

        return [result]

    def courses_users_fetch(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.users.CourseUser, None]:
        """
        Fetch a single user associated with the given course.
        Return None if no matching user is found.
        """

        raise NotImplementedError('courses_users_fetch')

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Sequence[lms.model.users.CourseUser]:
        """
        Get the users associated with the given course.
        """

        raise NotImplementedError('courses_users_list')

    def courses_users_resolve_and_list(self,
            course_id: str,
            user_queries: typing.List[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> typing.Sequence[lms.model.users.CourseUser]:
        """
        List the course users and then match the given queries.
        """

        users = self.courses_users_list(course_id, **kwargs)

        matches = []
        for user in users:
            for query in user_queries:
                if (query.match(user)):
                    matches.append(user)
                    break

        return matches

    # Utility Methods

    def parse_assignment_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.assignments.AssignmentQuery, None]:
        """
        Attempt to parse an assignment query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return self._parse_int_query(lms.model.assignments.AssignmentQuery, text, check_email = False)

    def parse_assignment_queries(self, texts: typing.List[typing.Union[str, None]]) -> typing.List[lms.model.assignments.AssignmentQuery]:
        """ Parse a list of assignment queries. """

        queries = []
        for text in texts:
            query = self.parse_assignment_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def parse_user_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.users.UserQuery, None]:
        """
        Attempt to parse a user query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return self._parse_int_query(lms.model.users.UserQuery, text, check_email = True)

    def parse_user_queries(self, texts: typing.List[typing.Union[str, None]]) -> typing.List[lms.model.users.UserQuery]:
        """ Parse a list of user queries. """

        queries = []
        for text in texts:
            query = self.parse_user_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def _parse_int_query(self, query_type: typing.Type[T], text: typing.Union[str, None],
            check_email: bool = True,
            ) -> typing.Union[T, None]:
        """
        Parse a query with the assumption that LMS ids are ints.

        Accepts queries are in the following forms:
         - LMS ID (`id`)
         - Email (`email`)
         - Full Name (`name`)
         - f"{email} ({id})"
         - f"{name} ({id})"
        """

        if (text is None):
            return None

        # Clean whitespace.
        text = re.sub(r'\s+', ' ', str(text)).strip()
        if (len(text) == 0):
            return None

        id = None
        email = None
        name = None

        match = re.search(r'^(\S.*)\((\d+)\)$', text)
        if (match is not None):
            # Query has both text and id.
            name = match.group(1).strip()
            id = match.group(2)
        elif (re.search(r'^\d+$', text) is not None):
            # Query must be an ID.
            id = text
        else:
            name = text

        # Check if the name is actually an email address.
        if (check_email and (name is not None) and ('@' in name)):
            email = name
            name = None

        data = {
            'id': id,
            'name': name,
            'email': email,
        }

        return query_type(**data)
