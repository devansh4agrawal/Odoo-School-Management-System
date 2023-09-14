odoo.define('school.Custom', function (require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class CustomDemoButtons extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.myfunction);
        }
        myfunction() {
            console.log("Button Clicked")
        }
    }
    CustomDemoButtons.template = 'CustomDemoButtons';
    ProductScreen.addControlButton({
        component: CustomDemoButtons,
        condition: function () {
            return this.env.pos;
        },
    });
    Registries.Component.add(CustomDemoButtons);
    return CustomDemoButtons;
});