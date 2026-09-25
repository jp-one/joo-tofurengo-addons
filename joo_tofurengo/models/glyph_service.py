from odoo import models
from tofurengo.builder import build_normalizer, build_renderer, build_simplifier
from tofurengo.glyph_normalizer import GlyphNormalizer, NormalizeResult
from tofurengo.glyph_inverse_renderer import GlyphInverseRenderer


class GlyphService(models.AbstractModel):
    """
    Service layer integrating the `tofurengo` library with Odoo.

    Provides normalization, rendering, simplification, and inverse rendering
    capabilities for variant GlyphTags.

    Documentation:
        https://jp-rad.github.io/tofurengo/
    """
    _name = "joo_tofurengo.glyph_service"
    _description = "Tofurengo GlyphTag Normalization, Rendering, and Simplification Service"

    def _get_normalizer(self) -> GlyphNormalizer:
        """
        Retrieves the `GlyphNormalizer` instance configured for the active Glyph System Identifier.

        Reads the Odoo system parameter `joo_tofurengo.set` (defaults to `'mj_plusx'`).

        Supported Glyph System Identifiers:
            - `'mj'`: MJ (version 6.02.201)
            - `'mj_onka'`: MJ with Onka (version 6.02.201_onka)
            - `'mj_plus'`: MJ+ Character Set (version 4.10)
            - `'mj_plusx'`: Extended MJ+ Character Set (version 1.20)

        Returns:
            GlyphNormalizer: Configured normalizer instance.
        """
        conf = self.env['ir.config_parameter'].sudo()
        system_id = conf.get_param('joo_tofurengo.set', 'mj_plusx')

        if system_id == 'mj':
            return build_normalizer("mj", "6.02.201")
        elif system_id == 'mj_onka':
            return build_normalizer("mj", "6.02.201_onka")
        elif system_id == 'mj_plus':
            return build_normalizer("mj_plus", "4.10")
        else:
            # Default fallback: 'mj_plusx'
            return build_normalizer("mj_plusx", "1.20")

    def normalize(self, text: str) -> NormalizeResult:
        """
        Normalizes variant GlyphTags within the given text.

        Uses `tofurengo`'s `GlyphNormalizer`. The behavior is governed by
        the active Glyph System Identifier set in system parameters.

        Args:
            text (str): Input string containing variant GlyphTags.

        Returns:
            NormalizeResult: The result object containing the normalized text
            and status information.
        """
        normalizer = self._get_normalizer()
        return normalizer.normalize(text)

    def render(self, text: str, use_base: bool = False) -> str:
        """
        Generates rendered string output for tagged text using `GlyphRenderer`.

        Args:
            text (str): The tagged text to render.
            use_base (bool, optional): If True, uses base characters for rendering.
                Defaults to False.

        Returns:
            str: Rendered text string.
        """
        renderer = build_renderer()
        return renderer.render(text, use_base=use_base)

    def simplify(self, text: str) -> str:
        """
        Simplifies text by converting variant GlyphTags to base characters.

        Uses `tofurengo`'s `GlyphSimplifier`.

        Args:
            text (str): The tagged text containing variant GlyphTags.

        Returns:
            str: Simplified text with GlyphTags stripped or reduced to base characters.
        """
        simplifier = build_simplifier()
        return simplifier.simplify(text)

    def inverse(self, text: str) -> str:
        """
        Converts Unicode text into normalized GlyphTags using `GlyphInverseRenderer`.

        Performs grapheme cluster segmentation (treating IVS as single units) and
        escapes literal left braces (`{` -> `{{`).

        Args:
            text (str): Input Unicode text.

        Returns:
            str: Inverse rendered text containing normalized GlyphTags and escaped braces.
        """
        inverse = GlyphInverseRenderer()
        return inverse.inverse_text(text)
