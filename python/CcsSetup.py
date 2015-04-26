import os
from collections import OrderedDict
import siteUtils

class CcsSetup(OrderedDict):
    def __init__(self, configFile):
        super(CcsSetup, self).__init__()
        self['tsCWD'] = os.getcwd()
        self['labname'] = siteUtils.getSiteName()
        self._read(configFile)
        self['CCDID'] = os.environ["LCATR_UNIT_ID"]
    def _read(self, configFile):
        if configFile is None:
            return
        configDir = siteUtils.configDir()
        for line in open(configFile, 'r'):
            key, value = line.strip().split("=")
            self[key.strip()] = os.path.join(configDir, value.strip())
    def __call__(self):
        """
        Return the setup commands for the CCS script.
        """
        # Set local variables.
        commands = ['%s = %s' % item for item in self.items()]
        # Append path to python libraries used by the jython code
        commands.append('import sys')
        commands.append('sys.path.append(%s)' % siteUtils.pythonDir())
        return '\n'.join(commands)

if __name__ == '__main__':
    os.environ['LCATR_UNIT_ID'] = '112-03'
    setup = CcsSetup(None)

    print setup()
