import jaconv
from odoo import models, fields, api


class JooTofurengoPartnerKanaMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.kana.mixin'
    _description = 'Partner Kana Mixin'

    family_kana = fields.Char("Family Kana",tracking=True, index=True)
    given_kana = fields.Char("Given Kana", tracking=True, index=True)

    def _normalize_kana_text(self, text):
        """Convert full-width spaces to half-width, strip leading/trailing spaces, and convert Katakana to Hiragana."""
        if not text:
            return ""
        # Replace full-width space (\u3000) with half-width space and strip leading/trailing spaces
        text = text.replace("\u3000", " ").strip()
        # Convert half-width Kana to full-width Kana
        zenkaku = jaconv.h2z(text, kana=True)
        # Convert Katakana to Hiragana
        return jaconv.kata2hira(zenkaku)

    def _split_kana(self, text):
        """Split text by space into family_kana and given_kana, stripping whitespace."""
        if not text:
            return "", ""
        parts = text.strip().split(" ", 1)
        return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (parts[0].strip(), "")

    @api.onchange('family_kana', 'given_kana')
    def _onchange_kana(self):
        if self.family_kana:
            self.family_kana = self._normalize_kana_text(self.family_kana)
        if self.given_kana:
            self.given_kana = self._normalize_kana_text(self.given_kana)

        # Clear given_kana if the partner is a company
        if getattr(self, 'is_company', False):
            self.given_kana = False

    @api.onchange('is_company')
    def _onchange_is_company_kana(self):
        """Handle switching between Individual and Company."""
        if self.is_company:
            # Switching to Company: combine family_kana and given_kana into family_kana, clear given_kana
            fam = (self.family_kana or "").strip()
            giv = (self.given_kana or "").strip()
            if fam and giv:
                self.family_kana = f"{fam} {giv}".strip()
            elif giv:
                self.family_kana = giv
            self.given_kana = False
        else:
            # Switching to Individual: split family_kana into family_kana and given_kana if space exists
            if self.family_kana and not self.given_kana:
                fam, giv = self._split_kana(self.family_kana)
                self.family_kana = fam
                self.given_kana = giv

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('family_kana'):
                vals['family_kana'] = self._normalize_kana_text(vals['family_kana'])
            if vals.get('given_kana'):
                vals['given_kana'] = self._normalize_kana_text(vals['given_kana'])

            # Ensure company only has family_kana
            if vals.get('is_company'):
                fam = (vals.get('family_kana') or "").strip()
                giv = (vals.get('given_kana') or "").strip()
                if fam and giv:
                    vals['family_kana'] = f"{fam} {giv}".strip()
                elif giv:
                    vals['family_kana'] = giv
                vals['given_kana'] = False
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('family_kana'):
            vals['family_kana'] = self._normalize_kana_text(vals['family_kana'])
        if vals.get('given_kana'):
            vals['given_kana'] = self._normalize_kana_text(vals['given_kana'])

        res = super().write(vals)

        # Adjust fields after write if company status changed or updated
        for rec in self:
            if rec.is_company and rec.given_kana:
                fam = (rec.family_kana or "").strip()
                giv = rec.given_kana.strip()
                combined = f"{fam} {giv}".strip()
                super(JooTofurengoPartnerKanaMixin, rec).write({
                    'family_kana': combined,
                    'given_kana': False,
                })
        return res
