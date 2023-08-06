MSG_TEMPLATE = ('{} number found in template ({}) does not match '
                'with the number of {} paths ({}) in the list')


class InvalidPathError(Exception):
    def __init__(self, path):
        self.message = f'{path} is not a valid URL to an image source nor an existing ' \
                       'path to an image file'
        super().__init__(self.message)


class UnmatchedCellNumberError(Exception):
    def __init__(self, row_n, header_n):
        self.message = (f'Given cell number {row_n} does not match '
                        f'with the number of header cells {header_n}')
        super().__init__(self.message)


class UnmatchedImageNumberError(Exception):
    def __init__(self, temp_img_n, list_img_n):
        self.message = MSG_TEMPLATE.format('Image', temp_img_n, 'image', list_img_n)
        super().__init__(self.message)


class UnmatchedVideoNumberError(Exception):
    def __init__(self, temp_vid_n, list_vid_n):
        self.message = MSG_TEMPLATE.format('Video', temp_vid_n, 'video', list_vid_n)
        super().__init__(self.message)
