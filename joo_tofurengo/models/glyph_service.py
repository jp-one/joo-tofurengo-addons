from odoo import models
from tofurengo.builder import build_normalizer, build_renderer, build_simplifier
from tofurengo.glyph_normalizer import GlyphNormalizer, NormalizeResult


class GlyphService(models.AbstractModel):
    """
    Service layer integrating the tofurengo library with Odoo.
    Provides normalization, rendering, and simplification capabilities for variant glyph tags.
    Documentation: https://jp-rad.github.io/tofurengo/
    """
    _name = "joo_tofurengo.glyph_service"
    _description = "Tofurengo Glyph Tag Normalization, Rendering, and Simplification Service"

    def _get_normalizer(self) -> GlyphNormalizer:
        """
        Retrieves the GlyphNormalizer instance configured for the active Glyph System Identifier.
        Reads the system parameter 'joo_tofurengo.set' (defaults to 'mj_plusx').

        Supported Glyph System Identifiers:
          - 'mj': MJ (version 6.02.201)
          - 'mj_onka': MJ with Onka (version 6.02.201_onka)
          - 'mj_plus': MJ+ Character Set (version 4.10)
          - 'mj_plusx': Extended MJ+ Character Set (version 1.20)
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
        Normalizes variant glyph tags within the given text using tofurengo's GlyphNormalizer.
        The behavior is governed by the active Glyph System Identifier set in system parameters.
        """
        normalizer = self._get_normalizer()
        return normalizer.normalize(text)

    def render(self, text: str, use_base: bool = False) -> str:
        """
        Generates rendered string output for tagged text using tofurengo's GlyphRenderer.

        :param text: The tagged text to render.
        :param use_base: If True, uses base characters for rendering.
        :return: Rendered text string.
        """
        renderer = build_renderer()
        return renderer.render(text, use_base=use_base)

    def simplify(self, text: str) -> str:
        """
        Simplifies text by removing variant glyph tags and converting them to base characters
        using tofurengo's GlyphSimplifier.

        :param text: The tagged text containing variant glyph tags.
        :return: Simplified text with glyph tags stripped or reduced to base characters.
        """
        simplifier = build_simplifier()
        return simplifier.simplify(text)
