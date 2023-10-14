DEFAULT_CONFIG = {
    'skin': 'moono-lisa',
    'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
    'toolbar_Full': [
        {'name': 'document', 'items': ['Source']},
        {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'SpellChecker', 'Undo', 'Redo']},
        {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList']},
    ],
    'toolbar': 'Full',
    'height': 300,
    'width': 'full',
}

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
        'toolbar_Full': [
            {'name': 'document', 'items': ['Source']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'SpellChecker', 'Undo', 'Redo']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList']},
        ],
        'toolbar': 'Full',
        'height': 300,
        'width': 'full',
    },
    'admin': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
        'toolbar_Full': [
            {'name': 'document', 'items': ['Source']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'extras', 'items': ['Language']},
            '/',
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Preview', 'NewPage', 'Maximize', 'ShowBlocks']},
        ],
        'toolbar': 'Full',
        'height': 400,
        'width': 'full',
        'extraPlugins': ','.join([
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}
