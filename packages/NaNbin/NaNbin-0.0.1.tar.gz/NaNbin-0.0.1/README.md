# Pastebin

Create a Paste as a guest.

get your api_dev_key from [here](https://pastebin.com/doc_api#1)

````python
    paste = pb.Paste("<your api_dev_key>")
    paste.create_paste(title="test",
        text="test",
        format=pb.code_formats.PYTHON,
        expire=pb.expire_type.ONE_DAY,
        paste_type=pb.paste_type.PUBLIC)
````
Get your user key:

````python
    import pastebin as pb

    api_user_key = pb.Login("username","password","api_dev_key").get_user_key()
````

Create Paste as a registered user.

````python
    paste = pb.Paste("<your api_dev_key>",user_key="<your user_key>")
    paste.create_paste(title="test",
        text="test",
        format=pb.code_formats.PYTHON,
        expire=pb.expire_type.ONE_DAY,
        paste_type=pb.paste_type.PUBLIC)
````

get the paste url.

````python
    paste.get_paste()
````

list all pastes.

````python
    paste.list_pastes()
````

delete a paste.

````python
    paste.delete_paste(paste_key="<paste_key>")
````