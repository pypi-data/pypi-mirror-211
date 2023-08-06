"""Provide features to create PDFs from Python."""
import os
from typing import Literal
from typing import Optional
from typing import TypeVar  # TODO waiting for PEP 673 to be released

# from typing import Self

Self_LaTeX = TypeVar("Self_LaTeX", bound="LaTeX")
from typing import Union

import pandas as pd
from pandas import DataFrame

from ipoly.traceback import raiser

available_functions = Literal["section", "subsection", "image", "text", "table"]


def _nothing(*_args, **_kwargs):
    """An empty function to put in a chain."""
    pass


class LaTeX:
    """Class to create PDFs from Python using LaTeX code compilation."""

    def __init__(self, *args, **kwargs):
        """Initializes instance, sets up document and chain attributes."""
        super().__init__(*args, *kwargs)
        self.doc = None
        self.chain = []

    def _image(
        self: Self_LaTeX,
        func,
        image_path: Optional[Union[str, tuple[str]]] = None,
        caption: Optional[Union[str, tuple[str]]] = None,
        centering: bool = True,
    ):
        """Loads an image or multiple images from provided paths.

        Adds them to the document as a figure or subfigures
        with optional captions, and then calls the provided function.

        Args:
            func: A function to call after the images have been added to the document.
            image_path: The path or paths to the image files. If a single string is provided,
                it is treated as a single path. If a tuple of strings is provided, it is
                treated as multiple paths. If None or not provided, no images are added.
            caption: The caption or captions to add to the images. If
                a single string is provided, it is used as the caption for all images. If a tuple of strings is
                provided, each string is used as the caption for the corresponding image. If None or not provided, no
                captions are added.
            centering: Whether to center the images in the document. Defaults to True.

        Returns:
            The provided function, to be called after the images have been added to the document.
        """
        from typing import Iterable
        from pylatex import Command
        from pylatex import Figure
        from pylatex import NoEscape
        from pylatex import SubFigure

        _image_path: tuple
        if isinstance(image_path, str):
            _image_path = (image_path,)
        elif isinstance(image_path, tuple):
            _image_path = image_path
        else:
            _image_path = ()

        _caption: tuple
        if isinstance(caption, str):
            _caption = (caption,)
        elif isinstance(caption, tuple):
            _caption = caption
        else:
            _caption = () if not _image_path else tuple([None] * len(_image_path))

        if _image_path == ():
            image_filenames: Iterable[str] = ()
        else:
            image_filenames = tuple(
                os.path.join(os.path.dirname(__file__), "..\\" + path)
                for path in _image_path
            )

        def image_func(*args, **kwargs):
            with self.doc.create(Figure(position="H")) as _figure:
                if centering:
                    self.doc.append(Command("centering"))
                for image_filename, image_caption in zip(image_filenames, _caption):
                    with self.doc.create(
                        SubFigure(width=NoEscape(rf"{1 / len(_caption)}\linewidth")),
                    ) as image:
                        image.add_image(
                            image_filename,
                            width=NoEscape(r"0.95\linewidth"),
                        )
                        if image_caption:
                            image.add_caption(image_caption)
            func(*args, *kwargs)

        return image_func

    def _section(self: Self_LaTeX, func, name: str):
        """A decorator that wraps a function within a LaTeX Section.

        Args:
            func: The function to wrap.
            name: The name of the Section.

        Returns:
            The decorated function, which when called, will execute
                within a LaTeX Section block.
        """
        from pylatex import Section

        def section_func(*args, **kwargs):
            """Add a section to the document."""
            with self.doc.create(Section(name)):
                func(*args, *kwargs)

        return section_func

    def _subsection(self: Self_LaTeX, func, name: str):
        """A decorator that wraps a function within a LaTeX Subsection.

        Args:
            func: The function to wrap.
            name: The name of the Subsection.

        Returns:
            callable: The decorated function, which when called, will execute
                      within a LaTeX Subsection block.
        """
        from pylatex import Subsection

        def section_func(*args, **kwargs):
            with self.doc.create(Subsection(name)):
                func(*args, *kwargs)

        return section_func

    def _text(self: Self_LaTeX, func, text: str):
        """Decorator that appends text to document before executing function.

        If the text string ends with ".txt", it is treated as a filename and the contents
        of the file are read and appended to the document.

        Args:
            func: The function to execute after appending the text.
            text: The text to append to the document. If this string ends with ".txt",
                        it is treated as a filename, and the contents of the file are read and appended.

        Returns:
            callable: The decorated function, which when called, will append the text and
                      then execute the original function.
        """
        if text[-4:] == ".txt":
            with open(text) as file:
                text = file.read()

        def text_func(*args, **kwargs):
            """Append text to the document."""
            self.doc.append(text)
            func(*args, *kwargs)

        return text_func

    def _table(
        self: Self_LaTeX,
        func,
        table: Union[str, DataFrame],
        name: str | None = None,
    ):
        """Loads a table from a file or DataFrame and applies transformations.

        Then, creates a LaTeX table from the data and adds it to the document.
        The provided function is called at the end with the table as an argument.

        Args:
            func: A function to call after the table has been processed.
            table: The source of the table data. If a string is provided, it is treated
            as a file path and the method attempts to load the file as a csv, pkl, or xlsx file. If a DataFrame
            is provided, it is used directly.
            name: The name of the table to be added to the document. Defaults to None.

        Raises:
            PermissionError: If the specified file is open and cannot be read.

        Returns:
            function: The provided function with the processed table as an argument.
        """
        from pylatex import Command
        from pylatex import NoEscape
        from pylatex import Table

        if type(table) is str:
            try:
                if table[-4:] == ".csv":
                    _table = pd.read_csv(table)
                elif table[-4:] == ".pkl":
                    _table = pd.read_pickle(table)
                elif table[-5:] == ".xlsx":
                    # noinspection PyArgumentList
                    _table = pd.read_excel(table, index_col=0)

            except PermissionError:
                raiser(
                    f"The file '{table}' is already open, please close it before trying again.",
                )
        else:
            _table = table

        _table = _table.applymap(
            lambda x: "".join(
                c
                for c in x
                if c
                in ["\t", "\n", "\r"]
                + list(map(chr, range(224, 249)))
                + list(map(chr, range(32, 35)))
                + list(map(chr, range(38, 127)))
            )
            if type(x) == str
            else x,
        )
        _table = _table.applymap(
            lambda x: x.replace("&", "\\&").replace("_", "\\_")
            if type(x) is str
            else x,
        )

        def table_func(*args, **kwargs):
            with self.doc.create(Table(position="H")) as table_figure:
                if name:
                    table_figure.add_caption(name)
                table_figure.append(Command("centering"))
                table_figure.append(NoEscape(_table.style.to_latex()))
            func(*args, *kwargs)

        return table_func

    def _chainer(self: Self_LaTeX):
        """Applies sequence of functions to a LaTeX document in reverse order.

        This method initializes a new LaTeX document with specific packages and settings. It then iterates over
        a sequence of functions stored in `self.chain` in reverse order, chaining them together by passing each
        function as the first argument to the next function. The chained functions are finally called with a
        placeholder function as an argument.

        The order of functions in `self.chain` should be such that the desired final state of the document is
        achieved when the functions are applied in reverse order.

        Note: The actual effect on the document depends on the specific functions stored in `self.chain`. This
        method does not modify `self.chain`; it only reads from it.
        """
        from pylatex import Document
        from pylatex import Package

        self.doc = Document(inputenc="latin1")
        self.doc.packages.append(
            Package(
                "geometry",
                options=["tmargin=1cm", "lmargin=1cm", "rmargin=1cm", "bmargin=2cm"],
            ),
        )
        self.doc.packages.append(Package("float"))
        self.doc.packages.append(Package("babel", options=["french"]))
        self.doc.append(r"\listoffigures")
        func_chain = _nothing
        for func, args, kwargs in reversed(self.chain):
            func_chain = func(func_chain, *args, *kwargs)
        func_chain(_nothing)

    def add(self, func: available_functions, *args, mandatory: bool = True, **kwargs):
        """Add a function to the chain based on the specified function type.

        Args:
            func: The type of function to add to the chain.
            *args: Variable length argument list.
            mandatory: Indicates whether the function is mandatory.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            Exception: If the provided path for image or table is incorrect or if the file extension is not handled.
        """
        funcs = {
            "section": self._section,
            "subsection": self._subsection,
            "image": self._image,
            "text": self._text,
            "table": self._table,
        }
        if func == "image":
            if type(args[0]) == str:
                paths = tuple(args[0])
            else:
                paths = args[0]
            for path in paths:
                if not os.path.exists(
                    os.path.join(os.path.dirname(__file__), "..\\" + path),
                ):
                    if not mandatory:
                        return None
                    raiser(f"The path '{path}' doesn't correspond to an image.")
            if (
                type(args[0]) == tuple
                and len(args) > 1
                and len(args[0]) != len(args[1])
            ):
                if not mandatory:
                    return None
                raiser(
                    "The number of images must be equal to the number of captions.",
                )
        if func == "table":
            if not os.path.exists(
                os.path.join(os.path.dirname(__file__), "..\\" + args[0]),
            ):
                if not mandatory:
                    return None
                raiser(
                    f"The provided path '{args[0]}' for the table is incorrect.",
                )
            elif args[0][-4:] not in (".csv", ".pkl", "xlsx"):
                if not mandatory:
                    return None
                raiser(f"The extension of the file '{args[0]}' is not handled.")
        self.chain.append((funcs[func], args, kwargs))

    def generate_pdf(self, filepath: str | None = None, compiler="pdfLaTeX"):
        """Generates a PDF from the current LaTeX document.

        Args:
            filepath: The path where the generated PDF will be saved. If None, the PDF is saved in the current directory with the default name.
            compiler: The LaTeX compiler to use. Default is "pdfLaTeX".
        """
        self._chainer()
        self.doc.generate_pdf(filepath, clean_tex=True, compiler=compiler)

    def generate_tex(self, filepath: str | None = None):
        """Generates a .tex file from the current LaTeX document.

        Args:
            filepath: The path where the generated .tex file will be saved. If None, the .tex file is saved in the current directory with the default name.
        """
        self._chainer()
        self.doc.generate_tex(filepath)
