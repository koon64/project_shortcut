# Python Project API
Use this to build python projects

### Methods

#### get_args()
Use this to requests a certain arg from the user upon proj request

There are 2 rules:

You **MUST** merge the parent's arguments when you return args

You **MUST** include your args after the parent's args

```python
return {
    **super().get_args(),
    **{
        'dijango_version': 'latest'
    }
}
```
