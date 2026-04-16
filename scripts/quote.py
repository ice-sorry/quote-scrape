from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class Quote:
    """Contains information related to a personal quote.

    Attributes:
        text (str): The content of the quote.
        author (str): The person the quote is attributed to.
        tags (list): A list of tags that describe the quote.
    """
    def __init__(self, text, author, tags):
        self.text = text.strip('"' + "'" + '“' + '”')
        self.author = author
        self.tags = tags
    
    @classmethod
    def __from_element__(cls, quote_element: WebElement):
        text = quote_element.find_element(By.CLASS_NAME, "text").text
        author = quote_element.find_element(By.CLASS_NAME, "author").text
        tags = [t.text for t in quote_element.find_elements(By.CLASS_NAME, "tag")]
        
        return cls(text=text, author=author, tags=tags)
        
    @classmethod
    def __from_dict__(cls, data):
        return cls(
            text=data.get("text", None),
            author=data.get("author", None),
            tags=data.get("tags", None)
        )

    def __repr__(self):
        return f"Quote(text={self.text!r}, author={self.author!r}, tags={self.tags!r})"