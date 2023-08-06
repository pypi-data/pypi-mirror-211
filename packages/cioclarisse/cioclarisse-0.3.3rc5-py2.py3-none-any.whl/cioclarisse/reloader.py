"""
For development mode, we can reload modules with a button push.



The button is available when the env var CONDUCTOR_MODE == "dev".
It reloads files imported by ConductorJob. Not ConductorJob itself.
"""
try:
    from importlib import reload 
except ImportError:
    from imp import reload
except ImportError:
    pass
    

from cioclarisse import utils, clarisse_config
from cioclarisse import (
    attr_docs,
    debug_ui,
    dependencies,
    validation,
    environment_ui,
    extra_uploads_ui,
    metadata_ui,
    frames_ui,
    instances_ui,
    validation_ui,
    notifications_ui,
    preview_ui,
    projects_ui,
    refresh,
    submission,
    submit_actions,
    task
)
 
reload(utils)
reload(clarisse_config)
reload(refresh)
reload(dependencies)
reload(debug_ui)
reload(validation)
reload(environment_ui)
reload(extra_uploads_ui)
reload(metadata_ui)
reload(validation_ui)
reload(frames_ui)
reload(instances_ui)
reload(task)
reload(notifications_ui)
reload(projects_ui)
reload(submission)
reload(submit_actions)
reload(attr_docs)
