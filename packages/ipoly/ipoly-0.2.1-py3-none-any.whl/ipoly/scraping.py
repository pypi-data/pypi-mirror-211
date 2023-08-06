"""Provides routines for web scraping."""
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Literal

from bs4 import BeautifulSoup
from bs4.element import Tag
from pandas import DataFrame
from selenium.webdriver import Chrome

from ipoly.traceback import raiser


class Component(ABC):
    """Abstract class representing a Component with an operation method."""

    @abstractmethod
    def operation(self, df) -> tuple[DataFrame, int]:
        """Perform an operation and return the result as a string."""
        raiser("Default implementation of the operation method.")
        return DataFrame([0]), 0  # Default implementation


class Leaf(Component):
    """Concrete class representing a Leaf in a component tree structure.

    It extends the Component class and implements the operation method.
    """

    def __init__(self, driver, scrap_object, file, backward_moves) -> None:
        """Initialise a Leaf object.

        Args:
            driver: The driver object to interact with.
            scrap_object: The object to be scraped.
            file: The file where the data will be stored.
            backward_moves: The steps to go back in the navigation.
        """
        self.driver = driver
        self.scrap_object = scrap_object
        self.file = file
        self.backward_moves = backward_moves

    def operation(self, df) -> tuple[DataFrame, int]:
        """Perform an operation by scraping data and moving backward.

        Args:
            df: The dataframe to perform operations on.

        Returns:
            A tuple containing the updated dataframe and integer 0.
        """
        df = self.scrap_object(self.driver, df, self.file)
        for backward_move in self.backward_moves:
            backward_move = _value_finder(self.driver, backward_move)
            click_element(self.driver, *backward_move)
        return df, 0


class Composite(Component):
    """A component class that can store other components.

    This class is part of the Composite design pattern.

    Attributes:
        forward_moves: A list of moves to go forward in the web scraping process.
        driver: A selenium webdriver object.
        _children: A list of child Component objects.
        file: A string representing the file path to store the scraped data.
        scrap_object: A function to scrape data from the web page.
        backward_moves: A list of moves to go backward in the web scraping process.
    """

    def __init__(
        self,
        forward_moves,
        driver,
        file,
        scrap_object,
        backward_moves,
    ) -> None:
        """Initialises a Composite instance for web scraping.

        Args:
            forward_moves: A list of forward navigation moves to perform during web scraping.
            driver: A WebDriver instance for web navigation.
            file: The output file where scraped data will be stored.
            scrap_object: The scraping function to be used for data extraction.
            backward_moves: A list of backward navigation moves to perform during web scraping.
        """
        self.forward_moves = forward_moves
        self.driver = driver
        self._children: List[Component] = []
        self.file = file
        self.scrap_object = scrap_object
        self.backward_moves = backward_moves

    def add(self, component: Component) -> None:
        """Add a child component to the composite.

        Args:
            component (Component): The child component to add.
        """
        self._children.append(component)

    def operation(self, df: DataFrame) -> tuple[DataFrame, int]:
        """Perform the operation of the composite.

        It involves performing the operations of its child components and managing navigation in the web scraping process.

        Args:
            df: The dataframe to store the scraped data.

        Returns:
            The updated dataframe and the number of child components left to explore.
        """
        from time import sleep

        sleep(2)
        forward_move = _value_finder(self.driver, self.forward_moves[0])
        elements = self.driver.find_elements(
            "xpath",
            "//"
            + forward_move[0]
            + "[@"
            + forward_move[1]
            + "='"
            + forward_move[2]
            + "']",
        ) + self.driver.find_elements(
            "xpath",
            "//"
            + forward_move[0]
            + "[@"
            + forward_move[1]
            + "='"
            + forward_move[2]
            + " ']",
        )
        if not self._children:
            for _ in elements:
                if len(self.forward_moves) == 1:
                    self.add(
                        Leaf(
                            self.driver,
                            self.scrap_object,
                            self.file,
                            self.backward_moves,
                        ),
                    )
                else:
                    self.add(
                        Composite(
                            self.forward_moves[1:],
                            self.driver,
                            self.file,
                            self.scrap_object,
                            self.backward_moves,
                        ),
                    )
        elements[len(elements) - len(self._children)].click()
        sleep(3)
        df, exploring = self._children[0].operation(df)
        if not exploring:
            self._children = self._children[1:]
        return df, len(self._children)


def _value_finder(driver, tag):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(driver.page_source, "html.parser")
    args, _ = unknown_attributes_finder((tag[0], {tag[1]: tag[2]}), {}, soup)
    return tag[0], tag[1], args[1][tag[1]]


def move(
    scrap_object: Callable,
    forward_moves: Iterable[Iterable[str]],
    backward_moves: Iterable[Iterable[str]],
) -> Callable:
    """Return function for web scraping with forward and backward navigation.

    Args:
        scrap_object: The function to scrape data from the web page.
        forward_moves: A list of lists representing the forward movements in the web scraping process.
        backward_moves: A list of lists representing the backward movements in the web scraping process.

    Returns:
        The move function that performs the sequence of movements and returns the scraped data.
    """
    if not all(isinstance(el, list) for el in forward_moves):
        _forward_moves = [forward_moves]
    if not all(isinstance(el, list) for el in backward_moves):
        _backward_moves = [backward_moves]

    def move_function(driver, df, file):
        tree = Composite(_forward_moves, driver, file, scrap_object, _backward_moves)
        exploring = True
        while exploring:
            df, exploring = tree.operation(df)
        return df

    return move_function


def _scraping_driver(visible: bool = False, size=(1980, 1080)):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    if not visible:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={size[0]},{size[1]}")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )


def click_element(driver: Chrome, categorie: str, classe: str, information: str):
    """Clicks on an element in a web page using Selenium WebDriver.

    Args:
        driver: The Selenium WebDriver instance to interact with the web page.
        categorie: The category of the HTML element to be clicked.
        classe: The class of the HTML element to be clicked.
        information: The specific information that identifies the HTML element to be clicked.

    Raises:
        NoSuchElementException: If the element is not found on the page.
    """
    from selenium.common.exceptions import NoSuchElementException
    from time import sleep

    try:
        element = driver.find_element(
            "xpath",
            "//" + categorie + "[@" + classe + "='" + information + "']",
        )
    except NoSuchElementException:
        element = driver.find_element(
            "xpath",
            "//" + categorie + "[@" + classe + "='" + information + " ']",
        )
    element.click()
    sleep(3)


def unknown_attributes_finder(args: tuple, kwargs: dict, soup: BeautifulSoup):
    """Processes arguments for BeautifulSoup's find_all method.

    This function processes the input arguments for BeautifulSoup's find_all method,
    manages arguments of type dictionary, and handles the case where the attribute to
    search for is unknown and needs to be inferred from the provided BeautifulSoup object.

    Args:
        args: The positional arguments intended for the find_all method.
        kwargs: The keyword arguments intended for the find_all method.
        soup: A BeautifulSoup object where the HTML parsing has been done.

    Returns:
        tuple: A tuple containing the processed positional and keyword arguments.

    Raises:
        Exception: If multiple unknown attributes are requested to be looked for.
    """
    new_args = []
    new_kwargs = {}
    unknown_attr = None
    for arg in args:
        if type(arg) == dict:
            try:
                arg["class_"] = arg.pop("class")
            except KeyError:
                pass
            kwargs.update(arg)
        else:
            new_args.append(arg)
    for kwarg in kwargs.items():
        if type(kwarg[1]) == int:
            if unknown_attr:
                from ipoly.traceback import raiser

                raiser("You can't look for multiple unknown attributes.")
            if kwarg[0] == "class_":
                unknown_attr = ("class", kwarg[1])
            else:
                unknown_attr = kwarg
        else:
            new_kwargs[kwarg[0]] = kwarg[1]
    if unknown_attr:
        search = soup.find_all(new_args, new_kwargs)
        search = [
            elem[unknown_attr[0]] for elem in search if elem.has_attr(unknown_attr[0])
        ]
        attr_values = []
        for elem in search:
            if " ".join(elem) not in attr_values:
                attr_values.append(" ".join(elem))
        if attr_values != []:
            new_args.append(
                {unknown_attr[0]: attr_values[min(unknown_attr[1], len(attr_values))]},
            )
    return new_args, new_kwargs


def _find_object(tag: Tag, object_type: Literal["text", "href"]) -> str:
    """Helper function to extract the desired data from a BeautifulSoup tag.

    Args:
        tag: A BeautifulSoup tag.
        object_type: The type of data to extract from the tag ("text" or "href").

    Returns:
        The extracted data.
    """
    match object_type:
        case "text":
            return tag.text.strip()
        case "href":
            return tag["href"]


def find_all_object(*args, object_type: str = "text", **kwargs) -> Callable:
    """Generates a function to find tags and retrieve specified object types.

    Args:
        *args: Positional arguments to pass to BeautifulSoup's find_all method.
        object_type: The type of data to extract from the tags ("text" or "href").
        **kwargs: Keyword arguments to pass to BeautifulSoup's find_all method.

    Returns:
        A function that takes a BeautifulSoup object and returns a list of the extracted data.
    """
    from re import compile as re_compile

    def func(soup):
        nonlocal args, kwargs
        args, kwargs = unknown_attributes_finder(args, kwargs, soup)
        args = [
            arg
            if type(arg) != dict
            else {k: re_compile(v + r" *") for k, v in arg.items()}
            for arg in args
        ]
        return [
            _find_object(tag, object_type) for tag in soup.find_all(*args, **kwargs)
        ]

    return func


def scrap(*actions: tuple[str, Any]):
    """Define a function to scrape data from a webpage using BeautifulSoup.

    Args:
        *actions: A sequence of tuples, each containing a column name and a scraping function.

    Returns:
        A function that takes a web driver, a DataFrame, and a file path, then scrapes data from the webpage.
    """
    from bs4 import BeautifulSoup
    from pandas import concat, DataFrame
    from ipoly.file_management import save

    def scrap_function(driver, df, file):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        scraped = dict()
        for action in actions:
            scraped[action[0]] = action[1](soup)
        df = concat([df, DataFrame(scraped)], ignore_index=True)
        save(df, file)
        return df

    return scrap_function


def scraper(
    url: str,
    file: str,
    scrap_object,
    visible: bool = False,
    size: tuple[int, int] = (1980, 1080),
):
    """Scrape data from a website and store it into a file.

    Args:
        url: The URL of the website to scrape data from.
        file: The path of the file where to store the scraped data.
        scrap_object: The object to be scraped.
        visible: Whether the web driver should be visible or not. Defaults to False.
        size: The size of the web driver's window. Defaults to (1980, 1080).
    """
    from time import sleep
    from pandas import DataFrame
    from ipoly.file_management import load

    driver = _scraping_driver(visible, size)
    try:
        df = load(file)
    except FileNotFoundError:
        df = DataFrame(dtype="object")

    driver.get(url)
    sleep(3)
    scrap_object(driver, df, file)
