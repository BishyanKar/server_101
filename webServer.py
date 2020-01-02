from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi,os,settings
from io import BytesIO

tasklist = []

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if(self.path.endswith('/')):
            if(self.path == '/'):
                self.path = '/index.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file = 'file not found'    
                self.send_error(404)
            obj = "<ul>"
            tasklist = os.listdir()
            for i in range(len(tasklist)):
                obj += '<li><a type="file" href="/'+tasklist[i]+'"download>'+tasklist[i]+'</a></li><br><br>'
            
            obj += '</ul>'
            self.send_header('content-type','')
            self.end_headers()        
            self.wfile.write(bytes(file,'utf-8'))
            self.wfile.write(bytes(obj,'utf-8'))

        elif(self.path.endswith('/index/task')):
            self.path = '/task.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file = 'file not found'    
                self.send_error(404)
            self.send_header('content-type','')
            self.end_headers()

            self.wfile.write(bytes(file,'utf-8'))
        else:
            #print('entered else block')
            try:
                file = open(self.path[1:],'rb').read()
                self.send_response(200)
            except Exception as e:
                print(e)
                file = 'file not found'    
                self.send_error(404)

            self.send_header('content-type','')
            self.send_header('Location','/')
            self.end_headers()
            try:
                print('trying to write file')
                self.wfile.write(file)
            except Exception as e:
                print('Exception',e)

    def do_POST(self):
        if(self.path.endswith('/new')):
            ctype , pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'],'utf-8')
            content_length = int(self.headers['Content-Length'])
            pdict['CONTENT-LENGTH'] = content_length

            if(ctype == 'multipart/form-data'):
                fields = cgi.parse_multipart(self.rfile,pdict)
                new_task = fields.get('t_name')
                filename = fields.get('e_name')
                redirect_to = fields.get('r_link')
                print(filename[0])
                with open(filename[0]+'','wb') as f:
                    f.write(new_task[0])
                
            self.send_response(301) 
            self.send_header('content-type','')   
            self.send_header('Location','/'+redirect_to[0])
            self.end_headers()

httpd = HTTPServer((settings.host,settings.port),Serv)
print('serving at : ',settings.port)
httpd.serve_forever()