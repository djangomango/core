module.exports = {
  build: {
    posthtml: {
      expressions: {
        delimiters: ['[[', ']]'],
        unescapeDelimiters: ['[[[', ']]]'],
      }
    },
    tailwind: {
      css: 'src/emails/css/tailwind.css',
      config: 'tailwind.maizzle.config.js',
    },
    templates: {
      source: 'src/emails/templates',
      destination: {
        path: '../templates/common/core/emails',
      },
    },
  },
  inlineCSS: true,
  prettify: true,
  removeUnusedCSS: false,
  shorthandInlineCSS: true,
  year: () => new Date().getFullYear(),
}