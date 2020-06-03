var m = require("mithril")
var Claim = require("../models/Claim")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Claim.register(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "Patient pkey"),
            m("input.input[type=text][placeholder=Patient pkey]", {
                oninput: m.withAttr("value", function(value) {Claim.current.patient_pkey = value}),
                value: Claim.current.patient_pkey
            }),
            m("label.label", "Claim id"),
            m("input.input[placeholder=Claim id]", {
                oninput: m.withAttr("value", function(value) {Claim.current.claim_id = value}),
                value: Claim.current.claim_id
                }),
//            m("label.label", "Patient public key"),
//            m("input.input[placeholder=Patient public key]", {
//                oninput: m.withAttr("value", function(value) {Claim.current.patient_pkey = value}),
//                value: Claim.current.patient_pkey
//            }),
            m("label.label", "Description"),
            m("input.input[placeholder=Description]", {
                oninput: m.withAttr("value", function(value) {Claim.current.description = value}),
                value: Claim.current.description
            }),
            m("label.label", "Contract ID (optional)"),
            m("input.input[placeholder=Contract ID]", {
                oninput: m.withAttr("value", function(value) {Claim.current.contract_id = value}),
                value: Claim.current.contract_id
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Claim.error)
        ])
    }
}