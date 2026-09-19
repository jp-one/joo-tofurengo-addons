import re
import jaconv
from odoo import models, fields, api
from .res_config_settings import get_furigana_type_setting


class ResPartner(models.Model):
    """
    Extension of `res.partner` to support Japanese phonetic reading (furigana).

    Features:
    - Normalization type controlled via System Parameter (`get_furigana_type_setting()`)
    - Integration with Odoo's name search (`_rec_names_search`)
    - Automatic normalization on create/write/onchange
    - Ordering prioritizes furigana and newest records first
    """

    _inherit = 'res.partner'
    _order = "furigana, complete_name, id desc"

    furigana = fields.Char(
        string="Furigana",
        index=True,
        help="Phonetic reading of the partner name."
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
    # System Settings Helper
    # ----------------------------------------------------------------------
    def _get_furigana_type_setting(self) -> str:
        """
        Fetch the furigana normalization type from system parameters.
        Possible values: 'hiragana', 'katakana', 'none'.
        """
        return get_furigana_type_setting(self)
    
    # ----------------------------------------------------------------------
    # Normalization helpers
    # ----------------------------------------------------------------------
    def _sanitize_spaces(self, text: str) -> str:
            """Helper to normalize spaces by converting full-width spaces and collapsing multiple whitespaces."""
            if not text:
                return ""
            text = text.replace("\u3000", "\u0020")
            text = text.strip()
            text = re.sub(r"\s+", "\u0020", text)
            return text

    def _normalize_furigana(self, text: str, mode: str) -> str:
        """Normalize furigana input based on system settings or specified mode.

        Parameters
        ----------
        text : str
            Raw text input.
        mode : str
            'hiragana', 'katakana', or 'none'.

        Returns
        -------
        str
            Normalized string.
        """
        if not text:
            return ""
        text = self._sanitize_spaces(text)
        if mode == 'hiragana':
            text = text.upper()
            text = jaconv.h2z(text, ignore="\u0020", kana=True, ascii=True, digit=True)
            text = jaconv.kata2hira(text)
        elif mode == 'katakana':
            text = text.upper()
            text = jaconv.h2z(text, ignore="\u0020", kana=True, ascii=True, digit=True)
            text = jaconv.hira2kata(text)
        return text

    # ----------------------------------------------------------------------
    # Onchange normalization
    # ----------------------------------------------------------------------
    @api.onchange('furigana')
    def _onchange_furigana(self):
        """
        Normalize furigana when the user edits the field in the UI.
        """
        if self.furigana:
            mode = self._get_furigana_type_setting()
            self.furigana = self._normalize_furigana(self.furigana, mode=mode)

    # ----------------------------------------------------------------------
    # Create override
    # ----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Normalize furigana before creating new records.
        """
        mode = self._get_furigana_type_setting()
        for vals in vals_list:
            if vals.get('furigana'):
                vals['furigana'] = self._normalize_furigana(vals['furigana'], mode=mode)
        return super().create(vals_list)

    # ----------------------------------------------------------------------
    # Write override
    # ----------------------------------------------------------------------
    def write(self, vals):
        """
        Normalize furigana before updating existing records.
        """
        if vals.get('furigana'):
            mode = self._get_furigana_type_setting()
            vals['furigana'] = self._normalize_furigana(vals['furigana'], mode=mode)
        return super().write(vals)
