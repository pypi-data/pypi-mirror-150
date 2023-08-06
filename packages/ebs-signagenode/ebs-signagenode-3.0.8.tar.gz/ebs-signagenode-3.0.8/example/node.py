

from random import shuffle
from datetime import datetime
from datetime import timedelta

from ebs.linuxnode.core.constants import TEXT
from ebs.linuxnode.core.constants import WEBRESOURCE

from ebs.signagenode.node import SignageNode


class ExampleSignageNode(SignageNode):
    # Gallery Example
    def _picsum_fname(self, iid, w, h):
        return "{0}-{1}x{2}.jpg".format(iid, w, h)

    def _picsum_url(self, iid, w, h):
        return 'https://picsum.photos/id/{0}/{1}/{2}/'.format(iid, w, h)

    def _populate_gallery(self):
        self.log.info("Populating Gallery Resources")
        ids = [100, 1003, 1011, 1018, 1025]
        w = 320
        h = 640
        items = []
        for iid in ids:
            url = self._picsum_url(iid, w, h)
            fname = self._picsum_fname(iid, w, h)
            self.log.info("Inserting Gallery Resource {} from {}".format(fname, url))
            self.resource_manager.insert(fname, url)
            items.append((fname, None))
        self.gallery_load(items)

    def _gallery_show(self):
        self.gui_gallery.visible = True

    def _gallery_hide(self):
        self.gui_gallery.visible = False

    def _demo_gallery(self):
        self.reactor.callLater(2, self._populate_gallery)
        self.reactor.callLater(10, self._gallery_show)
        self.reactor.callLater(30, self._gallery_hide)
        self.reactor.callLater(70, self._gallery_show)

    # Text Events Example
    _language_tests = {
        'English': 'English Keyboard',
        'Hindi': 'हिंदी कीबोर्ड',
        'Telugu': 'తెలుగులో టైప్',
        'Kannada': 'ಕನ್ನಡ ಕೀಲಿಮಣೆ',
        'Tamil': 'தமிழ் விசைப்பலகை',
        'Marathi': 'मराठी कळफलक',
        'Bengali': 'বাংলা কিবোর্ড',
        'Malyalam': 'മലയാളം കീബോര്‍ഡ്',
        'Punjabi': 'ਪੰਜਾਬੀ ਦੇ ਬੋਰਡ',
        'Oriya': 'ଉତ୍କଳଲିପି',
        'Urdu': 'اردوبورڈ',
    }

    def _create_demo_text_events(self, offset=1):
        self.log.info("Creating Demo Text Events")
        langs = list(self._language_tests.keys())
        runslot = list(range(len(langs)))
        shuffle(runslot)
        perslot = 30
        n = datetime.now() + timedelta(seconds=offset * perslot)
        for idx in range(len(self._language_tests)):
            eid = 't{0}'.format(runslot[idx] + offset)
            lang = langs[runslot[idx]]
            self.event_manager(TEXT).insert(
                eid, etype=TEXT, start_time=n, duration=25,
                resource='{0}: {1}'.format(lang, self._language_tests[lang])
            )
            n = n + timedelta(seconds=perslot)

    def _demo_marquee(self):
        self._create_demo_text_events(0)
        self.event_manager(TEXT).prune()

    # Media Events Examples

    _test_resources = [
        'v1.mp4',
        'p1.pdf',
        'v2.mp4',
        'v3.mp4',
        'v4.mp4',
    ]

    def _populate_resources(self):
        for r in self._test_resources:
            url = 'http://static.chintal.in/starxmedia/demo/{0}'.format(r)
            self.log.info("Inserting Test Resource {} from {}".format(r, url))
            self.resource_manager.insert(r, url=url)

    def _create_demo_events(self, offset=0, resources=None):
        self.log.info("Creating Demo Media Events")
        if not resources:
            resources = self._test_resources
        runslot = list(range(len(resources)))
        shuffle(runslot)
        perslot = 90
        n = datetime.now() + timedelta(seconds=offset * perslot)
        n += timedelta(seconds=3)
        for idx in range(len(resources)):
            eid = 'e{0}'.format(runslot[idx] + offset)
            self.event_manager(WEBRESOURCE).insert(
                eid, etype=WEBRESOURCE, start_time=n, duration=60,
                resource=resources[runslot[idx]]
            )
            n = n + timedelta(seconds=perslot)

    def _demo_media(self):
        self._populate_resources()
        self._create_demo_events()
        self.event_manager(WEBRESOURCE).prune()

    def start(self):
        super(ExampleSignageNode, self).start()
        self.gui_gallery.visible = False
        self.reactor.callLater(3, self._demo_gallery)
        self.reactor.callLater(2, self._demo_marquee)
        self.reactor.callLater(2, self._demo_media)
