def DefaultArchitecture():
    return 'x86_64'


def DefaultCompiler(system):
    if system == 'Linux':
        return 'gcc'
    if system == 'Darwin':
        return 'gcc'
    if system == 'Windows':
        return 'vc150'
    raise RuntimeError('Unknown platform: %s' % system)


def DefaultVariant():
    return 'Debug'


def GetBuildFolder():
    return 'build'


def GetInstallFolder():
    return 'install'


def GetProjectFolder():
    return 'projects'


def GetSupportedArchitectures():
    return {
        'i386': ['i386'],
        'x86_64': ['x86_64', 'AMD64']
    }


def GetSupportedVariants():
    return ['Debug', 'Release']


def GetSupportedVisualStudioVersions():
    return ['vs2013', 'vs2015', 'vs2017', 'vs2019']
