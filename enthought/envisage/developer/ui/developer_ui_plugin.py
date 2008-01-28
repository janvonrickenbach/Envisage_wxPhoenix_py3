""" The developer UI plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class DeveloperUIPlugin(Plugin):
    """ The developer UI plugin.

    This plugin contains the UI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # Extension points Ids.
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS        = 'enthought.envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    id   = 'enthought.envisage.developer.ui'
    name = 'Developer UI'

    #### Extension point contributions ########################################

    # Perspectives.
    perspectives = List(extension_point=PERSPECTIVES)

    # Views.
    views = List(extension_point=VIEWS)

    ###########################################################################
    # 'WorkbenchPlugin' interface.
    ###########################################################################

    def _views_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.ui.view.api import \
             ApplicationBrowserView
        
        return [ApplicationBrowserView]

    def _perspectives_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.ui.perspective.api import \
             DeveloperPerspective

        return [DeveloperPerspective()]
    
#### EOF ######################################################################
