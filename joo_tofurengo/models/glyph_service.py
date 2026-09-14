from odoo import models
from tofurengo.builder import build_normalizer, build_renderer, build_simplifier
from tofurengo.glyph_normalizer import GlyphNormalizer, NormalizeResult


class GlyphService(models.AbstractModel):
    _name = "joo_tofurengo.glyph_service"
    _description = "Glyph Tag Normalization and Rendering Service"

    def _get_normalizer(self) -> GlyphNormalizer:
        conf = self.env['ir.config_parameter'].sudo()
        param_set = conf.get_param('joo_tofurengo.set', 'mj_plusx')

        if param_set == 'mj':
            return build_normalizer("mj", "0.00")
        elif param_set == 'mj_plus':
            return build_normalizer("mj_plus", "4.10")
        else:
            return build_normalizer("mj_plusx", "1.20")

    def normalize(self, text: str) -> NormalizeResult:
        normalizer = self._get_normalizer()
        return normalizer.normalize(text)

    def render(self, text: str, use_base: bool = False) -> str:
        renderer = build_renderer()
        return renderer.render(text, use_base=use_base)

    def simplify(self, text: str) -> str:
        simplifier = build_simplifier()
        return simplifier.simplify(text)
