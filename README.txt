Installation:

1.  Close all instance of Maya.

2.  Copy updateReferenceTool.py to:

        Windows: \Documents\maya\version\scripts
        Linux: $HOME/Library/Preferences/Autodesk/maya/version/scripts

3.  Launch Maya

4.  Execute the following in a Maya:

import updateReferenceTool as uRef
uRef.UpdateReference()