"""
scaffold
"""
try: # pyramid 1.0.X
    # "pyramid.paster.paste_script..." doesn't exist past 1.0.X
    from pyramid.paster import paste_script_template_renderer
    from pyramid.paster import PyramidTemplate
except ImportError:
    try: # pyramid 1.1.X, 1.2.X
        # trying to import "paste_script_template_renderer" fails on 1.3.X
        from pyramid.scaffolds import paste_script_template_renderer
        from pyramid.scaffolds import PyramidTemplate
    except ImportError: # pyramid >=1.3a2
        paste_script_template_renderer = None
        from pyramid.scaffolds import PyramidTemplate
import os


class PyramidAppEngineStarterTemplate(PyramidTemplate):
    _template_dir = "starter"
    summary = "Pyramid scaffold for appengine with pyjamas support"
    #template_renderer = staticmethod(paste_script_template_renderer)

    # taken from pyramid/scaffolds.PyramidTemplate
    def pre(self, command, output_dir, vars):
        vars['random_string'] = os.urandom(20).encode('hex')
        package_logger = vars['package']
        if package_logger == 'root':
            # Rename the app logger in the rare case a project is named 'root'
            package_logger = 'app'
        vars['package_logger'] = package_logger
        return PyramidTemplate.pre(self, command, output_dir, vars)

    def post(self, command, output_dir, vars):
        self.out('Welcome to pj_pyramid_appengine.  Go HACK!!!')
        return PyramidTemplate.post(self, command, output_dir, vars)

    def out(self, msg): # pragma: no cover (replaceable testing hook)
        print msg
