"""Provide routines for managing data in files."""
import glob
import os
from string import ascii_letters
from string import digits
from typing import Iterable
from typing import Literal
from typing import TypeVar  # TODO waiting for PEP 673 to be released

# from typing import Self

Self_ndarray = TypeVar("Self_ndarray", bound="ndarray")

import numpy as np
import pandas as pd

from ipoly.traceback import raiser

SILLY_DELIMITERS = frozenset(ascii_letters + digits + ".")


def caster(df: pd.DataFrame):
    """Cast automatically columns in DataFrames.

    The columns with a data type as object are casted automaticallyas float, int or Datatime according to their pattern.

    Args:
        df: The DataFrame to cast.
    """
    string_cols = [col for col, col_type in df.dtypes.items() if col_type == "object"]
    if len(string_cols) > 0:
        mask = df.astype(str).apply(
            lambda x: x.str.match(
                r"(\d{1,4}[-/\\\. ]\d{1,2}[-/\\\. ]\d{2,4})+.*",
            ).any(),
        )

        def excel_date(x):
            from xlrd.xldate import xldate_as_datetime

            # Warning : Date in the French format
            x = pd.to_datetime(x, dayfirst=True, errors="ignore")
            x = x.apply(
                lambda y: xldate_as_datetime(y, 0) if type(y) in (int, float) else y,
            )
            return x.astype("datetime64[ns]")

        df.loc[:, mask] = df.loc[:, mask].apply(excel_date)
        del mask
    string_cols = [col for col, col_type in df.dtypes.items() if col_type == "object"]
    for col in string_cols:
        try:
            try:
                df[col] = df[col].str.split(",").str.join(".").values.astype(float)
            except AttributeError:
                df[col] = df[col].values.astype(float)
        except (ValueError, TypeError):
            pass

    df = df.apply(
        lambda col: col
        if not (
            col.dtype in [np.dtype("float64"), np.dtype("float32"), np.dtype("float16")]
        )
        or col.isna().any()
        or pd.Series(col.apply(np.int64) == col).sum() != df.shape[0]
        else col.apply(np.int64),
        axis=0,
    )
    return df


def locate_files(file: str, recursive: bool = True) -> tuple[list[str], str | None]:
    """Returns a list of file paths matching the given pattern of file name(s).

    Args:
        file: The name (or pattern) of the file to be located.
        recursive: Whether to search recursively through subdirectories.

    Returns:
        A list of file paths matching the given file name and directory.
    """
    split_path = file.split(os.sep)
    if len(split_path) == 1:
        directory = "." + os.sep
    else:
        file = split_path[-1]
        directory = os.sep.join(split_path[:-1])
    del split_path
    file_format: str | None = file.split(".")[-1]
    if file[-7:] == ".nii.gz":
        file_format = "nii.gz"
    if file_format is not None and len(file_format) + 1 >= len(file):
        file_format = None
    if recursive:
        pathname = "**" + os.sep + directory + os.sep + "**" + os.sep + file
    else:
        pathname = directory + os.sep + file
    files = glob.glob(pathname, recursive=recursive)
    return (
        list(dict.fromkeys([file.replace("." + os.sep, "") for file in files])),
        file_format,
    )


def _create_cube(x, y, z, size=0.5):
    # Define the vertices of the cube
    vertices = np.array(
        [
            [x - size / 2, y - size / 2, z - size / 2],
            [x + size / 2, y - size / 2, z - size / 2],
            [x - size / 2, y + size / 2, z - size / 2],
            [x + size / 2, y + size / 2, z - size / 2],
            [x - size / 2, y - size / 2, z + size / 2],
            [x + size / 2, y - size / 2, z + size / 2],
            [x - size / 2, y + size / 2, z + size / 2],
            [x + size / 2, y + size / 2, z + size / 2],
        ],
    )

    # Define the faces of the cube
    faces = np.array(
        [
            [0, 1, 3],
            [0, 3, 2],
            [0, 1, 5],
            [0, 5, 4],
            [1, 3, 7],
            [1, 7, 5],
            [2, 3, 7],
            [2, 7, 6],
            [0, 2, 6],
            [0, 6, 4],
            [4, 5, 7],
            [4, 7, 6],
        ],
    )

    return vertices, faces


class ndarray(np.ndarray):
    """Custom ndarray class that inherits from numpy.ndarray.

    This class adds methods to make usage of ndarray easier.

    Attributes:
        Same attributes as numpy.ndarray
    """

    def __new__(cls, array):
        """Create a new instance of the custom ndarray class.

        Args:
            array: An array, any object exposing the array interface, or an object
                    whose __array__ method returns an array.

        Returns:
            ndarray: A new custom ndarray object.
        """
        from numpy import asarray

        obj = asarray(array).view(cls)
        return obj.cast()

    def show(self: Self_ndarray):
        """Display the array as an image or as a 3D volume plot."""
        import numpy as np

        arr = self.copy()
        if len(self.unique()) == 2:
            arr = arr.label()

        if len(arr.shape) == 2:
            from PIL.Image import fromarray
            from IPython.display import display

            display(fromarray(arr.scale(256)))
        elif len(arr.shape) == 3:
            num_non_zero_pixels = np.count_nonzero(arr)
            if num_non_zero_pixels > 60000:
                import ipywidgets as widgets
                from IPython.display import display
                from matplotlib.pyplot import figure, imshow, show, close, cm
                from matplotlib.colors import Normalize

                norm = Normalize(vmin=0, vmax=arr.max())
                cmap = cm.hsv
                arr = np.ma.masked_where(arr == 0, arr)
                cmap.set_bad(color="white")

                def _plot_func(slice_index, axis):
                    figure(figsize=(6, 6))
                    if axis == "x":
                        imshow(arr[slice_index, :, :], cmap="hsv", norm=norm)
                    elif axis == "y":
                        imshow(arr[:, slice_index, :], cmap="hsv", norm=norm)
                    else:  # 'z'
                        imshow(arr[:, :, slice_index], cmap="hsv", norm=norm)
                    show()
                    close()

                def _update_slice_range(*args):
                    if axis_selection.value == "x":
                        slice_slider.max = arr.shape[0] - 1
                    elif axis_selection.value == "y":
                        slice_slider.max = arr.shape[1] - 1
                    else:  # 'z'
                        slice_slider.max = arr.shape[2] - 1

                # add interactive slider and buttons
                axis_selection = widgets.Dropdown(
                    options=["x", "y", "z"],
                    value="x",
                    description="Axis:",
                )
                axis_selection.observe(_update_slice_range, "value")
                slice_slider = widgets.IntSlider(
                    min=0,
                    max=arr.shape[0] - 1,
                    step=1,
                    description="Slice:",
                )
                ui = widgets.HBox([slice_slider, axis_selection])
                out = widgets.interactive_output(
                    _plot_func,
                    {"slice_index": slice_slider, "axis": axis_selection},
                )
                display(ui, out)
            else:
                import plotly.graph_objs as go

                # Get the x, y, z coordinates of the points
                x, y, z = np.where(arr)
                values = arr[x, y, z]

                # Normalize the values to the range 0-1
                values = (values - np.min(values)) / (np.max(values) - np.min(values))

                # Create cubes for each point
                vertices = []
                faces = []
                for i in range(len(x)):
                    v, f = _create_cube(x[i], y[i], z[i], size=1.0)
                    vertices.extend(v)
                    faces.extend(f + 8 * i)
                # Create a Mesh3d plot
                mesh = go.Mesh3d(
                    x=[v[0] for v in vertices],
                    y=[v[1] for v in vertices],
                    z=[v[2] for v in vertices],
                    i=[f[0] for f in faces],
                    j=[f[1] for f in faces],
                    k=[f[2] for f in faces],
                    intensity=values,
                    colorscale="Viridis",
                    showscale=False,
                    flatshading=True,
                )

                # Configure the layout
                layout = go.Layout(
                    scene=dict(
                        xaxis_title="X",
                        yaxis_title="Y",
                        zaxis_title="Z",
                    ),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10),
                )

                # Create the Figure
                fig = go.Figure(data=[mesh], layout=layout)
                fig.show()
        else:
            print("Only 2D and 3D arrays are supported for visualisation.")

    def filter(
        self: Self_ndarray,
        lower_threshold: float | None = None,
        upper_threshold: float | None = None,
    ) -> Self_ndarray:
        """Filter an array based on lower and/or upper thresholds.

        This method filters the input array by setting values outside the specified
        range to 0. If only one of the thresholds is provided, it filters the array
        based on that single threshold.

        Args:
            lower_threshold: Lower threshold for filtering the array.
                If None, no lower threshold will be applied.
            upper_threshold: Upper threshold for filtering the array.
                If None, no upper threshold will be applied.

        Returns:
            Filtered array.

        Example:
            >>> a = ndarray([0, 1, 2, 3, 4, 5])
            >>> a.filter(lower_threshold=1, upper_threshold=4)
            array([0, 0, 2, 3, 0, 0])
        """
        # Create a boolean mask with all True values
        mask = np.ones_like(self, dtype=bool)

        # Update the mask based on the provided thresholds
        if lower_threshold is not None:
            mask &= self > lower_threshold
        if upper_threshold is not None:
            mask &= self < upper_threshold

        # Create a copy of the input array to avoid modifying the original array
        filtered_arr = self.copy()

        # Set values outside the specified range to 0
        filtered_arr[~mask] = 0

        return filtered_arr

    def scale(self: Self_ndarray, max_value) -> Self_ndarray:
        """Scale the array to a given max value, preserving relative values.

        This method scales the input array so that the maximum value becomes the specified
        max_value, while keeping the relative values intact.

        Args:
            max_value: The desired maximum value for the scaled array.

        Returns:
            Scaled array.

        Example:
            >>> ndarray([0, 1, 2, 3, 4, 5]).scale(10)
            array([ 0.,  2.,  4.,  6.,  8., 10.])
        """
        arr_min = self.min()
        arr_max = self.max()

        # Scale the array values
        scaled_arr = (self - arr_min) * (max_value / (arr_max - arr_min))

        return scaled_arr

    def bounding_boxes(self: Self_ndarray) -> list[tuple[float, float, float, float]]:
        """Compute the bounding boxes of the connected regions if binary.

        This method computes the bounding boxes of connected regions in a binary image.
        The input array must be 2-dimensional and binary.

        Returns:
            List of bounding boxes in the format (min_row, min_col, max_row, max_col).

        Raises:
            Exception: If the input array has more than 2 dimensions or is not binary.

        Example:
            >>> a = ndarray([
            ...     [0, 0, 1, 1, 0],
            ...     [0, 0, 1, 1, 0],
            ...     [0, 0, 0, 0, 1],
            ... ])
            >>> a.bounding_boxes()
            [(0, 2, 1, 3), (2, 4, 2, 4)]
        """
        if len(self.shape) != 2:
            raiser(
                f"Can't compute the bounding boxes with {len(self.shape)} dimensions.",
            )
        nb_uniques = len(self.unique())
        if nb_uniques > 2:
            raiser("Can only compute the bounding boxes of binary images.")
        return get_bounding_boxes_from_segmentation(self)

    def unique(self: Self_ndarray, *args, **kwargs) -> Self_ndarray:
        """Calls the numpy.unique function."""
        return np.unique(self, *args, **kwargs)

    def isin(self: Self_ndarray, *args, **kwargs) -> Self_ndarray:
        """Calls the numpy.isin function."""
        return ndarray(np.isin(self, *args, **kwargs))

    def binarize(self: Self_ndarray, elements: list[int] | range) -> Self_ndarray:
        """Binarize the array based on a list of specified elements or a range.

        This method sets the elements in the input array to 1 if they are in the
        specified list or range, and 0 otherwise.

        Args:
            elements: List of elements or range to be set to 1.

        Returns:
            Binarized array.

        Example:
            >>> ndarray([1, 2, 3, 4, 5]).binarize([2, 3, 4])
            array([0, 1, 1, 1, 0])
        """
        return set_elements_to_binary(self, elements)

    def cast(self: Self_ndarray) -> Self_ndarray:
        """Cast a float array to int if all elements are whole values.

        This method checks if all elements in the input array are whole values and
        casts the array to int if they are.

        Returns:
            Cast array if all elements are whole values, otherwise the original array.

        Example:
            >>> ndarray([1.0, 2.0, 3.0]).cast()
            array([1, 2, 3])
        """
        return cast_float_to_int_if_whole(self)

    def normalise(
        self: Self_ndarray,
        min_value: float,
        max_value: float,
        clip_min: float | None = None,
        clip_max: float | None = None,
    ) -> Self_ndarray:
        """Normalise and clip the array between specified min and max values.

        This method normalises the input array between the specified min and max values,
        with optional clipping before normalisation.

        Args:
            min_value: Minimum value after normalisation.
            max_value: Maximum value after normalisation.
            clip_min: Minimum value to clip before normalisation.
            clip_max: Maximum value to clip before normalisation.

        Returns:
            Normalised array.

        Example:
            >>> ndarray([0, 1, 2, 3, 4, 5]).normalise(0, 1)
            array([0. , 0.2, 0.4, 0.6, 0.8, 1. ])
        """
        return normalise_array(
            self,
            min_value,
            max_value,
            clip_min,
            clip_max,
        )

    def round(self: Self_ndarray, *args, **kwargs) -> Self_ndarray:
        """Evenly round to the given number of decimals.

        Args:
            *args: Variable length argument list passed to np.round.
            **kwargs: Arbitrary keyword arguments passed to np.round.

        Returns:
            A new numpy array with elements rounded to the specified number of decimals.
        """
        return np.round(self, *args, **kwargs)

    def polygon(self: Self_ndarray, threshold_area: int = 0) -> list[list[float]]:
        """Converts the segmentation mask into polygonal representation.

        Args:
            threshold_area: The minimum contour area threshold for including a polygon.

        Returns:
            A list of polygons where each polygon is represented as a list of (x, y) coordinates.
        """
        from cv2 import findContours, contourArea, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE

        if self.ndim != 2 or not np.all(np.in1d(self, [0, 1])):
            raiser("The input mask must be a 2D binary array.")
        if self.dtype != np.uint8:
            self = self.astype(np.uint8)

        H, W = self.shape
        contours, _ = findContours(self, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

        polygons = []
        for cnt in contours:
            if contourArea(cnt) > threshold_area:
                polygon = []
                for point in cnt:
                    x, y = point[0]
                    polygon.append(x / W)
                    polygon.append(y / H)
                polygons.append(polygon)

        return polygons

    def crop_center(self: Self_ndarray, crop_shape: tuple, axes: tuple) -> Self_ndarray:
        """Crop a multi-dimensional array around the center.

        This function takes an n-dimensional numpy array, a desired crop shape,
        and the axes on which the cropping should be applied. It returns a new
        array that is a centered crop of the input array.

        Args:
            crop_shape: The desired shape of the crop. The length of the
                tuple should match the length of the `axes` argument.
            axes: The axes on which the cropping should be applied.

        Returns:
            np.ndarray: The cropped array.

        Raises:
            ValueError: If the length of `crop_shape` and `axes` do not match.
            IndexError: If a cropping dimension exceeds the size of the array along an axis.
        """
        if len(crop_shape) != len(axes):
            raiser("`crop_shape` and `axes` must have the same length.", ValueError)

        slices = [slice(None)] * self.ndim
        for ax, crop in zip(axes, crop_shape):
            start = self.shape[ax] // 2 - crop // 2
            if start < 0 or start + crop > self.shape[ax]:
                raiser(
                    f"Cropping dimension {crop} exceeds size of the array along axis {ax}.",
                    IndexError,
                )
            slices[ax] = slice(start, start + crop)

        return self[tuple(slices)]

    def label(self: Self_ndarray) -> Self_ndarray:
        """Calls the measure.label from scikit-image."""
        from skimage.measure import label as sk_label

        return ndarray(sk_label(np.array(self)))

    def contour(self: Self_ndarray) -> Self_ndarray:
        """Return the contour of the image."""
        from scipy.ndimage import binary_erosion

        if self.dtype == np.bool_:
            self = self.astype(int)
        return self - binary_erosion(self)

    def count(self: Self_ndarray) -> int:
        """Call the count_nonzero function from numpy."""
        return np.count_nonzero(self)


def get_bounding_boxes_from_segmentation(
    arr: np.ndarray | ndarray,
) -> list[tuple[float, float, float, float]]:
    """Extracts bounding boxes from a segmented 2D array.

    The array is supposed to have clusters of non-zero values representing objects of interest.
    The function labels these clusters and computes their bounding boxes in Darknet format:
    (center_x, center_y, width, height), where all values are
    normalized with respect to the dimensions of the input array.

    Args:
        arr: A 2D numpy array representing the segmented image.

    Returns:
        A list of tuples representing the bounding boxes of detected objects in Darknet format.
    """
    from scipy.ndimage import label

    # Label the clusters
    labeled, num_clusters = label(arr)

    # Initialize an empty list to store bounding boxes
    bounding_boxes = []

    # Loop over each cluster
    for cluster_id in range(1, num_clusters + 1):
        # Get the coordinates of the points in the current cluster
        coords = np.argwhere(labeled == cluster_id)

        # Compute the bounding box
        min_coords = coords.min(axis=0)
        max_coords = coords.max(axis=0)

        # Calculate the center, width, and height of the bounding box
        center_x = (min_coords[1] + max_coords[1]) / 2
        center_y = (min_coords[0] + max_coords[0]) / 2
        width = max_coords[1] - min_coords[1]
        height = max_coords[0] - min_coords[0]

        # Normalize the values with respect to the image dimensions
        img_width, img_height = arr.shape[1], arr.shape[0]
        center_x /= img_width
        center_y /= img_height
        width /= img_width
        height /= img_height

        # Add the bounding box to the list in Darknet format
        bounding_boxes.append((center_x, center_y, width, height))

    return bounding_boxes


def normalise_array(
    arr: np.ndarray | ndarray,
    min_value: float,
    max_value: float,
    clip_min: float | None = None,
    clip_max: float | None = None,
) -> np.ndarray:
    """Normalize an array between specified minimum and maximum values.

    Clip the input array if a clips value are provided.

    Args:
        arr: The input numpy array to be normalized.
        min_value: The desired minimum value for the normalized array.
        max_value: The desired maximum value for the normalized array.
        clip_min: The minimum value allowed in the input array before normalization.
        clip_max: The maximum value allowed in the input array before normalization.

    Returns:
        The normalized numpy array.
    """
    if clip_min or clip_max:
        arr = np.clip(arr, a_min=clip_min, a_max=clip_max)

    arr_min = arr.min()
    arr_max = arr.max()

    normalized_arr = (arr - arr_min) * (max_value - min_value) / (
        arr_max - arr_min
    ) + min_value

    return normalized_arr


def cast_float_to_int_if_whole(arr: np.ndarray | ndarray) -> np.ndarray | ndarray:
    """Casts a ndarray to int if values are whole values and dtype is float.

    Args:
        arr: The input ndarray.

    Returns:
        The ndarray with dtype as int if all values were whole and dtype was float,
            otherwise the original ndarray.
    """
    if arr.dtype in [np.dtype("float64"), np.dtype("float32"), np.dtype("float16")]:
        if np.all(np.mod(arr, 1) == 0):
            return arr.astype(int)

    return arr


def set_elements_to_binary(
    arr: np.ndarray | ndarray,
    elements: list[int] | range,
) -> np.ndarray | ndarray:
    """Binarize a tensor from a values.

    Sets the elements of the input ndarray to 1 if they are in the input list or range,
    and 0 otherwise.

    Args:
        arr: The input ndarray.
        elements: A list of integers or a range of integers to check against the elements in the input ndarray.

    Returns:
        The modified ndarray with binary values.
    """
    if not isinstance(elements, Iterable):
        raise ValueError("elements must be a list or a range")

    element_set = list(set(elements))
    arr_binary = np.where(np.isin(cast_float_to_int_if_whole(arr), element_set), 1, 0)
    if type(arr) == np.ndarray:
        return arr_binary
    return ndarray(arr_binary)


def _load_dicom(filenames: list[str]) -> tuple[ndarray, dict]:
    """Load a series of DICOM files and return a 3D NumPy array.

    This function takes a list of filenames corresponding to DICOM files, reads them,
    sorts them based on their position in the 3D volume, and stacks them into a single
    3D NumPy array.

    Args:
        filenames: A list of strings representing the file paths of the DICOM files to be loaded.

    Returns:
        A 3D NumPy array of shape (Rows, Columns, Slices) containing the pixel data from the DICOM files.

    Example:
        >>> dicom_files = ["file1.dcm", "file2.dcm", "file3.dcm"]
        >>> img = _load_dicom(dicom_files)
        >>> img.shape
        (512, 512, 3)
    """
    from operator import itemgetter
    from pydicom.dataset import FileDataset
    from pydicom import read_file

    def _thru_plane_position(dcm: FileDataset) -> float:
        """Calculate the position of a DICOM slice along the normal vector.

        This function takes a pydicom FileDataset object and calculates its position
        along the normal vector (perpendicular to the image plane). This position is
        useful for determining the order of slices in a 3D volume.

        Args:
            dcm: A pydicom FileDataset object containing the metadata of a DICOM file.

        Returns:
            The position of the DICOM slice along the normal vector.

        Example:
            >>> import pydicom
            >>> dcm = pydicom.read_file("file1.dcm")
            >>> position = _thru_plane_position(dcm)
            >>> position
            45.0
        """
        orientation = tuple(float(o) for o in dcm.ImageOrientationPatient)
        position = tuple(float(p) for p in dcm.ImagePositionPatient)
        rowvec, colvec = orientation[:3], orientation[3:]
        normal_vector = np.cross(rowvec, colvec)
        slice_pos = np.dot(position, normal_vector)
        return slice_pos

    dcm_slices = [read_file(fname, force=True) for fname in filenames]
    # Extract position for each slice to sort and calculate slice spacing
    dcm_slices = [(dcm, _thru_plane_position(dcm)) for dcm in dcm_slices]
    dcm_slices_sorted = sorted(dcm_slices, key=itemgetter(1))

    # All slices will have the same in-plane shape
    resolution = (
        int(dcm_slices_sorted[0][0].Rows),
        int(dcm_slices_sorted[0][0].Columns),
    )
    nslices = len(dcm_slices_sorted)
    metadata = {}

    shape = (*resolution, nslices)
    img = np.empty(shape, dtype="float32")
    for idx, (dcm, _) in enumerate(dcm_slices_sorted):
        img[..., idx] = dcm.pixel_array.astype("float32")
        metadata[idx] = dict(dcm)
    return ndarray(img), metadata


def load(
    file: str | Iterable[str],
    sheet: int = 1,
    skiprows=None,
    on: str = "index",
    classic_data: bool = True,
    recursive: bool = True,
    has_title: bool = True,
    has_index: bool = False,
    ordered: bool = False,
    dataframe_engine: Literal["pandas", "polars"] = "pandas",
    file_names: bool = False,
    keep_3D: bool = False,
):
    """Load files or folders for most used file types.

    Supported file extensions are :
        - csv
        - xlsx
        - xls
        - txt
        - png
        - jpg
        - pkl
        - bmp
        - xlsm
        - json
        - parquet
        - wav
        - yaml
        - tfrec
        - nii.gz
        - dcm (in this case indicate a folder name containing only dicoms)

    Args:
        file : The path to the file or a list of file paths.
            If it is a folder, all supported file types will be
            loaded in a list.
        sheet : Sheet number to extract if the file format is xlsx, xls, or xlsm.
        skiprows : Number of rows to skip from the start of the file.
        on : Column name to use as the index for the dataframe.
        classic_data : Drop duplicated rows and replace Nulls by NaNs.
        recursive : Whether to search for the file in subdirectories.
        has_title : Whether the file has a title line.
        has_index : Whether the file has an index column.
        ordered : Whether to return the data in the order it was stored.
        dataframe_engine : The engine used to manipulate tables.
        file_names : When loading a folder, return also the file names if enabled.
        keep_3D : Whether you want to keep 3D for black and white images.
    """
    if not isinstance(file, str):
        return [
            load(elem, sheet, skiprows, on, classic_data, recursive) for elem in file
        ]
    _file = file
    itsLink = url(_file)
    if itsLink == True:
        itsLink = _file
    else:
        _file = os.path.normpath(_file)
    files, file_format = locate_files(_file, recursive)
    if len(files) > 1 and (file_format != "tfrec"):
        print(files)
        raiser(
            "There are multiple files with '"
            + _file
            + "' name in the directory/subdirectories",
        )
    elif (len(files) == 0) and (not itsLink):
        print(f"Warning : The file '{_file}' wasn't found !")
        from polars import DataFrame as pl_DataFrame

        return pd.DataFrame() if dataframe_engine else pl_DataFrame()
    if (file_format != "tfrec") and (not itsLink):
        _file = files[0].split(_file)[0] + _file
    # --------------------------------------------------------------------------------------------
    if itsLink == True:
        _file = itsLink

    match file_format:
        case "tfrec":
            import tensorflow as tf

            AUTO = tf.data.experimental.AUTOTUNE
            ignore_order = tf.data.Options()
            if not ordered:
                ignore_order.experimental_deterministic = (
                    False  # disable order, increase speed
                )
            dataset = tf.data.TFRecordDataset(files, num_parallel_reads=AUTO)
            return dataset.with_options(
                ignore_order,
            )  # uses data as soon as it streams in, rather than in its original order
        case "xlsx" | "xls" | "xlsm":
            excel = pd.ExcelFile(_file)
            sheets = excel.sheet_names
            try:
                if type(sheet) is int:
                    extract = excel.parse(sheets[sheet - 1], skiprows=skiprows)
                else:
                    extract = excel.parse(sheet, skiprows=skiprows)
            except IndexError:
                print(
                    "There is no sheet number "
                    + str(sheet)
                    + ", please select a valid sheet.",
                )
                raise IndexError
            extract.dropna(how="all", inplace=True)
            if len(
                [
                    True
                    for elem in extract.columns
                    if (type(elem) is str and "Unnamed" in elem)
                ],
            ) == len(extract.columns):
                extract, extract.columns = (
                    extract.drop(extract.head(1).index),
                    extract.head(1).values.tolist()[0],
                )
            if classic_data:
                if on != "index" and on is not None:
                    extract.dropna(subset=[on], inplace=True)
                extract = caster(extract)
            extract.set_index(extract.columns[0])
            extract.drop(extract.columns[0], axis=1, inplace=True)
        case "pkl":
            if isinstance(_file, str) and not os.path.isfile(_file):
                print("The specified pickle file doesn't exist !")
            extract = pd.read_pickle(_file)
        case "csv":
            if itsLink:
                extract = pd.read_csv(_file)  # reading link csv
            else:
                if isinstance(_file, str):
                    with open(_file) as myfile:
                        firstline = myfile.readline()
                        sep = detect(firstline, default=";")
                        myfile.close()
                if dataframe_engine == "polars":
                    from polars import read_csv as pl_read_csv

                    return pl_read_csv(_file)
                extract = pd.read_csv(_file, sep=sep)
            extract = extract.dropna(how="all")  # Drop empty rows
            if not has_title:
                extract = extract.T.reset_index().T.reset_index(drop=True)
            if len(
                [
                    True
                    for elem in extract.columns
                    if (type(elem) is str and "Unnamed" in elem)
                ],
            ) == len(extract.columns):
                extract, extract.columns = (
                    extract.drop(extract.head(1).index),
                    extract.head(1).values.tolist()[0],
                )
            if classic_data:
                if on != "index":
                    extract.dropna(subset=[on], inplace=True)  # Drop rows without label
                extract = caster(extract)
            if has_index:
                extract = extract.set_index(
                    extract.columns[0],
                )  # Set first column as index
        case "parquet":
            from pyarrow.parquet import read_pandas

            extract = read_pandas(_file).to_pandas()
        case "png" | "jpg":
            from cv2 import imread

            img = ndarray(imread(_file))
            if keep_3D:
                if (img[:, :, 0] == img[:, :, 1]).all() and (
                    img[:, :, 0] == img[:, :, 2]
                ).all():
                    return img[:, :, 0]
            return img
        case "bmp":
            import imageio

            return ndarray(imageio.v3.imread(_file))
        case "json":
            import json

            if isinstance(_file, str):
                with open(_file) as user_file:
                    file_contents = user_file.read()
            return json.loads(file_contents)
        case "txt":
            if isinstance(_file, str):
                with open(_file) as f:
                    lines = f.read().splitlines()
            return lines
        case "wav":
            from librosa import load as librosa_load

            return librosa_load(_file, sr=None)
        case "yaml":
            from yaml import safe_load

            with open(_file) as stream:
                return safe_load(stream)
        case "nii.gz":
            from nibabel import load as nib_load

            nifti_data = nib_load(file)
            data_array = nifti_data.get_fdata()
            header = nifti_data.header
            metadata = dict(header)
            return data_array, metadata
        case None:  # Directory
            if itsLink:  # if it is a link and might be a json
                import json
                from requests import get

                r = get(_file)
                try:
                    return r.json()
                except json.JSONDecodeError:
                    raiser(
                        f"Not able to get the data from the link ({_file})",
                    )
            files = glob.glob(_file + "/*")
            if all(filename.endswith(".dcm") for filename in files):
                return _load_dicom(files)
            if file_names:
                return [
                    (load(elem, sheet, skiprows, on, classic_data, recursive), elem)
                    for elem in files
                ]
            return [
                load(elem, sheet, skiprows, on, classic_data, recursive)
                for elem in files
            ]

        case default:
            raiser(
                f"I don't handle this file format yet ({default}), came back in a decade.",
            )
    if classic_data:
        if on == "index":
            extract = extract[~extract.index.duplicated(keep="first")]
        elif (not (on in extract)) and (on != None):
            raiser(
                f"There is no column name '{on}' in the sheet {str(sheet)} of the file '{_file}' so I can't load this file? Try to change the 'on' parameter",
            )
        else:
            extract.drop_duplicates(subset=on, keep="last", inplace=True)
        extract.replace("Null", np.nan, inplace=True)
    return extract


def transpose_to_image_shape(arr: np.ndarray | ndarray) -> np.ndarray | ndarray:
    """Transposes a 3D array to have the shape, suitable for an image.

    Args:
        arr: A 3D numpy array with one of the following shapes: (channels, height, width),
             (height, channels, width), or (height, width, channels).

    Returns:
        A 3D numpy array with the shape (height, width, channels).

    Raises:
        ValueError: If the input array is not 3-dimensional, or if it does not have a valid shape for an image.
    """
    if len(arr.shape) != 3:
        raise ValueError("The input array must be 3-dimensional.")

    if arr.shape[0] == 3:
        return np.transpose(arr, (1, 2, 0))
    elif arr.shape[1] == 3:
        return np.transpose(arr, (0, 2, 1))
    elif arr.shape[2] == 3:
        return arr
    else:
        raiser("The input array does not have a valid shape for an image.")
        raise Exception  # Removing mypy error


def save(
    object_to_save: pd.DataFrame | np.ndarray | ndarray | dict | str,
    file: str,
    sheet="Data",
    keep_index=True,
):
    """Save different object types to different file types.

    Supported file types are:
        - pkl
        - parquet
        - json
        - xlsx
        - png
        - jpg
        - yaml
        - csv
        - txt
        - npz

    Args:
        file: The file name.
        sheet: The sheet name the data is saved if saved in an excel.
        keep_index: Keep the indexes in the saved file.

    Raises:
        Exception: If the file can't be accessed or the file type is
        not supported.
    """
    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
    except FileNotFoundError:
        pass
    match file.split(".")[-1]:
        case "xlsx":
            try:
                writer = pd.ExcelWriter(file)
            except PermissionError:
                raiser(
                    "I can't access the file '" + file + "', the "
                    "solution may be to close it and retry.",
                )
            if isinstance(object_to_save, pd.DataFrame):
                try:
                    object_to_save.to_excel(writer, sheet_name=sheet, index=keep_index)
                except OSError:
                    object_to_save.to_excel(writer, sheet_name=sheet, index=True)
            else:
                raiser(f"To save the file '{file}', the object should be a DataFrame.")
            # for column in object_to_save:
            #    column_length = max(object_to_save[column].astype(str).map(len).max(), len(column))
            #    col_idx = object_to_save.columns.get_loc(column)
            #    writer.sheets[sheet].set_column(col_idx, col_idx, column_length)
            writer._save()
        case "csv":
            if isinstance(object_to_save, pd.DataFrame):
                object_to_save.to_csv("./" + file, index=keep_index)
            else:
                raiser(f"To save the file '{file}', the object should be a DataFrame.")
        case "pkl":
            pd.to_pickle(object_to_save, "./" + file)
        case "parquet":
            caster(object_to_save)
            from pyarrow import Table as paTable
            from pyarrow.parquet import write_table

            table = paTable.from_pandas(object_to_save, preserve_index=False)
            write_table(table, file + ".parquet")
        case "png" | "jpg":
            from PIL import Image

            if not isinstance(object_to_save, np.ndarray | ndarray):
                raiser(f"To save the file '{file}', the object should be an array.")
            else:
                if object_to_save.dtype != np.uint8:
                    object_to_save = np.round(object_to_save).astype(np.uint8)
            object_to_save = transpose_to_image_shape(object_to_save)
            im = Image.fromarray(object_to_save)
            if len(object_to_save.shape) == 2:
                # Convert the image to RGB mode
                im = im.convert("RGB")
            im.save(file)
        case "json" | "txt":
            if isinstance(object_to_save, str):
                with open(file, "w") as f:
                    f.write(object_to_save)
            else:
                raiser(f"To save the file '{file}', the object should be a string.")
        case "yaml":
            import yaml

            with open(file, "w") as f:
                yaml.dump(object_to_save, f)
        case "npz":
            if isinstance(object_to_save, dict):
                np.savez(
                    file,
                    **object_to_save,
                )
            else:
                raiser(f"To save the file '{file}', the object should be a dict.")
        case default:
            raiser(
                f"I don't handle this file format yet ({default}), come back in a decade.",
            )


def merge(
    df: pd.DataFrame,
    file: str | pd.DataFrame,
    sheet=1,
    on: str = "index",
    skiprows=None,
    how: str = "outer",
    save_file: bool = False,
):
    """Merge two pandas DataFrames either on index or a specific column.

    Args:
        df : The first DataFrame to be merged.
        file : The second DataFrame or file to be merged.
        sheet : The sheet number if `file` is a file name. Defaults to 1.
        on : The column to merge on. Defaults to "index".
        skiprows : The number of rows to skip from the file.
        how : The type of merge to be performed. Defaults to "outer".
        save_file : Whether to save the merged DataFrame to file. Defaults to False.

    Returns:
        pd.DataFrame: The merged DataFrame.

    Raises:
        ValueError: If `df` is not a DataFrame or if the specified `on` column doesn't exist in `file`.
    """
    from re import match

    if not (type(df) is pd.DataFrame):
        raiser("The df parameter must be a DataFrame.")
    if type(file) is pd.DataFrame:
        dataBase = file
    else:
        dataBase = load(
            file,
            sheet=sheet,
            skiprows=skiprows,
            on=on,
        )
    if not dataBase.empty:
        columns = list(dataBase.columns)
        if on != "index":
            try:
                columns.remove(on)
            except ValueError:
                raiser(
                    "You can't merge your data as there are no column '"
                    + on
                    + "' in your already loaded DataFrame.",
                )
        if df.empty:
            merge = dataBase.copy()
        elif on != "index":
            merge = dataBase.merge(df, how=how, on=on)
        else:
            merge = dataBase.merge(df, how=how, left_index=True, right_index=True)
        merge = merge.loc[:, ~merge.columns.duplicated()]
        col = list(merge.columns)
        if on != "index":
            col.remove(on)
        merge.dropna(how="all", subset=col, inplace=True)
        del dataBase
        drop_y = list(filter(lambda v: match(".*_y$", v), merge.columns))
        keep_x = list(filter(lambda v: match(".*_x$", v), merge.columns))
        keep = [name[:-2] for name in keep_x]
        for col_x, col_y in zip(keep_x, drop_y):
            merge[col_x] = merge[col_x].mask(pd.isnull, merge[col_y], errors="ignore")
        merge.drop(drop_y, axis=1, inplace=True)
        merge.rename(columns=dict(zip(keep_x, keep)), inplace=True)
        merge = merge.sort_index()
        merge.replace("Null", np.nan, inplace=True)
    else:
        merge = df
    if save_file:
        save(merge, file)
    else:
        return merge


def color(
    text: str,
    fg: Literal[
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        "LIGHTBLACK",
        "LIGHTRED",
        "LIGHTGREEN",
        "LIGHTYELLOW",
        "LIGHTBLUE",
        "LIGHTMAGENTA",
        "LIGHTCYAN",
        "LIGHTWHITE",
    ] = "RED",
    bg: Literal[
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        "LIGHTBLACK",
        "LIGHTRED",
        "LIGHTGREEN",
        "LIGHTYELLOW",
        "LIGHTBLUE",
        "LIGHTMAGENTA",
        "LIGHTCYAN",
        "LIGHTWHITE",
    ]
    | None = None,
) -> str:
    r"""Format the text to print it in color.

    Args:
        text: The input text to format.
        fg: The foreground color.
        bg: The background color.

    Examples:
        >>> "This is a " + color("blue text", "BLUE") + " !"
        'This is a \\x1b[34mblue text\\x1b[0m !'

        >>> print("This is a " + color("blue text", "BLUE") + " !")
        This is a \x1b[34mblue text\x1b[0m !

        >>> "This is a " + color("strange color", "GREEN", "WHITE") + " !"
        'This is a \\x1b[47m\\x1b[32mstrange color\\x1b[0m !'
    """
    from colorama import Back
    from colorama import Fore
    from colorama import Style

    if bg:
        complete_bg: str = bg
        if "LIGHT" in bg:
            complete_bg += "_EX"
    complete_fg: str = fg
    if "LIGHT" in fg:
        complete_fg += "_EX"
    colored_text = f"{Fore.__getattribute__(complete_fg)}{text}{Style.RESET_ALL}"
    return (
        colored_text
        if bg is None
        else Back.__getattribute__(complete_bg) + colored_text
    )


def _same(sequence) -> bool:
    """Determine if all elements in a sequence are the same.

    This function takes a sequence (e.g., list or tuple) and checks if all its elements are equal.
    If the sequence is empty, it returns True.

    Args:
        sequence: A sequence of elements to be checked for equality.

    Returns:
        True if all elements in the sequence are equal, or if the sequence is empty. False otherwise.

    Example:
        >>> _same([1, 1, 1])
        True
        >>> _same([1, 2, 1])
        False
        >>> _same([])
        True
    """
    elements = iter(sequence)
    try:
        first = next(elements)
    except StopIteration:
        return True
    for el in elements:
        if el != first:
            return False
    return True


def detect(
    text: str,
    default: str | None = None,
    whitelist: list[str] | None = None,
    blacklist: Iterable[str] = SILLY_DELIMITERS,
) -> str | None:
    r"""Detects the delimiter used in text formats.

    >>> detect(r"looks|like|the vertical bar\nis|the|delimiter\n")
    '|'

    `detect_delimiter.detect()` looks at the text provided to try to
    find an uncommon delimiter, such as ` for whatever reason.

    >>> detect('looks\x10like\x10something stupid\nis\x10the\x10delimiter')
    '\x10'

    When `detect()` doesn't know, it returns `None`:

    >>> text = "not really any delimiters in here.\nthis is just text.\n"
    >>> detect(text)

    It's possible to provide a default, which will be used in that case:

    >>> detect(text, default=',')
    ','

    By default, it will prevent avoid checking alpha-numeric characters
    and the period/full stop character ("."). This can be adjusted via
    the `blacklist` parameter.

    If you believe that you know the delimiter, it's possible to provide
    a list of possible delimiters to check for via the `whitelist` parameter.
    If you don't provide a value, `[',', ';', ':', '|', '\t']` will be checked.
    """
    from collections import Counter
    from copy import copy

    if whitelist:
        candidates = whitelist
    else:
        candidates = list(",;:|\t")

    sniffed_candidates: Counter[str] = Counter()
    likely_candidates = []

    lines: list[str] = []
    # todo: support streaming
    text_ = copy(text)
    while len(lines) < 5:
        for line in text_.splitlines():
            lines.append(line)

    for c in candidates:
        fields_for_candidate = []

        for line in lines:
            for char in line:
                if char not in blacklist:
                    sniffed_candidates[char] += 1
            fields = line.split(c)
            n_fields = len(fields)

            # if the delimiter isn't present in the
            # first line, it won't be present in the others
            if n_fields == 1:
                break
            fields_for_candidate.append(n_fields)

        if not fields_for_candidate:
            continue

        if _same(fields_for_candidate):
            likely_candidates.append(c)

    # no delimiter found
    if not likely_candidates:
        if whitelist is None and sniffed_candidates:
            new_whitelist = [
                char for (char, _count) in sniffed_candidates.most_common()
            ]
            return detect(text, whitelist=new_whitelist) or default
        return default

    if default in likely_candidates:
        return default

    return likely_candidates[0]


def delete(name: str | list[str]) -> None:
    """Delete file(s) and/or folder(s) by its name."""
    from os import remove
    from shutil import rmtree

    if isinstance(name, str):
        try:
            rmtree(name)
        except NotADirectoryError:
            remove(name)
    elif isinstance(name, list):
        for file_name in name:
            try:
                rmtree(file_name)
            except NotADirectoryError:
                remove(file_name)


def url(value, public=False):
    """Return whether or not given value is a valid URL.

    If the value is valid URL this function returns ``True``, otherwise
    :class:`~validators.utils.ValidationFailure`.

    This validator is based on the wonderful `URL validator of dperini`_.

    .. _URL validator of dperini:
        https://gist.github.com/dperini/729294

    Examples::

        >>> url('http://foobar.dk')
        True

        >>> url('http://10.0.0.1')
        True

        >>> url('http://foobar.d')
        ValidationFailure(func=url, ...)

        >>> url('http://10.0.0.1', public=True)
        ValidationFailure(func=url, ...)

    .. versionadded:: 0.2

    .. versionchanged:: 0.10.2

        Added support for various exotic URLs and fixed various false
        positives.

    .. versionchanged:: 0.10.3

        Added ``public`` parameter.

    .. versionchanged:: 0.10.4

        Made the regular expression this function uses case insensitive.

    :param value: URL address string to validate
    :param public: (default=False) Set True to only allow a public IP address
    """
    from re import compile, UNICODE, IGNORECASE

    ip_middle_octet = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
    ip_last_octet = r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"

    regex = compile(
        "^"
        # protocol identifier
        "(?:(?:https?|ftp)://)"
        # user:pass authentication
        r"(?:\S+(?::\S*)?@)?" "(?:" "(?P<private_ip>"
        # IP address exclusion
        # private & local networks
        "(?:(?:10|127)" + ip_middle_octet + "{2}" + ip_last_octet + ")|"
        r"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + ")|"
        r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + "))"
        "|"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        "(?P<public_ip>"
        r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        "" + ip_middle_octet + "{2}"
        "" + ip_last_octet + ")"
        "|"
        # host name
        "(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        "(?:\\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        "(?:\\.(?:[a-z\u00a1-\uffff]{2,}))" ")"
        # port number
        r"(?::\d{2,5})?"
        # resource path
        r"(?:/\S*)?"
        # query string
        r"(?:\?\S*)?" "$",
        UNICODE | IGNORECASE,
    )

    pattern = compile(regex)

    result = pattern.match(value)
    if not public:
        return result

    return result and not result.groupdict()["private_ip"]
