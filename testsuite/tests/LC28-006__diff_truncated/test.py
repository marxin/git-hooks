from support import *

class TestRun(TestCase):
    def test_push_commit_on_master(self):
        """Try pushing one single-file commit on master.
        """
        cd ('%s/repo' % TEST_DIR)

        # Push master to the `origin' remote.  The delta should be one
        # commit with one file being modified.
        p = Run('git push origin master'.split())
        expected_out = """\
remote: *** cvs_check: `trunk/repo/a'
remote: DEBUG: Content-Type: text/plain; charset="us-ascii"
remote: MIME-Version: 1.0
remote: Content-Transfer-Encoding: 7bit
remote: From: Test Suite <testsuite@adacore.com>
remote: To: git-hooks-ci@example.com
remote: Bcc: file-ci@gnat.com
remote: Subject: [repo] Updated a.
remote: X-ACT-checkin: repo
remote: X-Git-Refname: refs/heads/master
remote: X-Git-Oldrev: d065089ff184d97934c010ccd0e7e8ed94cb7165
remote: X-Git-Newrev: 1becc1a611a0059146a839001527229fa6f75569
remote:
remote: commit 1becc1a611a0059146a839001527229fa6f75569
remote: Author: Joel Brobecker <brobecker@adacore.com>
remote: Date:   Fri Apr 27 13:08:29 2012 -0700
remote:
remote:     Updated a.
remote:
remote:     Added a lot of text to a, to triggger "diff truncated message".
remote:
remote: Diff:
remote: ---
remote:  a |   38 +++++++++++++++++++++++++++++++++++++-
remote:  1 file changed, 37 insertions(+), 1 deletion(-)
remote:
remote: diff --git a/a b/a
remote: index 01d0f12..4f675c8 100644
remote: --- a/a
remote: +++ b/a
remote: @@ -1,3 +1,39 @@
remote:  Some file.
remote: -Se
remote:
remote: [diff truncated at 200 bytes]
remote:
To ../bare/repo.git
   d065089..1becc1a  master -> master
"""

        self.assertEqual(p.status, 0, p.image)
        self.assertRunOutputEqual(p, expected_out)

if __name__ == '__main__':
    runtests()