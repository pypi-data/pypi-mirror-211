"""
Utilities
=========

Produce a 4-D mask file from 3-D labels:

>>> task = PVCMake4D(input_image="mask.nii")
>>> task.cmdline    # doctest: +ELLIPSIS
'pvc_make4d -i mask.nii -o ...mask_pvcmake4d.nii'

Relabel an image:

>>> task = PVCRelabel(
...     input_image="input.nii",
...     parcellation_file="parc.csv",
...     parcellation_type="DST",
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'pvc_relabel -i input.nii -o ...input_pvcrelabel.nii --parc parc.csv --type DST'

Simulate partial volume effect with blurring:

>>> task = PVCSimulate(input_image="input.nii", fwhm_x=4.0, fwhm_y=4.0, fwhm_z=4.0)
>>> task.cmdline    # doctest: +ELLIPSIS
'pvc_simulate input.nii ...input_pvcsimulate.nii -x 4.0 -y 4.0 -z 4.0'
"""

__all__ = ["PVCMake4D", "PVCRelabel", "PVCSimulate"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .specs import FWHMSpec


@define(kw_only=True)
class PVCMake4DSpec(ShellSpec):
    """Specifications for pvc_make4d."""

    input_image: PathLike = field(metadata={"help_string": "input 3-D mask image", "mandatory": True, "argstr": "-i"})

    output_image: str = field(
        metadata={
            "help_string": "output 4-D region mask image",
            "argstr": "-o",
            "output_file_template": "{input_image}_pvcmake4d",
        }
    )


class PVCMake4D(ShellCommandTask):
    """Task definition for pvc_make4d."""

    executable = "pvc_make4d"

    input_spec = SpecInfo(name="Inputs", bases=(PVCMake4DSpec,))


@define(kw_only=True)
class PVCRelabelSpec(ShellSpec):
    """Specifications for pvc_relabel."""

    input_image: PathLike = field(metadata={"help_string": "input image", "mandatory": True, "argstr": "-i"})

    output_image: str = field(
        metadata={"help_string": "output image", "argstr": "-o", "output_file_template": "{input_image}_pvcrelabel"}
    )

    parcellation_file: PathLike = field(
        metadata={"help_string": "parcellation file", "mandatory": True, "argstr": "--parc"}
    )

    parcellation_type: str = field(metadata={"help_string": "parcellation type", "mandatory": True, "argstr": "--type"})


class PVCRelabel(ShellCommandTask):
    """Task definition for pvc_relabel."""

    executable = "pvc_relabel"

    input_spec = SpecInfo(name="Inputs", bases=(PVCRelabelSpec,))


@define(kw_only=True)
class PVCSimulateSpec(ShellSpec):
    """Specifications for pvc_simulate."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": "", "position": 0}
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "position": 1,
            "output_file_template": "{input_image}_pvcsimulate",
        }
    )


class PVCSimulate(ShellCommandTask):
    """Task definition for pvc_simulate."""

    executable = "pvc_simulate"

    input_spec = SpecInfo(name="Inputs", bases=(PVCSimulateSpec, FWHMSpec))
