import requests

class Blog:        
    def save(self, url, file):
        try:
            response = requests.get(url, allow_redirects=True)

            with open(file + ".html", 'wb') as output:
                output.write(response.content)
            print("--DONE--")
        except Exception as e:
            print("Error : ",e)

          
   


