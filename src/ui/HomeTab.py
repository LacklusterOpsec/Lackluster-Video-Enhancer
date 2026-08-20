import os
import sys

from ..Util import openLink, networkCheck
from ..constants import CWD
import requests


class HomeTab:
    def __init__(self, parent):
        self.parent = parent
        self.QConnect()

    def getChangelog(self):
        changeLog = ""
        try:
            response = requests.get(
                "https://api.github.com/repos/LacklusterOpsec/Lackluster-Video-Enhancer/releases"
            )
            releases = response.json()
            releaseTags = [release["tag_name"] for release in releases][:5]
            releaseBodies = [release["body"].replace(r"\r\n", "") for release in releases][:5]
            for releaseTag, releaseBody in zip(releaseTags, releaseBodies):
                changeLog += "\n# " + releaseTag
                changeLog += "\n" + releaseBody
        except Exception:
            pass
        if not changeLog.strip():
            # No releases on this fork yet (or no network): fall back to the
            # CHANGELOG.md bundled with the app.
            changeLog = self._local_changelog()
        return changeLog

    def _local_changelog(self):
        candidates = [CWD, os.path.dirname(sys.executable)]
        for base in candidates:
            if not base:
                continue
            path = os.path.join(base, "CHANGELOG.md")
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception:
                    pass
        return ""

    def QConnect(self):
        self.parent.githubBtn.clicked.connect(
            lambda: openLink("https://github.com/LacklusterOpsec/Lackluster-Video-Enhancer")
        )
        # this fork has no donation page of its own, hide the upstream button
        self.parent.kofiBtn.setVisible(False)
        if networkCheck(
            "https://api.github.com/repos/LacklusterOpsec/Lackluster-Video-Enhancer/releases"
        ):
            self.parent.changeLogText.setVisible(True)
            changelog = self.getChangelog()
            self.parent.changeLogText.setMarkdown(changelog)