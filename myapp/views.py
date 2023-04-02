from django.shortcuts import render, HttpResponse, redirect
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
# Create your views here.
nextId = 4
topics=[
    {'id':1, 'title':'routing','body':'Routing is..'},
    {'id':2, 'title':'view','body':'View is..'},
    {'id':3, 'title':'Model','body':'Model is..'},
]

def HTMLTemplate(article, id=None):
    global topics
    ol=''
    delete=''
    if id != None:
        delete=f'''
            <li>
                <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id} />
                <input type="submit" value="Delete" />
                </form>
            </li>
            <li>
                <a href="/update/{id}">update</a>
            </li>
        '''
    for topic in topics:
        ol+=f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {article}
        <ul>
            <li><p><a href="/create">create</a></p></li>
            {delete}
        </ul>
    </body>
    </html>
    '''
def index(request):
    global topics
    article = '''
    <h2>Welcome</h2>
    Hello,Django!
    '''
    # template= loader.get_template('myapp/index.html')
    context = {'topics': topics}
    return render(request, 'myapp/index.html', context)
# HttpResponse(template.render(request)) 
# HttpResponse(HTMLTemplate(article))
@csrf_exempt
def create(request):
    global nextId
    if request.method=='GET':
         article = f'''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></input></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" /></p>
            </form>
        '''
         return HttpResponse(HTMLTemplate(article))
    elif request.method=='POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title,"body":body}
        topics.append(newTopic)
        url='/read/'+str(nextId)
        nextId += 1
        return redirect(url)
    
def read(request, id):
    global topics
    article =''
    for topic in topics:
        if str(topic["id"])==id:
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'

    return HttpResponse(HTMLTemplate(article,id))

@csrf_exempt
def delete(request):
    global topics
    newtopics = []
    if request.method=='POST':
        id = request.POST['id']
        for topic in topics:
            if int(id) != topic['id']:
                newtopics.append(topic)
        topics = newtopics
    return redirect('/')

@csrf_exempt
def update(request, id):
    global topics
    title=''
    body=''
    if request.method=='GET':
         for topic in topics:
             if str(topic["id"])==id:
                 title=topic['title']
                 body=topic['body']
                 article = f'''
                 <form action="/update/{id}/" method="post">
                    <p><input type="text" value={title} name="title" placeholder="title"></input></p>
                    <p><textarea name="body" placeholder="body">{body}</textarea></p>
                    <p><input value="edit" type="submit" /></p>
                 </form>
                 '''
                 return HttpResponse(HTMLTemplate(article))
    elif request.method=='POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if str(topic["id"])==id:
                topic['title']=title
                topic['body']=body
        return redirect(f'/read/{id}')