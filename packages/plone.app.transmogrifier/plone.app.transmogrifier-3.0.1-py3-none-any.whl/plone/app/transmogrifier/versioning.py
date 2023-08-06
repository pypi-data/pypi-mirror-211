from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import provider


VERSIONABLE_KEY = "plone.app.transmogrifier.versioning:versionable"


@implementer(ISection)
class BaseVersioningSection:
    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.repository = getToolByName(transmogrifier.context, "portal_repository")
        self.anno = IAnnotations(transmogrifier)
        self.save()

    def save(self):
        versionable = self.repository._versionable_content_types
        self.anno[VERSIONABLE_KEY] = tuple(versionable)

    def restore(self):
        versionable = self.repository._versionable_content_types
        versionable[:] = ()
        versionable.extend(self.anno[VERSIONABLE_KEY])

    def clear(self):
        versionable = self.repository._versionable_content_types
        versionable[:] = ()


@provider(ISectionBlueprint)
class DisableVersioningSection(BaseVersioningSection):
    def __iter__(self):
        for item in self.previous:
            try:
                self.save()
                self.clear()
                yield item
            finally:
                self.restore()


@provider(ISectionBlueprint)
class EnableVersioningSection(BaseVersioningSection):
    def __iter__(self):
        for item in self.previous:
            self.restore()
            yield item
