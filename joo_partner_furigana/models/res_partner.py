import jaconv
from odoo import models, fields, api


class ResPartner(models.Model):
    """
    Extension of `res.partner` to support Japanese phonetic reading (furigana).

    Features:
    - Input normalization (space normalization, kana normalization)
    - Integration with Odoo's name search (`_rec_names_search`)
    - Display name enhancement (append furigana)
    - Automatic normalization on create/write/onchange
    - Ordering prioritizes furigana and newest records first
    """

    _inherit = 'res.partner'
    _order = "furigana, complete_name, id desc"

    furigana = fields.Char(
        string="Furigana",
        tracking=True,
        index=True,
        help="Phonetic reading of the partner name in Hiragana."
    )

    # ----------------------------------------------------------------------
    # Register hook
    # ----------------------------------------------------------------------
    def _register_hook(self):
        """
        Add `furigana` to `_rec_names_search` so that Odoo's name search
        includes phonetic reading.
        """
        super()._register_hook()

        if not isinstance(self._rec_names_search, list):
            self._rec_names_search = list(self._rec_names_search or [])

        if 'furigana' not in self._rec_names_search:
            self._rec_names_search.append('furigana')

    # ----------------------------------------------------------------------
    # Normalization helper
    # ----------------------------------------------------------------------
    def _normalize_furigana(self, text):
        """
        Normalize furigana input.

        Steps:
        - Replace full-width spaces with half-width spaces
        - Strip whitespace
        - Convert half-width kana to full-width kana
        - Convert Katakana to Hiragana

        Parameters
        ----------
        text : str
            Raw user input.

        Returns
        -------
        str
            Normalized Hiragana string.
        """
        if not text:
            return ""
        text = text.replace("\u3000", " ").strip()
        zenkaku = jaconv.h2z(text, kana=True)
        return jaconv.kata2hira(zenkaku)

    # ----------------------------------------------------------------------
    # Display name override
    # ----------------------------------------------------------------------
    @api.depends('furigana')
    def _compute_display_name(self):
        """
        Append furigana to the computed display name.

        Example:
            "John Smith" → "John Smith (hiragana)"
        """
        super()._compute_display_name()
        for partner in self:
            if partner.furigana:
                partner.display_name = f"{partner.display_name} ({partner.furigana})"

    # ----------------------------------------------------------------------
    # Onchange normalization
    # ----------------------------------------------------------------------
    @api.onchange('furigana')
    def _onchange_furigana(self):
        """
        Normalize furigana when the user edits the field in the UI.
        """
        if self.furigana:
            self.furigana = self._normalize_furigana(self.furigana)

    # ----------------------------------------------------------------------
    # Create override
    # ----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Normalize furigana before creating new records.

        Parameters
        ----------
        vals_list : list[dict]
            List of value dictionaries for new records.

        Returns
        -------
        ResPartner
            Created partner records.
        """
        for vals in vals_list:
            if vals.get('furigana'):
                vals['furigana'] = self._normalize_furigana(vals['furigana'])
        return super().create(vals_list)

    # ----------------------------------------------------------------------
    # Write override
    # ----------------------------------------------------------------------
    def write(self, vals):
        """
        Normalize furigana before updating existing records.

        Parameters
        ----------
        vals : dict
            Values to update.

        Returns
        -------
        bool
            True if the update succeeds.
        """
        if vals.get('furigana'):
            vals['furigana'] = self._normalize_furigana(vals['furigana'])
        return super().write(vals)
