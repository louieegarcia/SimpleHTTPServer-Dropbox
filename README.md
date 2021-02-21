# SimpleHTTPServer-Dropbox
Using the SimpleHTTPServer Python module, instead of serving files you can upload files to your machine via HTTP POST requests.

You can visit the webserver via a browser to upload a file or simply make a POST request via CURL to upload a file as well.
i.e. curl -F "data=@<path to file>" <webserver IP>:<webserver PORT>
