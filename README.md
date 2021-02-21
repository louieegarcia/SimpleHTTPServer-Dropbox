# SimpleHTTPServer-Dropbox
Using the SimpleHTTPServer Python module, instead of serving files you can upload files to your machine via HTTP POST requests.

You can visit the webserver via a browser to upload a file or simply make a POST request via CURL to upload a file as well.

i.e. `curl -F "data=@<path to file>" <webserver IP>:<webserver PORT>`

## Arguments
- LHOST

The IP the http/https server will listen on. (Default=0.0.0.0)

- LPORT

The PORT the http/https server will listen on. (Default=8000)

- SSLKEYFILE

Not supported yet

- SSLCERTFILE

Not supported yet
