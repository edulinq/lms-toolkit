import logging
import typing

import edq.util.parse

import lms.model.assignments
import lms.model.constants
import lms.model.courses
import lms.model.groups
import lms.model.groupsets
import lms.model.query
import lms.model.scores
import lms.model.users

class APIBackend():
    """
    API backends provide a unified interface to an LMS.

    Note that instead of using an abstract class,
    methods will raise a NotImplementedError by default.
    This will allow child backends to fill in as much functionality as they can,
    while still leaving gaps where they are incomplete or impossible.
    """

    _testing_override: typing.Union[bool, None] = None
    """ A top-level override to control testing status. """

    def __init__(self,
            server: str,
            backend_type: str,
            testing: typing.Union[bool, str] = False,
            **kwargs: typing.Any) -> None:
        self.server: str = server
        """ The server this backend will connect to. """

        self.backend_type: str = backend_type
        """
        The type for this backend.
        Should be set by the child class.
        """

        parsed_testing = edq.util.parse.boolean(testing)
        if (APIBackend._testing_override is not None):
            parsed_testing = APIBackend._testing_override

        self.testing: bool = parsed_testing
        """ True if the backend is being used for a test. """

    # Core Methods

    def is_testing(self) -> bool:
        """ Check if this backend is in testing mode. """

        return self.testing

    def get_standard_headers(self) -> typing.Dict[str, str]:
        """
        Get standard headers for this backend.
        Children should take care to set the write header when performing a write operation.
        """

        return {
            lms.model.constants.HEADER_KEY_BACKEND: self.backend_type,
            lms.model.constants.HEADER_KEY_WRITE: 'false',
        }

    def not_found(self, operation: str, identifiers: typing.Dict[str, typing.Any]) -> None:
        """
        Called when the backend was unable to find some object.
        This will only be called when a requested object is not found,
        e.g., a user requested by ID is not found.
        This is not called when a list naturally returns zero results,
        or when a query does not match any items.
        """

        logging.warning("Object not found during operation: '%s'. Identifiers: %s.", operation, identifiers)

    # API Methods

    def courses_get(self,
            course_queries: typing.Collection[lms.model.courses.CourseQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.courses.Course]:
        """
        Get the specified courses associated with the given course.
        """

        if (len(course_queries) == 0):
            return []

        courses = self.courses_list(**kwargs)

        matches = []
        for course in sorted(courses):
            for query in course_queries:
                if (query.match(course)):
                    matches.append(course)
                    break

        return sorted(matches)

    def courses_fetch(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.courses.Course, None]:
        """
        Fetch a single course associated with the context user.
        Return None if no matching course is found.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        courses = self.courses_list(**kwargs)
        for course in courses:
            if (course.id == course_id):
                return course

        return None

    def courses_list(self,
            **kwargs: typing.Any) -> typing.List[lms.model.courses.Course]:
        """
        List the courses associated with the context user.
        """

        raise NotImplementedError('courses_list')

    def courses_assignments_get(self,
            course_query: lms.model.courses.CourseQuery,
            assignment_queries: typing.Collection[lms.model.assignments.AssignmentQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        """
        Get the specified assignments associated with the given course.
        """

        if (len(assignment_queries) == 0):
            return []

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        assignments = sorted(self.courses_assignments_list(resolved_course_query.get_id(), **kwargs))
        assignment_queries = sorted(assignment_queries)

        matches = []
        for assignment in assignments:
            for query in assignment_queries:
                if (query.match(assignment)):
                    matches.append(assignment)
                    break

        return matches

    def courses_assignments_fetch(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.assignments.Assignment, None]:
        """
        Fetch a single assignment associated with the given course.
        Return None if no matching assignment is found.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        assignments = self.courses_assignments_list(course_id, **kwargs)
        for assignment in sorted(assignments):
            if (assignment.id == assignment_id):
                return assignment

        return None

    def courses_assignments_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        """
        List the assignments associated with the given course.
        """

        raise NotImplementedError('courses_assignments_list')

    def courses_assignments_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        """
        List the assignments associated with the given course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        return sorted(self.courses_assignments_list(resolved_course_query.get_id(), **kwargs))

    def courses_assignments_scores_get(self,
            course_query: lms.model.courses.CourseQuery,
            assignment_query: lms.model.assignments.AssignmentQuery,
            user_queries: typing.Collection[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        Get the scores associated with the given assignment query and user queries.
        """

        if (len(user_queries) == 0):
            return []

        scores = self.courses_assignments_scores_resolve_and_list(course_query, assignment_query, **kwargs)

        matches = []
        for score in scores:
            for user_query in user_queries:
                if (user_query.match(score.user_query)):
                    matches.append(score)

        return sorted(matches)

    def courses_assignments_scores_fetch(self,
            course_id: str,
            assignment_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.scores.AssignmentScore, None]:
        """
        Fetch the score associated with the given assignment and user.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        scores = self.courses_assignments_scores_list(course_id, assignment_id, **kwargs)
        for score in scores:
            if ((score.user_query is not None) and (score.user_query.id == user_id)):
                return score

        return None

    def courses_assignments_scores_list(self,
            course_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given assignment.
        """

        raise NotImplementedError('courses_assignments_scores_list')

    def courses_assignments_scores_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            assignment_query: lms.model.assignments.AssignmentQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given assignment query.
        In addition to resolving the assignment query,
        users will also be resolved into their full version
        (instead of the reduced version usually returned with scores).
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        # Resolve the assignment query.
        matched_assignments = self.courses_assignments_get(resolved_course_query, [assignment_query], **kwargs)
        if (len(matched_assignments) == 0):
            return []

        target_assignment = matched_assignments[0]

        # List the scores.
        scores = self.courses_assignments_scores_list(resolved_course_query.get_id(), target_assignment.id, **kwargs)
        if (len(scores) == 0):
            return []

        # Resolve the scores' queries.

        users = self.courses_users_list(resolved_course_query.get_id(), **kwargs)
        users_map = {user.id: user for user in users}

        for score in scores:
            score.assignment_query = target_assignment.to_query()

            if ((score.user_query is not None) and (score.user_query.id in users_map)):
                score.user_query = users_map[score.user_query.id].to_query()

        return sorted(scores)

    def courses_assignments_scores_resolve_and_upload(self,
            course_query: lms.model.courses.CourseQuery,
            assignment_query: lms.model.assignments.AssignmentQuery,
            scores: typing.Dict[lms.model.users.UserQuery, lms.model.scores.ScoreFragment],
            **kwargs: typing.Any) -> int:
        """
        Resolve queries and upload assignment scores (indexed by user query).
        A None score (ScoreFragment.score) indicates that the score should be cleared.
        Return the number of scores sent to the LMS.
        """

        if (len(scores) == 0):
            return 0

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_assignment_query = self.resolve_assignment_query(resolved_course_query.get_id(), assignment_query, **kwargs)

        resolved_users = self.resolve_user_queries(resolved_course_query.get_id(), list(scores.keys()), warn_on_miss = True)
        resolved_scores: typing.Dict[str, lms.model.scores.ScoreFragment] = {}

        for (user, score) in scores.items():
            for resolved_user in resolved_users:
                if (user.match(resolved_user)):
                    resolved_scores[resolved_user.get_id()] = score
                    continue

        if (len(resolved_scores) == 0):
            return 0

        return self.courses_assignments_scores_upload(
                resolved_course_query.get_id(),
                resolved_assignment_query.get_id(),
                resolved_scores,
                **kwargs)

    def courses_assignments_scores_upload(self,
            course_id: str,
            assignment_id: str,
            scores: typing.Dict[str, lms.model.scores.ScoreFragment],
            **kwargs: typing.Any) -> int:
        """
        Upload assignment scores (indexed by user id).
        A None score (ScoreFragment.score) indicates that the score should be cleared.
        Return the number of scores sent to the LMS.
        """

        raise NotImplementedError('courses_assignments_scores_upload')

    def courses_gradebook_get(self,
            course_query: lms.model.courses.CourseQuery,
            assignment_queries: typing.Collection[lms.model.assignments.AssignmentQuery],
            user_queries: typing.Collection[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        """
        Get a gradebook with the specified users and assignments.
        Specifying no users/assignments is the same as requesting all of them.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        resolved_assignment_queries = self.resolve_assignment_queries(resolved_course_query.get_id(), assignment_queries, empty_all = True, **kwargs)
        assignment_ids = [query.get_id() for query in resolved_assignment_queries]

        resolved_user_queries = self.resolve_user_queries(resolved_course_query.get_id(), user_queries,
                empty_all = True, only_students = True, **kwargs)
        user_ids = [query.get_id() for query in resolved_user_queries]

        gradebook = self.courses_gradebook_fetch(resolved_course_query.get_id(), assignment_ids, user_ids, **kwargs)

        # Resolve the gradebook's queries (so it can show names/emails instead of just IDs).
        gradebook.update_queries(resolved_assignment_queries, resolved_user_queries)

        return gradebook

    def courses_gradebook_fetch(self,
            course_id: str,
            assignment_ids: typing.Collection[str],
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        """
        Get a gradebook with the specified users and assignments.
        If either the assignments or users is empty, an empty gradebook will be returned.
        """

        raise NotImplementedError('courses_gradebook_fetch')

    def courses_gradebook_list(self,
            course_id: str,
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        """
        List the full gradebook associated with this course.
        """

        return self.courses_gradebook_get(lms.model.courses.CourseQuery(id = course_id), [], [], **kwargs)

    def courses_gradebook_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> lms.model.scores.Gradebook:
        """
        List the full gradebook associated with this course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        return self.courses_gradebook_list(resolved_course_query.get_id(), **kwargs)

    def courses_gradebook_resolve_and_upload(self,
            course_query: lms.model.courses.CourseQuery,
            gradebook: lms.model.scores.Gradebook,
            **kwargs: typing.Any) -> int:
        """
        Resolve queries and upload a gradebook.
        Missing scores in the gradebook are skipped,
        a None score (ScoreFragment.score) indicates that the score should be cleared.
        Return the number of scores sent to the LMS.
        """

        if (len(gradebook) == 0):
            return 0

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        assignments = self.courses_assignments_list(resolved_course_query.get_id(), **kwargs)
        users = self.courses_users_list(resolved_course_query.get_id(), **kwargs)

        resolved_assignment_queries = [assignment.to_query() for assignment in assignments]
        resolved_user_queries = [user.to_query() for user in users]

        gradebook.update_queries(resolved_assignment_queries, resolved_user_queries)

        return self.courses_gradebook_upload(
                resolved_course_query.get_id(),
                gradebook,
                **kwargs)

    def courses_gradebook_upload(self,
            course_id: str,
            gradebook: lms.model.scores.Gradebook,
            **kwargs: typing.Any) -> int:
        """
        Upload a gradebook.
        All queries in the gradebook must be resolved (or at least have an ID).
        Missing scores in the gradebook are skipped,
        a None score (ScoreFragment.score) indicates that the score should be cleared.
        Return the number of scores sent to the LMS.
        """

        assignment_scores = gradebook.get_scores_by_assignment()

        count = 0
        for (assignment, user_scores) in assignment_scores.items():
            if (assignment.id is None):
                raise ValueError(f"Assignment query for gradebook upload ({assignment}) does not have an ID.")

            upload_scores = {}
            for (user, score) in user_scores.items():
                if (user.id is None):
                    raise ValueError(f"User query for gradebook upload ({user}) does not have an ID.")

                upload_scores[user.id] = score.to_fragment()

            count += self.courses_assignments_scores_upload(course_id, assignment.id, upload_scores, **kwargs)

        return count

    def courses_groupsets_create(self,
            course_id: str,
            name: str,
            **kwargs: typing.Any) -> lms.model.groupsets.GroupSet:
        """
        Create a group set.
        """

        raise NotImplementedError('courses_groupsets_create')

    def courses_groupsets_resolve_and_create(self,
            course_query: lms.model.courses.CourseQuery,
            name: str,
            **kwargs: typing.Any) -> lms.model.groupsets.GroupSet:
        """
        Resolve references and create a group set.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        return self.courses_groupsets_create(resolved_course_query.get_id(), name, **kwargs)

    def courses_groupsets_delete(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> bool:
        """
        Delete a group set.
        """

        raise NotImplementedError('courses_groupsets_delete')

    def courses_groupsets_resolve_and_delete(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            **kwargs: typing.Any) -> bool:
        """
        Resolve references and create a group set.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        return self.courses_groupsets_delete(resolved_course_query.get_id(), resolved_groupset_query.get_id(), **kwargs)

    def courses_groupsets_get(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_queries: typing.Collection[lms.model.groupsets.GroupSetQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSet]:
        """
        Get the specified group sets associated with the given course.
        """

        if (len(groupset_queries) == 0):
            return []

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        groupset_queries = sorted(groupset_queries)
        groupsets = sorted(self.courses_groupsets_list(resolved_course_query.get_id(), **kwargs))

        matches = []
        for groupset in groupsets:
            for query in groupset_queries:
                if (query.match(groupset)):
                    matches.append(groupset)
                    break

        return matches

    def courses_groupsets_fetch(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.groupsets.GroupSet, None]:
        """
        Fetch a single group set associated with the given course.
        Return None if no matching group set is found.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        groupsets = self.courses_groupsets_list(course_id, **kwargs)
        for groupset in groupsets:
            if (groupset.id == groupset_id):
                return groupset

        return None

    def courses_groupsets_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSet]:
        """
        List the group sets associated with the given course.
        """

        raise NotImplementedError('courses_groupsets_list')

    def courses_groupsets_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSet]:
        """
        List the group sets associated with the given course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        return sorted(self.courses_groupsets_list(resolved_course_query.get_id(), **kwargs))

    def courses_groupsets_memberships_resolve_and_add(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            memberships: typing.Collection[lms.model.groups.GroupMembership],
            **kwargs: typing.Any) -> typing.Tuple[
                    typing.List[lms.model.groups.Group],
                    typing.Dict[lms.model.groups.ResolvedGroupQuery, int]
            ]:
        """
        Resolve queries and add the specified users to the specified groups.
        This may create groups.

        Return:
         - Created Groups
         - Group Addition Counts
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)

        found_group_memberships, missing_group_memberships, _ = self._resolve_group_memberships(
                resolved_course_query.get_id(), resolved_groupset_query.get_id(), memberships, **kwargs)

        # Create missing groups.
        created_groups = []
        for name in sorted(missing_group_memberships.keys()):
            group = self.courses_groups_create(resolved_course_query.get_id(), resolved_groupset_query.get_id(), name, **kwargs)
            created_groups.append(group)

            # Merge in new group with existing structure.
            query = group.to_query()
            if (query not in found_group_memberships):
                found_group_memberships[query] = []

            found_group_memberships[query] += missing_group_memberships[name]

        # Add memberships.
        counts = {}
        for resolved_group_query in sorted(found_group_memberships.keys()):
            resolved_user_queries = found_group_memberships[resolved_group_query]

            count = self.courses_groups_memberships_resolve_and_add(
                    resolved_course_query, resolved_groupset_query, resolved_group_query,
                    resolved_user_queries,
                    **kwargs)

            counts[resolved_group_query] = count

        return (created_groups, counts)

    def courses_groupsets_memberships_resolve_and_set(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            memberships: typing.Collection[lms.model.groups.GroupMembership],
            **kwargs: typing.Any) -> typing.Tuple[
                    typing.List[lms.model.groups.Group],
                    typing.List[lms.model.groups.ResolvedGroupQuery],
                    typing.Dict[lms.model.groups.ResolvedGroupQuery, int],
                    typing.Dict[lms.model.groups.ResolvedGroupQuery, int],
            ]:
        """
        Resolve queries and set the specified group memberships.
        This may create and delete groups.

        Return:
         - Created Groups
         - Deleted Groups
         - Group Addition Counts
         - Group Subtraction Counts
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)

        found_group_memberships, missing_group_memberships, unused_groups = self._resolve_group_memberships(
                resolved_course_query.get_id(), resolved_groupset_query.get_id(), memberships, **kwargs)

        # Delete unused groups.
        deleted_groups = []
        for group_query in sorted(unused_groups):
            result = self.courses_groups_delete(resolved_course_query.get_id(), resolved_groupset_query.get_id(), group_query.get_id(), **kwargs)
            if (result):
                deleted_groups.append(group_query)

        # Create missing groups.
        created_groups = []
        for name in sorted(missing_group_memberships.keys()):
            group = self.courses_groups_create(resolved_course_query.get_id(), resolved_groupset_query.get_id(), name, **kwargs)
            created_groups.append(group)

            # Merge in new group with existing structure.
            query = group.to_query()
            if (query not in found_group_memberships):
                found_group_memberships[query] = []

            found_group_memberships[query] += missing_group_memberships[name]

        # Set memberships.
        add_counts = {}
        sub_counts = {}
        for resolved_group_query in sorted(found_group_memberships.keys()):
            resolved_user_queries = found_group_memberships[resolved_group_query]

            (add_count, sub_count, deleted) = self.courses_groups_memberships_resolve_and_set(
                    resolved_course_query, resolved_groupset_query, resolved_group_query,
                    resolved_user_queries,
                    delete_empty = True,
                    **kwargs)

            if (deleted):
                deleted_groups.append(resolved_group_query)

            add_counts[resolved_group_query] = add_count
            sub_counts[resolved_group_query] = sub_count

        return (created_groups, deleted_groups, add_counts, sub_counts)

    def courses_groupsets_memberships_resolve_and_subtract(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            memberships: typing.Collection[lms.model.groups.GroupMembership],
            **kwargs: typing.Any) -> typing.Dict[lms.model.groups.ResolvedGroupQuery, int]:
        """
        Resolve queries and subtract the specified users to the specified groups.
        This will not delete any groups.

        Return:
         - Group Subtraction Counts
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)

        found_group_memberships, missing_group_memberships, _ = self._resolve_group_memberships(
                resolved_course_query.get_id(), resolved_groupset_query.get_id(), memberships, **kwargs)

        # Warn about missing groups.
        for name in sorted(missing_group_memberships.keys()):
            logging.warning("Group does not exist: '%s'.", name)

        # Subtract memberships.
        counts = {}
        for resolved_group_query in sorted(found_group_memberships.keys()):
            resolved_user_queries = found_group_memberships[resolved_group_query]

            (count, _) = self.courses_groups_memberships_resolve_and_subtract(
                    resolved_course_query, resolved_groupset_query, resolved_group_query,
                    resolved_user_queries,
                    delete_empty = False,
                    **kwargs)

            counts[resolved_group_query] = count

        return counts

    def courses_groupsets_memberships_list(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        """
        List the membership of the group sets associated with the given course.
        """

        raise NotImplementedError('courses_groupsets_memberships_list')

    def courses_groupsets_memberships_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        """
        List the membership of the group sets associated with the given course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)

        memberships = self.courses_groupsets_memberships_list(resolved_course_query.get_id(), resolved_groupset_query.get_id(), **kwargs)

        # Resolve memberships.

        users = self.courses_users_list(resolved_course_query.get_id(), **kwargs)
        groups = self.courses_groups_list(resolved_course_query.get_id(), resolved_groupset_query.get_id(), **kwargs)

        users_map = {user.id: user.to_query() for user in users}
        groups_map = {group.id: group.to_query() for group in groups}

        for membership in memberships:
            membership.update_queries(resolved_groupset_query, users = users_map, groups = groups_map)

        return sorted(memberships)

    def courses_groups_create(self,
            course_id: str,
            groupset_id: str,
            name: str,
            **kwargs: typing.Any) -> lms.model.groups.Group:
        """
        Create a group.
        """

        raise NotImplementedError('courses_groups_create')

    def courses_groups_resolve_and_create(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            name: str,
            **kwargs: typing.Any) -> lms.model.groups.Group:
        """
        Resolve references and create a group.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        return self.courses_groups_create(resolved_course_query.get_id(), resolved_groupset_query.get_id(), name, **kwargs)

    def courses_groups_delete(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            **kwargs: typing.Any) -> bool:
        """
        Delete a group.
        """

        raise NotImplementedError('courses_groups_delete')

    def courses_groups_resolve_and_delete(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_query: lms.model.groups.GroupQuery,
            **kwargs: typing.Any) -> bool:
        """
        Resolve references and create a group.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        resolved_group_query = self.resolve_group_query(resolved_course_query.get_id(), resolved_groupset_query.get_id(), group_query, **kwargs)
        return self.courses_groups_delete(resolved_course_query.get_id(), resolved_groupset_query.get_id(), resolved_group_query.get_id(), **kwargs)

    def courses_groups_get(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_queries: typing.Collection[lms.model.groups.GroupQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.groups.Group]:
        """
        Get the specified groups associated with the given course.
        """

        if (len(group_queries) == 0):
            return []

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        groups = self.courses_groups_list(resolved_course_query.get_id(), resolved_groupset_query.get_id(), **kwargs)

        group_queries = sorted(group_queries)
        groups = sorted(groups)

        matches = []
        for group in groups:
            for query in group_queries:
                if (query.match(group)):
                    matches.append(group)
                    break

        return matches

    def courses_groups_fetch(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.groups.Group, None]:
        """
        Fetch a single group associated with the given course.
        Return None if no matching group is found.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        groups = self.courses_groups_list(course_id, groupset_id, **kwargs)
        for group in groups:
            if (group.id == group_id):
                return group

        return None

    def courses_groups_list(self,
            course_id: str,
            groupset_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groups.Group]:
        """
        List the groups associated with the given course.
        """

        raise NotImplementedError('courses_groups_list')

    def courses_groups_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.groups.Group]:
        """
        List the groups associated with the given course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        return self.courses_groups_list(resolved_course_query.get_id(), resolved_groupset_query.get_id(), **kwargs)

    def courses_groups_memberships_add(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> int:
        """
        Add the specified users to the group.
        """

        raise NotImplementedError('courses_groups_memberships_add')

    def courses_groups_memberships_resolve_and_add(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_query: lms.model.groups.GroupQuery,
            user_queries: typing.Collection[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> int:
        """
        Resolve queries and add the specified users to the group.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        resolved_group_query = self.resolve_group_query(resolved_course_query.get_id(), resolved_groupset_query.get_id(), group_query, **kwargs)
        resolved_user_queries = self.resolve_user_queries(resolved_course_query.get_id(), user_queries, warn_on_miss = True, **kwargs)

        # Get users already in this group.
        group_memberships = self.courses_groups_memberships_list(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                **kwargs)

        group_user_ids = {membership.user.id for membership in group_memberships if membership.user.id is not None}

        # Filter out users already in the group.
        user_ids = []
        for query in sorted(resolved_user_queries):
            if (query.get_id() in group_user_ids):
                logging.warning("User '%s' already in group '%s'.", query, resolved_group_query)
                continue

            user_ids.append(query.get_id())

        if (len(user_ids) == 0):
            return 0

        return self.courses_groups_memberships_add(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                user_ids,
                **kwargs)

    def courses_groups_memberships_list(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        """
        List the membership of the group associated with the given group set.
        """

        raise NotImplementedError('courses_groups_memberships_list')

    def courses_groups_memberships_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_query: lms.model.groups.GroupQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.GroupSetMembership]:
        """
        List the membership of the group associated with the given group set.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)

        groups = self.courses_groups_get(resolved_course_query, resolved_groupset_query, [group_query], **kwargs)
        if (len(groups) == 0):
            raise ValueError(f"Unable to find group: '{group_query}'.")

        group = groups[0]

        memberships = self.courses_groups_memberships_list(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                group.id,
                **kwargs)

        # Resolve memberships.

        users = self.courses_users_list(resolved_course_query.get_id(), **kwargs)
        users_map = {user.id: user.to_query() for user in users}

        groups_map = {group.id: group.to_query()}

        for membership in memberships:
            membership.update_queries(resolved_groupset_query, users = users_map, groups = groups_map)

        return sorted(memberships)

    def courses_groups_memberships_resolve_and_set(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_query: lms.model.groups.GroupQuery,
            user_queries: typing.Collection[lms.model.users.UserQuery],
            delete_empty: bool = False,
            **kwargs: typing.Any) -> typing.Tuple[int, int, bool]:
        """
        Resolve queries and set the specified users for the group.
        This method can both add and subtract users from the group.

        Returns:
         - The count of users added.
         - The count of users subtracted.
         - If this group was deleted.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        resolved_group_query = self.resolve_group_query(resolved_course_query.get_id(), resolved_groupset_query.get_id(), group_query, **kwargs)
        resolved_user_queries = self.resolve_user_queries(resolved_course_query.get_id(), user_queries, warn_on_miss = True, **kwargs)

        # Get users already in this group.
        group_memberships = self.courses_groups_memberships_list(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                **kwargs)

        group_user_queries = {membership.user for membership in group_memberships if membership.user is not None}
        group_user_ids = {membership.user.id for membership in group_memberships if membership.user.id is not None}
        query_user_ids = {resolved_user_query.get_id() for resolved_user_query in resolved_user_queries}

        # Collect users that need to be added.
        add_user_ids = []
        for query_user_id in query_user_ids:
            if (query_user_id not in group_user_ids):
                add_user_ids.append(query_user_id)

        # Collect users that need to be subtracted.
        sub_user_queries = []
        for group_user_query in group_user_queries:
            if (group_user_query not in resolved_user_queries):
                sub_user_queries.append(group_user_query)

        # Update the group.

        add_count = 0
        if (len(add_user_ids) > 0):
            add_count = self.courses_groups_memberships_add(
                    resolved_course_query.get_id(),
                    resolved_groupset_query.get_id(),
                    resolved_group_query.get_id(),
                    add_user_ids,
                    **kwargs)

        sub_count = 0
        deleted = False
        if (len(sub_user_queries) > 0):
            sub_count, deleted = self.courses_groups_memberships_resolve_and_subtract(
                    resolved_course_query,
                    resolved_groupset_query,
                    resolved_group_query,
                    sub_user_queries,
                    delete_empty = delete_empty,
                    **kwargs)

        return add_count, sub_count, deleted

    def courses_groups_memberships_subtract(self,
            course_id: str,
            groupset_id: str,
            group_id: str,
            user_ids: typing.Collection[str],
            **kwargs: typing.Any) -> int:
        """
        Subtract the specified users from the group.
        """

        raise NotImplementedError('courses_groups_memberships_subtract')

    def courses_groups_memberships_resolve_and_subtract(self,
            course_query: lms.model.courses.CourseQuery,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            group_query: lms.model.groups.GroupQuery,
            user_queries: typing.Collection[lms.model.users.UserQuery],
            delete_empty: bool = False,
            **kwargs: typing.Any) -> typing.Tuple[int, bool]:
        """
        Resolve queries and subtract the specified users from the group.
        Return:
            - The number of users deleted.
            - If this group was deleted.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        resolved_groupset_query = self.resolve_groupset_query(resolved_course_query.get_id(), groupset_query, **kwargs)
        resolved_group_query = self.resolve_group_query(resolved_course_query.get_id(), resolved_groupset_query.get_id(), group_query, **kwargs)
        resolved_user_queries = self.resolve_user_queries(resolved_course_query.get_id(), user_queries, warn_on_miss = True, **kwargs)

        # Get users already in this group.
        group_memberships = self.courses_groups_memberships_list(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                **kwargs)

        group_user_ids = {membership.user.id for membership in group_memberships if membership.user.id is not None}

        # Filter out users not in the group.
        user_ids = []
        for query in resolved_user_queries:
            if (query.get_id() not in group_user_ids):
                logging.warning("User '%s' is not in group '%s'.", query, resolved_group_query)
                continue

            user_ids.append(query.get_id())

        if (delete_empty and len(group_memberships) == 0):
            deleted = self.courses_groups_delete(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                **kwargs)
            return 0, deleted

        if (len(user_ids) == 0):
            return 0, False

        count = self.courses_groups_memberships_subtract(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                user_ids,
                **kwargs)

        deleted = False
        if (delete_empty and (count == len(group_memberships))):
            deleted = self.courses_groups_delete(
                resolved_course_query.get_id(),
                resolved_groupset_query.get_id(),
                resolved_group_query.get_id(),
                **kwargs)

        return count, deleted

    def courses_syllabus_fetch(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.Union[str, None]:
        """
        Get the syllabus for a course, or None if no syllabus exists.
        """

        raise NotImplementedError('courses_syllabus_fetch')

    def courses_syllabus_get(self,
            course_query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> typing.Union[str, None]:
        """
        Get the syllabus for a course query, or None if no syllabus exists.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        return self.courses_syllabus_fetch(resolved_course_query.get_id(), **kwargs)

    def courses_users_get(self,
            course_query: lms.model.courses.CourseQuery,
            user_queries: typing.Collection[lms.model.users.UserQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        """
        Get the specified users associated with the given course.
        """

        if (len(user_queries) == 0):
            return []

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        users = self.courses_users_list(resolved_course_query.get_id(), **kwargs)

        user_queries = sorted(user_queries)
        users = sorted(users)

        matches = []
        for user in users:
            for query in user_queries:
                if (query.match(user)):
                    matches.append(user)
                    break

        return matches

    def courses_users_fetch(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.users.CourseUser, None]:
        """
        Fetch a single user associated with the given course.
        Return None if no matching user is found.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        users = self.courses_users_list(course_id, **kwargs)
        for user in sorted(users):
            if (user.id == user_id):
                return user

        return None

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        """
        List the users associated with the given course.
        """

        raise NotImplementedError('courses_users_list')

    def courses_users_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        """
        List the users associated with the given course.
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)
        return list(sorted(self.courses_users_list(resolved_course_query.get_id(), **kwargs)))

    def courses_users_scores_get(self,
            course_query: lms.model.courses.CourseQuery,
            user_query: lms.model.users.UserQuery,
            assignment_queries: typing.Collection[lms.model.assignments.AssignmentQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        Get the scores associated with the given user query and assignment queries.
        """

        if (len(assignment_queries) == 0):
            return []

        scores = self.courses_users_scores_resolve_and_list(course_query, user_query, **kwargs)

        scores = sorted(scores)
        assignment_queries = sorted(assignment_queries)

        matches = []
        for score in scores:
            for assignment_query in assignment_queries:
                if (assignment_query.match(score.assignment_query)):
                    matches.append(score)

        return matches

    def courses_users_scores_fetch(self,
            course_id: str,
            user_id: str,
            assignment_id: str,
            **kwargs: typing.Any) -> typing.Union[lms.model.scores.AssignmentScore, None]:
        """
        Fetch the score associated with the given user and assignment.

        By default, this will just do a list and choose the relevant record.
        Specific backends may override this if there are performance concerns.
        """

        # The default implementation is the same as courses_assignments_scores_fetch().
        return self.courses_assignments_scores_fetch(course_id, assignment_id, user_id, **kwargs)

    def courses_users_scores_list(self,
            course_id: str,
            user_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given user.
        """

        raise NotImplementedError('courses_users_scores_list')

    def courses_users_scores_resolve_and_list(self,
            course_query: lms.model.courses.CourseQuery,
            user_query: lms.model.users.UserQuery,
            **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
        """
        List the scores associated with the given user query.
        In addition to resolving the user query,
        assignments will also be resolved into their full version
        (instead of the reduced version usually returned with scores).
        """

        resolved_course_query = self.resolve_course_query(course_query, **kwargs)

        # Resolve the user query.
        matched_users = self.courses_users_get(resolved_course_query, [user_query], **kwargs)
        if (len(matched_users) == 0):
            return []

        target_user = matched_users[0]

        # List the scores.
        scores = self.courses_users_scores_list(resolved_course_query.get_id(), target_user.id, **kwargs)
        if (len(scores) == 0):
            return []

        # Resolve the scores' queries.

        assignments = self.courses_assignments_list(resolved_course_query.get_id(), **kwargs)
        assignments_map = {assignment.id: assignment for assignment in assignments}

        for score in scores:
            score.user_query = target_user.to_query()

            if ((score.assignment_query is not None) and (score.assignment_query.id in assignments_map)):
                score.assignment_query = assignments_map[score.assignment_query.id].to_query()

        return sorted(scores)

    # Utility Methods

    def parse_assignment_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.assignments.AssignmentQuery, None]:
        """
        Attempt to parse an assignment query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return lms.model.query.parse_int_query(lms.model.assignments.AssignmentQuery, text, check_email = False)

    def parse_assignment_queries(self, texts: typing.Collection[typing.Union[str, None]]) -> typing.List[lms.model.assignments.AssignmentQuery]:
        """ Parse a list of assignment queries. """

        queries = []
        for text in texts:
            query = self.parse_assignment_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def parse_course_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.courses.CourseQuery, None]:
        """
        Attempt to parse a course query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return lms.model.query.parse_int_query(lms.model.courses.CourseQuery, text, check_email = False)

    def parse_course_queries(self, texts: typing.Collection[typing.Union[str, None]]) -> typing.List[lms.model.courses.CourseQuery]:
        """ Parse a list of course queries. """

        queries = []
        for text in texts:
            query = self.parse_course_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def parse_groupset_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.groupsets.GroupSetQuery, None]:
        """
        Attempt to parse a group set query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return lms.model.query.parse_int_query(lms.model.groupsets.GroupSetQuery, text, check_email = False)

    def parse_groupset_queries(self, texts: typing.Collection[typing.Union[str, None]]) -> typing.List[lms.model.groupsets.GroupSetQuery]:
        """ Parse a list of group set queries. """

        queries = []
        for text in texts:
            query = self.parse_groupset_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def parse_group_query(self, text: typing.Union[str, None]) -> typing.Union[lms.model.groups.GroupQuery, None]:
        """
        Attempt to parse a group query from a string.
        The there is no query, return a None.
        If the query is malformed, raise an exception.

        By default, this method assumes that LMS IDs are ints.
        Child backends may override this to implement their specific behavior.
        """

        return lms.model.query.parse_int_query(lms.model.groups.GroupQuery, text, check_email = False)

    def parse_group_queries(self, texts: typing.Collection[typing.Union[str, None]]) -> typing.List[lms.model.groups.GroupQuery]:
        """ Parse a list of group queries. """

        queries = []
        for text in texts:
            query = self.parse_group_query(text)
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

        return lms.model.query.parse_int_query(lms.model.users.UserQuery, text, check_email = True)

    def parse_user_queries(self, texts: typing.Collection[typing.Union[str, None]]) -> typing.List[lms.model.users.UserQuery]:
        """ Parse a list of user queries. """

        queries = []
        for text in texts:
            query = self.parse_user_query(text)
            if (query is not None):
                queries.append(query)

        return queries

    def resolve_assignment_query(self,
            course_id: str,
            assignment_query: lms.model.assignments.AssignmentQuery,
            **kwargs: typing.Any) -> lms.model.assignments.ResolvedAssignmentQuery:
        """ Resolve the assignment query or raise an exception. """

        # Shortcut already resolved queries.
        if (isinstance(assignment_query, lms.model.assignments.ResolvedAssignmentQuery)):
            return assignment_query

        results = self.resolve_assignment_queries(course_id, [assignment_query], **kwargs)
        if (len(results) == 0):
            raise ValueError(f"Could not resolve assignment query: '{assignment_query}'.")

        return results[0]

    def resolve_assignment_queries(self,
            course_id: str,
            queries: typing.Collection[lms.model.assignments.AssignmentQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.assignments.ResolvedAssignmentQuery]:
        """
        Resolve a list of assignment queries into a list of resolved assignment queries.
        See _resolve_queries().
        """

        results = self._resolve_queries(
            queries,
            'assignment',
            self.courses_assignments_list(course_id, **kwargs),
            lms.model.assignments.ResolvedAssignmentQuery,
            **kwargs)

        return typing.cast(typing.List[lms.model.assignments.ResolvedAssignmentQuery], results)

    def resolve_course_query(self,
            query: lms.model.courses.CourseQuery,
            **kwargs: typing.Any) -> lms.model.courses.ResolvedCourseQuery:
        """ Resolve the course query or raise an exception. """

        # Shortcut already resolved queries.
        if (isinstance(query, lms.model.courses.ResolvedCourseQuery)):
            return query

        results = self.resolve_course_queries([query], **kwargs)
        if (len(results) == 0):
            raise ValueError(f"Could not resolve course query: '{query}'.")

        return results[0]

    def resolve_course_queries(self,
            queries: typing.Collection[lms.model.courses.CourseQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.courses.ResolvedCourseQuery]:
        """
        Resolve a list of course queries into a list of resolved course queries.
        See _resolve_queries().
        """

        results = self._resolve_queries(
            queries,
            'course',
            self.courses_list(**kwargs),
            lms.model.courses.ResolvedCourseQuery,
            **kwargs)

        return typing.cast(typing.List[lms.model.courses.ResolvedCourseQuery], results)

    def resolve_group_queries(self,
            course_id: str,
            groupset_id: str,
            queries: typing.Collection[lms.model.groups.GroupQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.groups.ResolvedGroupQuery]:
        """
        Resolve a list of group queries into a list of resolved group queries.
        See _resolve_queries().
        """

        results = self._resolve_queries(
            queries,
            'group',
            self.courses_groups_list(course_id, groupset_id, **kwargs),
            lms.model.groups.ResolvedGroupQuery,
            **kwargs)

        return typing.cast(typing.List[lms.model.groups.ResolvedGroupQuery], results)

    def resolve_group_query(self,
            course_id: str,
            groupset_id: str,
            query: lms.model.groups.GroupQuery,
            **kwargs: typing.Any) -> lms.model.groups.ResolvedGroupQuery:
        """ Resolve the group query or raise an exception. """

        # Shortcut already resolved queries.
        if (isinstance(query, lms.model.groups.ResolvedGroupQuery)):
            return query

        results = self.resolve_group_queries(course_id, groupset_id, [query], **kwargs)
        if (len(results) == 0):
            raise ValueError(f"Could not resolve group query: '{query}'.")

        return results[0]

    def resolve_groupset_queries(self,
            course_id: str,
            queries: typing.Collection[lms.model.groupsets.GroupSetQuery],
            **kwargs: typing.Any) -> typing.List[lms.model.groupsets.ResolvedGroupSetQuery]:
        """
        Resolve a list of group set queries into a list of resolved group set queries.
        See _resolve_queries().
        """

        results = self._resolve_queries(
            queries,
            'group set',
            self.courses_groupsets_list(course_id, **kwargs),
            lms.model.groupsets.ResolvedGroupSetQuery,
            **kwargs)

        return typing.cast(typing.List[lms.model.groupsets.ResolvedGroupSetQuery], results)

    def resolve_groupset_query(self,
            course_id: str,
            groupset_query: lms.model.groupsets.GroupSetQuery,
            **kwargs: typing.Any) -> lms.model.groupsets.ResolvedGroupSetQuery:
        """ Resolve the group set query or raise an exception. """

        # Shortcut already resolved queries.
        if (isinstance(groupset_query, lms.model.groupsets.ResolvedGroupSetQuery)):
            return groupset_query

        results = self.resolve_groupset_queries(course_id, [groupset_query], **kwargs)
        if (len(results) == 0):
            raise ValueError(f"Could not resolve group set query: '{groupset_query}'.")

        return results[0]

    def resolve_user_queries(self,
            course_id: str,
            queries: typing.Collection[lms.model.users.UserQuery],
            only_students: bool = False,
            **kwargs: typing.Any) -> typing.List[lms.model.users.ResolvedUserQuery]:
        """
        Resolve a list of user queries into a list of resolved user queries.
        See _resolve_queries().
        """

        filter_func = None
        if (only_students):
            filter_func = lambda user: user.is_student()  # pylint: disable=unnecessary-lambda-assignment

        results = self._resolve_queries(
            queries,
            'user',
            self.courses_users_list(course_id, **kwargs),
            lms.model.users.ResolvedUserQuery,
            filter_func = filter_func,
            **kwargs)

        return typing.cast(typing.List[lms.model.users.ResolvedUserQuery], results)

    def _resolve_queries(self,
            queries: typing.Collection[lms.model.query.BaseQuery],
            label: str,
            items: typing.Collection,
            resolved_query_class: typing.Type,
            empty_all: bool = False,
            warn_on_miss: bool = False,
            filter_func: typing.Union[typing.Callable, None] = None,
            **kwargs: typing.Any) -> typing.List[lms.model.query.ResolvedBaseQuery]:
        """
        Resolve a list of queries.
        The returned list may be shorter than the list of queries (if input queries are not matched).
        The queries will be deduplicated and sorted.

        If |empty_all| is true and no queries are specified, then all items will be returned.

        If |filter_func| is passed, then that function will be called with each raw item,
        and ones that return true will be kept.
        """

        if (filter_func is not None):
            items = list(filter(filter_func, items))

        if (empty_all and (len(queries) == 0)):
            return list(sorted({resolved_query_class(item) for item in items}))

        matched_queries = []  # type: ignore[var-annotated]
        for query in queries:
            match = False
            for item in items:
                if (query.match(item)):
                    matched_query = resolved_query_class(item)

                    if (match):
                        raise ValueError(
                            f"Ambiguous {label} query ('{query}')"
                            f" matches multiple {label}s ['{matched_queries[-1]}', '{matched_query}'].")

                    matched_queries.append(matched_query)
                    match = True

            if ((not match) and warn_on_miss):
                logging.warning("Could not resolve %s query '%s'.", label, query)

        return list(sorted(set(matched_queries)))

    def _resolve_group_memberships(self,
            course_id: str,
            groupset_id: str,
            memberships: typing.Collection[lms.model.groups.GroupMembership],
            **kwargs: typing.Any) -> typing.Tuple[
                typing.Dict[lms.model.groups.ResolvedGroupQuery, typing.List[lms.model.users.ResolvedUserQuery]],
                typing.Dict[str, typing.List[lms.model.users.ResolvedUserQuery]],
                typing.List[lms.model.groups.ResolvedGroupQuery]]:
        """
        Resolve a list of group memberships.
        This method will resolved each query and split up the memberships by the appropriate group.
        If a group does not exist, the memberships will be split by apparent group name.

        Returns:
         - Memberships in Found Groups (keyed by resolved group query)
         - Memberships in Missing Groups (keyed by apparent group name)
         - Groups not involved in any of the returned memberships.

        The returned dicts will be the found groups (keyed by resolved query) and then the missing groups (keyed by apparent group name).
        """

        found_group_memberships: typing.Dict[lms.model.groups.ResolvedGroupQuery, typing.List[lms.model.users.ResolvedUserQuery]] = {}
        missing_group_memberships: typing.Dict[str, typing.List[lms.model.users.ResolvedUserQuery]] = {}

        users = self.courses_users_list(course_id, **kwargs)
        resolved_user_queries = [user.to_query() for user in sorted(users)]

        groups = self.courses_groups_list(course_id, groupset_id, **kwargs)
        resolved_group_queries = [group.to_query() for group in sorted(groups)]

        for (i, membership) in enumerate(memberships):
            # Resolve user.

            resolved_user_query = None
            for possible_user_query in resolved_user_queries:
                if (membership.user.match(possible_user_query)):
                    resolved_user_query = possible_user_query
                    break

            if (resolved_user_query is None):
                logging.warning("Could not resolve user '%s' for membership entry at index %d.", membership.user, i)
                continue

            # Resolve group.

            resolved_group_query = None
            for possible_group_query in resolved_group_queries:
                if (membership.group.match(possible_group_query)):
                    resolved_group_query = possible_group_query
                    break

            # Add to the correct collection.

            if (resolved_group_query is None):
                if ((membership.group.name is None) or (len(membership.group.name) == 0)):
                    logging.warning(("Membership entry at index %d has a group with no name."
                        + " Ensure that non-existent groups all have names."), i)
                    continue

                if (membership.group.name not in missing_group_memberships):
                    missing_group_memberships[membership.group.name] = []

                missing_group_memberships[membership.group.name].append(resolved_user_query)
            else:
                if (resolved_group_query not in found_group_memberships):
                    found_group_memberships[resolved_group_query] = []

                found_group_memberships[resolved_group_query].append(resolved_user_query)

        unused_groups = sorted(list(set(resolved_group_queries) - set(found_group_memberships.keys())))

        return (found_group_memberships, missing_group_memberships, unused_groups)
