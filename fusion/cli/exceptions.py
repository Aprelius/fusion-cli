class FusionCliException(Exception):
    message = 'Whoops! Something went wrong.'

    def __init__(self, message=None, *args, **kwargs):
        super(FusionCliException, self).__init__(*args, **kwargs)
        self.message = message or self.message


class InvalidRootPath(FusionCliException):
    message = 'The root path is invalid.'


class MatrixError(FusionCliException):
    message = 'Failed to execute the matrix configuration'


class MatrixValidationError(MatrixError):
    message = 'Failed to validate the matrix'


class ProjectNotInitialized(FusionCliException):
    message = "Project path '{}' was not initialized."

    def __init__(self, path, *a, **k):
        super(ProjectNotInitialized, self).__init__(
            self.message.format(path), *a, **k)
