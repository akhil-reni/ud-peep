class AWSAssumeException(Exception):
    def __str__(self):
        return 'Failed to assume AWS account'
