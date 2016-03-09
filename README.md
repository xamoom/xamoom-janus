This framework is developed for you by [xamoom](https://xamoom.com) in Austria with <3

xamoom-janus is a lightweight Python framework to easily build RESTful [json:api](http://jsonapi.org/) webservices on top of frameworks like [Bottle](http://bottlepy.org/) or [Flask](http://flask.pocoo.org/). It takes care of generating valid json:api messages from your internal python objects and also the other way around. There is no need for you as a developer anymore to take care about rendering or parsing JSON. Just work with your objects and let janus do the json:api magic.

Because janus is designed to be an extension to existing Python web frameworks this will basically work the same with other frameworks than Bottle or Flask, like [CherryPy](http://www.cherrypy.org/) or [WebPy](http://www.cherrypy.org/).

# Example using Bottle
All you have to do is add a jsonapi decorator to your service method and let the service method return a JanusResponse object containing your python data object, or list of objects, and also your message class, that defines how your object is mapped to the json:api message.

```python
@bottle.route('/posts/<entity_id>', method=['GET']) #Decorator to make use of Bottle.
@jsonapi(success_status=200,include_relationships=True) #Tell xamoom-janus to make this a json:api method.
def get(entity_id):
    #load object by given id from your data source
    post = Post.get_by_id(entity_id)
    
    #generate response using the post object and the message type it should be mapped to.
    resp = JanusResponse(
                            data=post,
                            message=PostMessage
                        ) 
    
    return resp #simply return the message object. Janus takes care of the rest.
```
For more information please head over to the [Wiki](https://github.com/xamoom/xamoom-janus/wiki)
