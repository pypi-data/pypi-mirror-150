# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path as path_t
from typing import Union

import cell_tracking_BC.in_out.graphics.generic.d_any as gphc
import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.measure as msre
import tifffile as tiff
from cell_tracking_BC.in_out.graphics.dbe.matplotlib.style import CellAnnotationStyle
from cell_tracking_BC.type.sequence import BoundingBoxSlices, sequence_t


def SaveSequenceAnnotations(
    sequence: sequence_t, folder: path_t, file: Union[str, path_t], /
) -> None:
    """"""
    figure, axes = pypl.subplots()
    canvas = figure.canvas

    annotated = None
    cell_contours = gphc.CellContours(sequence, True)
    for t_idx in range(sequence.length):
        axes.clear()
        axes.set_axis_off()
        for cell in sequence.cell_frames[t_idx].cells:
            position = nmpy.flipud(cell.centroid)
            # TODO: check how to improve the speed of TrackLabelsContainingCell
            labels = sequence.tracks.TrackLabelsContainingCell(cell, tolerant_mode=True)
            if labels is None:
                text = "i"  # Invalid
            elif labels.__len__() == 0:
                text = "p"  # Pruned
            else:
                if labels.__len__() > 1:
                    labels = "\n".join(str(_lbl) for _lbl in labels)
                else:
                    labels = str(labels[0])
                text = labels
            additionals = CellAnnotationStyle(False, "\n" in text)
            axes.annotate(
                text,
                position,
                ha="center",
                **additionals,
            )
            contour = msre.find_contours(
                cell.Map(sequence.shape, margin=-50), level=0.5
            )[0]
            axes.plot(
                contour[:, 1],
                contour[:, 0],
                linestyle=":",
                color=(0.0, 0.6, 0.6, 0.3),
            )
        for contour in cell_contours[t_idx]:
            axes.plot(
                contour[:, 1],
                contour[:, 0],
                linestyle=":",
                color=(0.0, 1.0, 1.0, 0.3),
            )
        canvas.draw()
        content = nmpy.array(canvas.renderer.buffer_rgba())[:,:,:3]
        if annotated is None:
            annotated = nmpy.empty((*content.shape, sequence.length), dtype=nmpy.uint8)
        annotated[..., t_idx] = content

    row_slice, col_slice = BoundingBoxSlices(annotated)
    annotated = annotated[row_slice, col_slice, :, :]
    annotated = nmpy.moveaxis(annotated, (0, 1, 2, 3), (2, 3, 1, 0))
    annotated = annotated[:, nmpy.newaxis, :, :, :]

    tiff.imwrite(
        str(folder / file),
        annotated,
        photometric="rgb",
        compression="deflate",
        planarconfig="separate",
        metadata={"axes": "XYZCT"},
    )

    pypl.close(fig=figure)  # To prevent remaining caught in event loop
