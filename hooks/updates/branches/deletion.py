"""Handling of branch deletion."""

from errors import InvalidUpdate
from git import commit_oneline
from updates import AbstractUpdate
from updates.branches import branch_summary_of_changes_needed

BRANCH_DELETION_EMAIL_BODY_TEMPLATE = """\
The branch '%(short_ref_name)s' was deleted.
It previously pointed to:

 %(commit_oneline)s"""


class BranchDeletion(AbstractUpdate):
    """Update object for branch creation/update."""
    def self_sanity_check(self):
        """See AbstractUpdate.self_sanity_check."""
        assert (self.ref_name.startswith('refs/heads/')
                or self.ref_name.startswith('refs/users/')
                or self.ref_name.startswith('refs/vendors/'))

    def validate_ref_update(self):
        """See AbstractUpdate.validate_ref_update."""
        # Deleting a user or vendor branch is always allowed.
        if not (self.ref_name.startswith('refs/users')
                or self.ref_name.startswith('refs/vendors')):
            raise InvalidUpdate(
                'Branch deletion is only allowed for user and vendor '
                'branches. If another branch was created by mistake, '
                'contact an administrator to delete it on the server '
                'with git update-ref. If a development branch is dead, '
                'also contact an administrator to move it under '
                'refs/dead/heads/ rather than deleting it.')

    def get_update_email_contents(self):
        """See AbstractUpdate.get_update_email_contents.
        """
        subject = "[%s] Deleted branch %s" % (self.email_info.project_name,
                                              self.short_ref_name)

        update_info = {'short_ref_name': self.short_ref_name,
                       'commit_oneline': commit_oneline(self.old_rev),
                       }
        body = BRANCH_DELETION_EMAIL_BODY_TEMPLATE % update_info
        if branch_summary_of_changes_needed(self.added_commits,
                                            self.lost_commits):
            body += self.summary_of_changes()

        return (self.everyone_emails(), subject, body)
