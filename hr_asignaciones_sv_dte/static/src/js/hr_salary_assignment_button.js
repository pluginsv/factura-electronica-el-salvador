/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { useService } from "@web/core/utils/hooks";

patch(ControlPanel.prototype, {
    name: "hr_asignaciones_sv_dte.salary_assignment_cp_button",

    get buttons() {
        const buttons = this._super();

        const action = useService("action");

        buttons.push({
            name: "download_template",
            string: "Descargar plantilla",
            classes: "btn btn-secondary",
            icon: "fa fa-download",
            click: () => {
                action.doAction({
                    type: "ir.actions.act_url",
                    url: "/hr_asignaciones_sv_dte/static/src/plantilla/plantilla_horas-extras.xls",
                    target: "new",
                });
            },
        });
        return buttons;
    },
});
