Releasing ironic-staging-drivers
================================

This section is relevant to the maintainers of ironic-staging-drivers. You have
to be a member of the ironic-staging-drivers-release_ group to do releases.

#. Verify that the CI works via a dummy patch.

#. Create a **signed** tag locally::

       git tag -s -m "Release <version>" <version>

#. Push the new tag to gerrit::

       git push gerrit <version>

#. Wait for the new release to appear on PyPI_, contact the infra team in case
   of any issues.

#. If a stable branch is needed, go to the *branches* section of the
   `ironic-staging-drivers settings`_ in gerrit and add a new branch from the
   newly created tag.

#. If a stable branch has been created, submit a change for it that:

   #. updates ``.gitreview`` with a new ``defaultbranch``,

   #. updates ``extra-requirements.txt`` with a link to ironic stable,

   #. updates ``tox.ini`` to use upper constraints from the corresponding
      release.

   See the `stable/xena patch`_ for an example.

.. _ironic-staging-drivers-release: https://review.opendev.org/admin/groups/bf6b0cc8749d0d89a8620882f697a60b46f032ab
.. _PyPI: https://pypi.org/project/ironic-staging-drivers/
.. _ironic-staging-drivers settings: https://review.opendev.org/admin/repos/x/ironic-staging-drivers
.. _stable/xena patch: https://review.opendev.org/c/x/ironic-staging-drivers/+/810657
