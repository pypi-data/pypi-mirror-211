"""
PETPVC
======

Examples
--------

Iterative Yang with a 6-millimeter PSF:

>>> task = PETPVC(
...     input_image="input.nii",
...     input_mask="mask.nii",
...     pvc_method="IY",
...     fwhm_x=6.0,
...     fwhm_y=6.0,
...     fwhm_z=6.0,
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'petpvc --input input.nii --mask mask.nii --output ...input_pvc.nii --pvc IY ... -x 6.0 -y 6.0 -z 6.0'
"""

__all__ = ["PETPVC"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .specs import FWHMSpec


@define(kw_only=True)
class PETPVCSpec(ShellSpec):
    """Specifications for petpvc."""

    input_image: PathLike = field(metadata={"help_string": "input image", "mandatory": True, "argstr": "--input"})

    input_mask: PathLike = field(metadata={"help_string": "input mask", "mandatory": True, "argstr": "--mask"})

    output_image: str = field(
        metadata={"help_string": "output image", "argstr": "--output", "output_file_template": "{input_image}_pvc"}
    )

    pvc_method: str = field(
        metadata={
            "help_string": "desired PVC method",
            "mandatory": True,
            "argstr": "--pvc",
            "allowed_values": {
                "GTM",
                "LABBE",
                "RL",
                "VC",
                "RBV",
                "LABBE+RBV",
                "RBV+VC",
                "RBV+RL",
                "LABBE+RBV+VC",
                "LABBE+RBV+RL",
                "STC",
                "MTC",
                "LABBE+MTC",
                "MTC+VC",
                "MTC+RL",
                "LABBE+MTC+VC",
                "LABBE+MTC+RL",
                "IY",
                "IY+VC",
                "IY+RL",
                "MG",
                "MG+VC",
                "MG+RL",
            },
        }
    )

    debug: bool = field(metadata={"help_string": "print debug information", "argstr": "-d"})

    num_iterations_for_iterative_yang: int = field(
        default=10,
        metadata={
            "help_string": "number of iterations for the iterative Yang method",
            "formatter": lambda num_iterations_for_iterative_yang, pvc_method: (
                f"-n {str(num_iterations_for_iterative_yang)}" if "IY" in pvc_method else ""
            ),
        },
    )

    num_iterations_for_deconvolution: int = field(
        default=10,
        metadata={
            "help_string": "number of iterations for deconvolution (RL and VC methods)",
            "formatter": lambda num_iterations_for_deconvolution, pvc_method: (
                f"-k {str(num_iterations_for_deconvolution)}" if any(s in pvc_method for s in ["RL", "VC"]) else ""
            ),
        },
    )

    alpha_value: float = field(default=1.5, metadata={"help_string": "alpha value", "argstr": "--alpha"})

    stop_value: float = field(default=0.01, metadata={"help_string": "stopping criterion", "argstr": "--stop"})

    disable_non_negativity: bool = field(
        metadata={"help_string": "turn non-negativity constraint off", "argstr": "--disable-non-neg"}
    )


class PETPVC(ShellCommandTask):
    """Task definition for petpvc."""

    executable = "petpvc"

    input_spec = SpecInfo(name="Inputs", bases=(PETPVCSpec, FWHMSpec))
