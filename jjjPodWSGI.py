import jjjPod
from cgi import parse_qs, escape


def application(environ, start_response):
    #try:
        arguments = parse_qs(environ.get('QUERY_STRING', ''))
        show = arguments['show'][0]

        output = jjjPod.showToFeed(jjjPod.showFeedURL(show))
        length = "%d" % (len(output.encode('utf-8')))
        start_response('200 OK',
            [('Content-Type', 'application/rss+xml;charset=utf-8'),
             ('Content-Length', length)])

        print "Output: %s" % (output)
#        return['''%(body)s %(test)s
#''' % {'body': output, 'test': "Howdy Partner"}]
        string = "Hello"
        return [output.encode('utf-8')]

    #except:
    #    start_response('500 Internal Error', [('Content-Type', 'text/html')])
    #    return "<html><title>500 Internal Error</title><body><h1>500 Internal Error</h1><p>An error occurred.</p></body></html>"
