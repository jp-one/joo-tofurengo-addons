/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

/**
 * Mapping between configuration keys and actual font-family names defined in @font-face.
 */
const FONT_MAP = {
    dwpiexmincho: "DWPIexMincho",
    dwpimincho: "DWPIMincho",
    ipamjm: "IPAmjMincho",
};

const DYNAMIC_STYLE_ID = "joo-web-fonts-dynamic-style";

/**
 * Fetch selected font from server and apply CSS via dedicated style element.
 */
async function loadAndApplyFont() {
    try {
        const fontKey = await rpc("/joo_web_fonts/font");
        const fontFamily = FONT_MAP[fontKey] || null;

        if (!fontFamily) {
            console.warn(
                "[joo_web_fonts] Unknown font key received:",
                fontKey
            );
            return;
        }

        // Get existing <style> tag by ID or create a new one
        let style = document.getElementById(DYNAMIC_STYLE_ID);
        if (!style) {
            style = document.createElement("style");
            style.id = DYNAMIC_STYLE_ID;
            document.head.appendChild(style);
        }

        // Overwrite style rules for .joo-font
        style.innerHTML = `.joo-font { font-family: "${fontFamily}", serif !important; }`;

        console.debug("[joo_web_fonts] Applied font:", fontFamily);
    } catch (err) {
        console.error("[joo_web_fonts] Failed to load font configuration:", err);
    }
}

loadAndApplyFont();
