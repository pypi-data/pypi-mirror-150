

import os
import shutil
from collections import namedtuple

from twisted import logger
from twisted.internet.threads import deferToThread
from twisted.internet.defer import succeed, fail
from twisted.internet.defer import inlineCallbacks, returnValue

ExportSpec = namedtuple(
    'ExportSpec', ["path", "destination", "no_clear", "writer", "contexts"],
    defaults=['[id]', False, None, ['all']]
)


class ChannelNotFound(Exception):
    pass


class ChannelNotAuthenticated(Exception):
    pass


class LocalEximManager(object):
    def __init__(self, actual):
        self._actual = actual
        self._log = None
        self._exports = {}
        self._imports = {}

    @property
    def actual(self):
        return self._actual

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="exim.local", source=self)
        return self._log

    def register_export(self, tag, spec):
        tag = tag.upper()
        if tag not in self._exports.keys():
            self._exports[tag] = []
        if isinstance(spec, str):
            spec = ExportSpec(spec)
        self.log.debug("Registering '{}' Export from '{}'".format(tag, spec.path))
        self._exports[tag].append(spec)

    def register_import(self):
        pass

    def install(self):
        self.log.info("Initializing Local Export/Import Infrastructure")

    @inlineCallbacks
    def _clear_directory(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    yield deferToThread(shutil.rmtree(file_path))
            except Exception as e:
                self.log.warn('Failed to delete %s. Reason: %s' % (file_path, e))

    @inlineCallbacks
    def _remove_directory(self, directory):
        yield deferToThread(shutil.rmtree, directory)

    @inlineCallbacks
    def _copy_tree(self, src, dest):
        yield deferToThread(shutil.copytree, src, dest)

    @inlineCallbacks
    def _execute_export(self, channel, tag, spec):
        target_path = os.path.join(channel, tag)
        if not os.path.exists(target_path):
            return False
        self.log.info("Executing Export {}".format(spec))
        if spec.destination:
            if spec.destination == '[id]':
                destination = self.actual.id
            else:
                destination = spec.destination
            destination = destination.upper()
            target_path = os.path.join(target_path, destination)
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
        path_part = os.path.basename(spec.path)
        target_path = os.path.join(target_path, path_part)
        if not spec.no_clear:
            if os.path.exists(target_path):
                if os.path.isdir(target_path):
                    yield self._remove_directory(target_path)
                else:
                    os.unlink(target_path)
        if spec.writer:
            yield spec.writer(target_path)
        else:
            yield self._copy_tree(spec.path, target_path)

    @inlineCallbacks
    def execute(self, channel, context=None):
        self.log.info("Executing Local Exports")
        for tag, specs in self._exports.items():
            for spec in specs:
                if context in spec.contexts or 'all' in spec.contexts:
                    self.actual.signal_exim_action_start(tag, 'export')
                    yield self._execute_export(channel, tag, spec)
            self.actual.signal_exim_action_done(tag, 'export')
        self.log.info("Executing Local Imports")
        pass

    def _authenticate_channel(self, path):
        if not os.path.exists(os.path.join(path, '.ebs')):
            return fail(ChannelNotAuthenticated())
        return succeed(path)

    @inlineCallbacks
    def find_authenticated_channel(self):
        candidates = [self.actual.config.exim_local_mountpoint]
        for candidate in candidates:
            if not os.path.exists(candidate):
                self.log.debug("Channel '{}' not found.".format(candidate))
                continue
            try:
                yield self._authenticate_channel(candidate)
            except ChannelNotAuthenticated:
                self.log.debug("Channel '{}' not authenticated.".format(candidate))
                continue
            returnValue(candidate)
        returnValue(None)

    @inlineCallbacks
    def trigger(self, context):
        if not self.actual.config.exim_local_enabled:
            return
        self.log.info("Triggering Export/Import")
        channel = yield self.find_authenticated_channel()
        if not channel:
            self.log.info("No authenticated channel found. Not executing EXIM.")
            return
        self.log.info("Found Authenticated Channel '{}'. Executing EXIM.".format(channel))
        self.actual.busy_set()
        yield self.execute(channel, context=context)
        self.actual.busy_clear()
