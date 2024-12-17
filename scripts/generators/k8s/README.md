# Introduction

This project is intended to replace the run.sh and build.sh orginally included in APM game. It creates deployment files to let APM games run on kubernetes. It creates the required deployment, service and a config-map which holds the configuration for every service defined.

It also handles the deployment of databases and loaders. The AppDynamics specific part has been removed from the images and the build process.

## Info
port command: this will create a second service of type loadbalancer with the specified port as the external port
the service will always run on port 8080 internally and ther is always a service of type ClusterIP created mapping 80->8080

## Working
- Java services (multiple)
- dotNet services
- NodeJS services
- mysql db

## To Do (not orderd list)
- Other languages (dotnet, nodejs, php)
- dotNet sql call support
- add pyhton language
- build process and build scrips for the images
- loader
- db deployments (mysql, mongo)
- potentially update images
- slim down images
- resource limits
- support for passing annotations to service and deployments
- make the templating more flexible (the template building method)



## TechStuff
### Jinja2 templating
#### check for keys
In Jinja2 templates, you can check if a key exists in a dictionary using the in operator. This is useful when you want to conditionally display content based on the presence of a key in a dictionary passed to the template. Here’s how you can do it:

Example

Suppose you have a dictionary passed to the template called data, and you want to check if a key named my_key exists.
````
{% if 'my_key' in data %}
    <p>The key exists and its value is: {{ data['my_key'] }}</p>
{% else %}
    <p>The key does not exist.</p>
{% endif %}
````

Explanation
- {% if 'my_key' in data %}''': This line checks if 'my_key' is a key in the data dictionary. If it exists, the condition evaluates to True.
- '''{{ data['my_key'] }}''': If the key exists, you can safely access its value using this syntax.
- '''{% else %}''': This block executes if 'my_key' is not found in the dictionary.

#### jinja2 default values
you can provide a default value when accessing a dictionary key by using the default filter or the get method. This is helpful to avoid errors when a key might not exist and you want to ensure a fallback value is used.
Using the default Filter

The default filter can be applied directly in the template to provide a fallback value if a key doesn't exist or if the value is ```None```.

```
<p>The value is: {{ data['my_key'] | default('Default Value') }}</p>
```
You can also use the get method of dictionaries, which allows you to specify a default value directly.
```
<p>The value is: {{ data.get('my_key', 'Default Value') }}</p>
```