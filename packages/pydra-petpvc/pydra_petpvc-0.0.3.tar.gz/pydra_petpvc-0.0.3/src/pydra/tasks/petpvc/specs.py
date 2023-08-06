from attrs import define, field
from pydra.engine.specs import ShellSpec


@define(slots=False, kw_only=True)
class FWHMSpec(ShellSpec):
    """Specifications for the FWHM of the PSF."""

    fwhm_x: float = field(metadata={"help_string": "FWHM of the PSF in the x-axis", "mandatory": True, "argstr": "-x"})

    fwhm_y: float = field(metadata={"help_string": "FWHM of the PSF in the y-axis", "mandatory": True, "argstr": "-y"})

    fwhm_z: float = field(metadata={"help_string": "FWHM of the PSF in the z-axis", "mandatory": True, "argstr": "-z"})
