

from cached_property import threaded_cached_property_with_ttl
from ebs.linuxnode.core.resources import CacheableResource
from ebs.linuxnode.core.constants import WEBRESOURCE


class ScheduledResourceClass(CacheableResource):
    @threaded_cached_property_with_ttl(ttl=3)
    def next_use(self):
        next_event = self.node.event_manager(WEBRESOURCE).next(
            resource=self.filename)
        if next_event:
            return next_event.start_time
        else:
            return None
