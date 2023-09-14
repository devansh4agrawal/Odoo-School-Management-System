/* @odoo-module */
// import { Component } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

// const { registry } = require("@web/core/registry");

class HelloWorld extends Component {
   static template = "HelloWorld"
}

registry.category("actions").add("action_component", HelloWorld);