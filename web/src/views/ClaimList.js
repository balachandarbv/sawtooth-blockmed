var m = require("mithril")
var Claim = require("../models/Claim")

module.exports = {
    oninit:
        function(vnode){
            Claim.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", Claim.list.map(function(claim) {
            return m("a.user-list-item", // {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link},
                "DESCRIPTION: " + claim.description +
                "; NAME: " + claim.name +
                "; SURNAME: " + claim.surname +
                "; ID: " + claim.id +
                "; CLIENT PKEY: " + claim.client_pkey +
                "; STATE: " + claim.state +
                "; PROVIDED SERVICE: " + claim.provided_service +
                "; CONTRACT ID: " + claim.contract_id +
                ";",
                m("div"),
                m("button", {
                    onclick: function() {
                        Claim.current.claim_id = claim.id
                        Claim.current.client_pkey = claim.client_pkey
//                        Claim.current.provided_service = "pills, lab tests"
                        Claim.current.contract_id = claim.contract_id
                        Claim.update(vnode.attrs.client_key)
                    }
                }, 'Update claim'),
                m("div"),
                m("button", {
                    onclick: function() {
                        Claim.current.claim_id = claim.id
                        Claim.current.client_pkey = claim.client_pkey
//                        Claim.current.provided_service = "pills, lab tests"
                        Claim.current.contract_id = claim.contract_id
                        Claim.close(vnode.attrs.client_key)
                    }
                }, 'Close claim')
            )
        }),
        m("label.label", "Provided Service"),
        m("input.input[placeholder=Provided Service]", {
            oninput: m.withAttr("value", function(value) {Claim.current.provided_service = value}),
            value: Claim.current.provided_service
        }),
        m("label.error", Claim.error))
    }
}