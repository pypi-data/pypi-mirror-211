import json
import flask
import hashlib

from ohmytmp import Ohmytmp
from ohmytmp_plugins.taggy import TagInterpreter
from ohmytmp_plugins.simimg import SimImg


class SSR:
    def __init__(self) -> None:
        self.sha_p = dict()
        self.p_sha = dict()

        self.ai = Ohmytmp()
        self.si = SimImg()
        self.ti = TagInterpreter()

        self.ai.register(self.si)
        self.ai.register(self.ti)

    def showimgs(self, files: list) -> str:
        jsrc = list()
        for p in files:
            if p not in self.p_sha:
                psha = hashlib.new('sha256', p.encode('utf8')).hexdigest()
                self.p_sha[p] = psha
                self.sha_p[psha] = p
            jsrc.append('/file/%s' % self.p_sha[p])
        return open('img.html', 'r').read().replace(
            '["Untitled.png"]',
            json.dumps(jsrc)
        )

    def walk(self, d: str) -> None:
        self.ai.walk(d)

    def w_root(self) -> str:
        return 'Hello, world!'

    def w_file(self, sha256: str) -> flask.Response:
        return flask.send_file(self.sha_p[sha256])

    def w_sim(self, phash: int) -> str:
        return self.showimgs(self.si.findsim(int(phash), 4))

    def w_tag(self, tags: str) -> str:
        return self.showimgs(self.ti.getsrcs(tags))
