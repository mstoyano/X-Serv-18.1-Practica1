#!/usr/bin/python

import webapp
import urllib


class practica1(webapp.webApp):

    dicc_large = {}
    dicc_short = {}
    counter = 0

    def parse(self, request):

        metodo = request.split()[0]
        recurso = request.split()[1]

        if metodo == "POST":
            cuerpo = request.split("\r\n\r\n")[1].split('=')[1]
        else:
            cuerpo = ""

        return (metodo, recurso, cuerpo)

    def lista_url(self):

        lista = ""
        for url in self.dicc_large:
            lista = (lista + "<p><a href='" + url + "'>" + url +
                     "</a>" + " | " + "<a href='" + self.dicc_large[url] +
                     "'>" + self.dicc_large[url] + "</a></p>")
        return lista

    def process(self, parsedRequest):

        try:
            metodo, recurso, cuerpo = parsedRequest
        except TypeError:
            HttpCode = "400 Bad Request"
            HtmlBody = ("<html><body><h1> Error. Introduce una URL" +
                        "</h1></body></html>")
            return (HttpCode, HtmlBody)

        formulario = ('<form action="" method="POST">Intruduce una URL: '
                      + '<input type="text" name="url" value="" />'
                      + '<input type="submit" value="Acortar" /></form>')

        if metodo == "GET":
            if recurso == "/":
                head = ("<h1><center>Aplicacion web para acortar URLs" +
                        "</center></h1>")
                texto = "<h2> Lista de URLs acortadas: </h2>"
                HttpCode = "200 OK"
                HtmlBody = head + formulario + texto + self.lista_url()

            else:

                url_corta = "http://localhost:1234" + recurso

                try:
                    url_request = self.dicc_short[url_corta]
                except KeyError:
                    HttpCode = "404 Not Found"
                    head = ("<h1><center>Aplicacion web para acortar URLs" +
                            "</center></h1>")
                    HtmlBody = ("<html><body>" + head + "<b>La URL " +
                                "solicitada no existe</b></body></html>")
                    return (HttpCode, HtmlBody)

                HttpCode = "301 Moved Permanently"
                head = ("<h1><center>Aplicacion web para acortar URLs" +
                        "</center></h1>")
                HtmlBody = ('<html><body>' + head + '<head>Estas siendo' +
                            ' redirigido...<meta ' + 'http-equiv="refresh"' +
                            ' content="1; url=' + url_request + '" />')

        elif metodo == "POST" and recurso == "/":

            if cuerpo == "":
                HttpCode = "400 Bad Request"
                head = ("<h1><center>Aplicacion web para acortar URLs" +
                        "</center></h1>")
                HtmlBody = ("<html><body>" + head + "<b>Se ha producido" +
                            " un error con el formulario. Intentalo de " +
                            "nuevo!</b></body></html>")
                return (HttpCode, HtmlBody)

            url = urllib.unquote(cuerpo).decode('utf8')

            if url.split("://")[0] != "http" and url.split("://")[0] != "https":
                url = "http://" + url

            try:
                url_corta = self.dicc_large[url]
            except KeyError:
                url_corta = "http://localhost:1234/" + str(self.counter)
                self.counter = self.counter + 1
                self.dicc_large[url] = url_corta
                self.dicc_short[url_corta] = url

            HttpCode = "200 OK"
            head = "<h1><center>Aplicacion web para acortar URLs</center></h1>"
            HtmlBody = ("<html><body>" + head + "<p><a href='" + url +
                        "'>URL</a></p><p><a href='" + url_corta +
                        "'>URL Acortada</a></p></html></body>")

        else:
            httpCode = "400 Bad Request"
            HtmlBody = "<html><body>Metodo no permitido</body></html>"

        return (HttpCode, HtmlBody)

if __name__ == "__main__":
    try:
        TestWebApp = practica1("localhost", 1234)
    except KeyboardInterrupt:
        print "\n Aplicacion cerrada. Hasta la proxima!"
        