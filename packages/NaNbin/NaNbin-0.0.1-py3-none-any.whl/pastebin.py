from bin_formats import * 
from requests import post

class Paste(object):
    def __init__(self,api_key:str,user_key=None) -> None:
        self.api_key = api_key
        self.paste_type = paste_type
        self.expire_type = expire_type
        self.code_formats = code_formats
        self.user_key = user_key
    def create_paste(self, title:str, text:str, format:code_formats, expire:expire_type,paste_type:paste_type) -> str:
        """create a paste

        Args:
            title (str): Set the title of the paste.
            text (str): Set the text of the paste.
            format (code_formats): Set the format of the paste.
            expire (expire_type): Set the expiration of the paste.
            paste_type (paste_type): Set the type of the paste.

        Returns:
            str: The url of the paste.
        """
        if self.user_key != None:
            data = {
            'api_user_key': self.user_key,
            'api_option': 'paste',
            'api_paste_code': text,
            'api_paste_name': title,
            'api_paste_format': format,
            'api_paste_private': paste_type,
            'api_paste_expire_date': expire,
            'api_dev_key': self.api_key,
            'api_paste_return_raw': '1'
            }
        else:
            data = {
            'api_option': 'paste',
            'api_paste_code': text,
            'api_paste_name': title,
            'api_paste_format': format,
            'api_paste_private': paste_type,
            'api_paste_expire_date': expire,
            'api_dev_key': self.api_key,
            'api_paste_return_raw': '1'
            }
        response = post('https://pastebin.com/api/api_post.php', data=data)
        return response.text

    def get_paste(self, url:str) -> str:
        if url.startswith("https://pastebin.com/"):
            url = url[21:]
            print(url)
        else:
            raise ValueError("The url is not valid.")
        """get a paste
            
            Args:
                url (str): The url of the paste.

            Returns:
                str: The text of the paste.
            **Note: You need to login to get a paste.**
        """
        if self.user_key != None:
            data = {
            'api_user_key': self.user_key,
            'api_option': 'show_paste',
            'api_dev_key': self.api_key,
            'api_paste_key': url
            }
        else:
            raise ValueError("You need to login to get a paste.")
        response = post('https://pastebin.com/api/api_raw.php', data=data)
        return response.text

    def delete_paste(self, url:str) -> str:
        """delete a paste

            Args:
                url (str): The url of the paste.
                    
            Returns:
                str: The text of the paste.
            **Note: You need to login to delete a paste.**
        """
        if self.user_key != None:
            data = {
            'api_user_key': self.user_key,
            'api_option': 'delete',
            'api_dev_key': self.api_key,
            'api_paste_key': url
            }
        else:
            raise ValueError("You need to login to delete a paste.")
        response = post('https://pastebin.com/api/api_post.php', data=data)
        return response.text
    
    def list_pastes(self) -> str:
        """list all pastes

            Returns:
                str: The text of the paste.
            **Note: You need to login to get a paste.**
        """
        if self.user_key != None:
            data = {
            'api_user_key': self.user_key,
            'api_option': 'list',
            'api_dev_key': self.api_key
            }
        else:
            raise ValueError("You need to login to list pastes.")
        response = post('https://pastebin.com/api/api_post.php', data=data)
        return response.text
