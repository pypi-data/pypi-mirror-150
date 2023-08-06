# urlToHTML
Save your favorite site, blog, html in just two lines of code. 


This is an example project that is used to demonstrate how to publish Python packages on PyPI. To take a look at the step by step guide on how to do so, make sure you read my article on my personal blog.

# Installing
pip install urlToHTML

# Usage
```
url = 'https://blog.octachart.com/how-to-deploy-a-docz-site-on-render'

from urltohtml import Blog 
new = Blog().save(url, "file")
```

You don't have to add file extension to the second parameter.

So running the script automatically creates ```file.html```

🌟 ♥ Hope You Found This Useful 🌟 ♥
