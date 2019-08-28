"""An example of using kubetest to manage a configmap."""

import os


def test_secret(kube):

    f = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'configs',
        'secret.yaml'
    )

    cm = kube.load_secret(f)

    kube.create(cm)

    cm.wait_until_ready(timeout=10)
    cm.refresh()

    kube.delete(cm)

    cm.wait_until_deleted(timeout=20)
