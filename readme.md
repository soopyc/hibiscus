###### readme shouldn't exist

wait...






















Nevermind, it existed. More details of this repo in the projects page.

# Selfhosting
You MAY selfhost this bot if you want.
#### How to selfhost
First, download python 3.6+ [here](https://www.python.org/downloads/)if you haven't. I suggest python 3.6.0 as its the language this bot is being developed in. Therefore, the chances of succeding the setup would be higher. (Also I have no \*\*\*\*\*\*\* idea how you live if you use python2.)

###### #####To be done.#####
## Flair config syntax!
Ok this is what a typical flair/role config at v0.0.1 looks like.
```json
{
    "877562412658462333":{
        "random":{
            "config":{
                "mode": "single"
            },
            "yes":{
                "id": 696969696969696969
            },
            "thing":{
                "id": 420420420420420420
            }
        }
    }
}
```
First, we have this ``"877562412658462333"``, which is just the server ID the roles are in.
The script will scan the config for that.
Then, we have this ``"random"``, which is the group name.
Further into the tree, we have ``"config"``. This defines the mode of the group, i.e. allow only one role per group or more than one.
Then, we have the id. The id is crucial for assigning the roles, since i haven't been able to role stuff properly, lol.

Here i brainstorm my ideas

