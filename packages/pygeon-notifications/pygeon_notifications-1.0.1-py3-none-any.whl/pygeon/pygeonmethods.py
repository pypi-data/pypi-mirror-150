import requests

class Pygeon:
    
    def __init__(self, ppk, context=None):
        """Main class for creating a Pygeon object with methods to trigger push notifications

        :param ppk: Your pygeon private key
        :type ppk: string
        :param context: reference string to use as a convenience to identify caller script that shows up in notifications, defaults to None
        :type context: string, optional
        """
        
        self.ppk = ppk
        self.context = context
        self.server_url = "https://pygeon.io/api/alert"
        
    def send(self, title, desc=None):
        """method to send push notification to your devices

        :param title: Title of the push notification
        :type title: string
        :param desc: Description of the push notification, defaults to None
        :type desc: string, optional
        :return: response tuple containing success status and response text
        :rtype: (bool, string)
        """
        

        if desc and self.context:
            data = {"ppk": self.ppk, "title": title, "desc": desc, "context": self.context}
        elif desc:
            data = {"ppk": self.ppk, "title": title, "desc": desc}
        elif self.context:
            data = {"ppk": self.ppk, "title": title, "context": self.context}
        else:
            data = {"ppk": self.ppk, "title": title}
        
        res = requests.post(self.server_url, json = data)
        print(res.text)
        return res.status_code==200, res.text



if __name__ == "__main__":
    my = Pygeon("YOUR_PRIVATE_KEY", context="Cool Context")
    my.send(f"Cool Title", "Cooler body")