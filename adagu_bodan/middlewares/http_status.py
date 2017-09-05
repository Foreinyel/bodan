from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest

class HttpStatusMiddleware(object):

    @classmethod
    def process_response(self,request,response,spider):
        http_status = response.status
        url = request.url
        html_file = open('cache/' + url.replace('/','+').replace(':','+'),'a')
        html_file.write(response.body)
        html_file.flush()
        html_file.close()
        if http_status != 200:
            raise IgnoreRequest("request_err")
        return response