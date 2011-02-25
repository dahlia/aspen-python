import os
import logging
from os.path import isdir, join

from aspen import restarter
from aspen.website import Website
from aspen.configuration import Configuration
from diesel import Application, Loop, Service
from diesel.protocols import http


log = logging.getLogger('aspen.cli')


def main(argv=None):
    try:
        configuration = Configuration(argv)
        configuration.app = app = Application()
        website = Website(configuration)
        for hook in configuration.hooks.startup:
            website = hook(website) or website

        # change current working directory
        os.chdir(configuration.root)

        if configuration.conf.aspen.yes('changes_kill'):
            # restart for template files too;
            # TODO generalize this to all of etc?
            # TODO can't we just invalidate the simplate cache for these?
            templates = join(configuration.root, '.aspen', 'etc', 'templates')
            if isdir(templates):
                for filename in os.listdir(templates):
                    restarter.add(join(templates, filename))
            app.add_loop(Loop(restarter.loop))
        
        port = configuration.address[1]
        app.add_service(Service(http.HttpServer(website), port))

        log.warn("Greetings, program! Welcome to port %d." % port)
        app.run()

    except KeyboardInterrupt, SystemExit:
        for hook in configuration.hooks.shutdown:
            website = hook(website) or website
