# coding: utf-8

import misaka as m


class JuneRenderer(m.HtmlRenderer, m.SmartyPants):
    def autolink(self, link, is_email):
        title = link.replace('http://', '').replace('https://', '')

        #: youtube.com
        pattern = r'http://www.youtube.com/watch\?v=([a-zA-Z0-9\-\_]+)'
        match = re.match(pattern, link)
        if not match:
            pattern = r'http://youtu.be/([a-zA-Z0-9\-\_]+)'
            match = re.match(pattern, link)
        if match:
            value = ('<iframe width="560" height="315" src='
                     '"http://www.youtube.com/embed/%(id)s" '
                     'frameborder="0" allowfullscreen></iframe>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'id': match.group(1), 'link': link, 'title': title}
            return value

        #: gist support
        pattern = r'(https?://gist.github.com/[\d]+)'
        match = re.match(pattern, link)
        if match:
            value = ('<script src="%(link)s.js"></script>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'link': match.group(1), 'title': title}
            return value

        #: vimeo.com
        pattern = r'http://vimeo.com/([\d]+)'
        match = re.match(pattern, link)
        if match:
            value = ('<iframe width="500" height="281" frameborder="0" '
                     'src="http://player.vimeo.com/video/%(id)s" '
                     'allowFullScreen></iframe>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'id': match.group(1), 'link': link, 'title': title}
            return value

        if is_email:
            return '<a href="mailto:%(link)s">%(link)s</a>' % {'link': link}

        return '<a href="%s" rel="nofollow">%s</a>' % (link, title)


def rich_markdown(text):
    renderer = JuneRenderer(flags=m.HTML_ESCAPE)
    ext = (
        m.EXT_NO_INTRA_EMPHASIS | m.EXT_FENCED_CODE | m.EXT_AUTOLINK |
        m.EXT_TABLES | m.EXT_STRIKETHROUGH
    )
    md = m.Markdown(renderer, extensions=ext)
    return md.render(text)