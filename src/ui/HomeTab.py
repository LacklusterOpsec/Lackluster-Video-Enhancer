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
        fetched_tag = ""
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
            if releaseTags:
                fetched_tag = releaseTags[0].replace("RVE-", "")
        except Exception:
            pass
        # Prefer the CHANGELOG.md bundled with the app over older GitHub release
        # text: the home tab should report what we actually shipped.
        if not changeLog.strip():
            changeLog = self._local_changelog()
        else:
            try:
                fetched = tuple(map(int, fetched_tag.split(".")))
                local = tuple(map(int, "2.4.3".split(".")))
                if fetched < local:
                    changeLog = self._local_changelog()
            except Exception:
                pass
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