(this.webpackJsonpui_v2=this.webpackJsonpui_v2||[]).push([[13],{1329:function(e,t,n){},1366:function(e,t,n){"use strict";n.r(t);var a=n(3),i=n(6),o=n(0),c=n.n(o),l=n(14),s=n.n(l),r=n(1033),d=n.n(r),u=n(100),j=n.n(u),b=n(449),f=n(4),m=n(492),v=n(735),_=n(56),h=n(499),O=n(1);var x=function(e){var t=e.when,n=e.message,a=void 0===n?"Changes you made may not be saved.":n,o=e.confirmBtnText,l=void 0===o?"Leave":o,s=c.a.useState(!1),r=Object(i.a)(s,2),d=r[0],u=r[1],j=c.a.useState(""),b=Object(i.a)(j,2),m=b[0],v=b[1],x=c.a.useState(!1),p=Object(i.a)(x,2),N=p[0],C=p[1],g=Object(_.h)();function y(e){return t?(null===e||void 0===e||e.preventDefault(),e&&(e.returnValue="Your changes is not saved. Do you still want to leave"),""):void 0}function D(){u(!1)}return c.a.useEffect((function(){return N&&(g.push(m),C(!1)),window.addEventListener("beforeunload",y),function(){window.removeEventListener("beforeunload",y)}}),[N,t]),Object(O.jsxs)(O.Fragment,{children:[Object(O.jsx)(_.a,{when:t,message:function(e){return!!N||(function(e){u(!0),v(e)}(e.pathname),!1)}}),Object(O.jsx)(h.a,{open:d,onCancel:D,onSubmit:function(){D(),m&&C(!0)},text:a,icon:Object(O.jsx)(f.f,{name:"warning-contained"}),statusType:"warning",confirmBtnText:l,title:"Are you sure"})]})},p=n(223),N=n(225),C=n(246),g=n(222),y=n(867);var D=function(e){var t=e.children,n=c.a.useRef(null),a=c.a.useState(!1),o=Object(i.a)(a,2),l=o[0],s=o[1];return c.a.useEffect((function(){if(l){var e=n.current.parentNode.parentNode.parentNode;"notes-toolbar-popover"!==e.id&&(e.id="notes-toolbar-popover")}else s(!0)}),[l]),Object(O.jsx)("div",{ref:n,children:t})};n(1329);function T(e){var t,n=e.runHash,o=Object(C.a)(y.a),l=o.isLoading,r=o.noteData,u=o.notifyData,_=c.a.useState(""),h=Object(i.a)(_,2),T=h[0],w=h[1],M=c.a.useState(!0),E=Object(i.a)(M,2),S=E[0],R=E[1],k=c.a.useState(null),B=Object(i.a)(k,2),Y=B[0],P=B[1],L=c.a.useRef(null);c.a.useEffect((function(){return y.a.initialize(n),g.a(p.a.runDetails.tabs.notes.tabView),function(){y.a.destroy()}}),[]),c.a.useEffect((function(){var e;L.current&&(w((null===r||void 0===r?void 0:r.id)?null===r||void 0===r?void 0:r.content:""),P(Object(a.a)(Object(a.a)({},null===(e=L.current)||void 0===e?void 0:e.theme()),N.b)))}),[r]);var z=c.a.useCallback((function(){R(!0),(null===r||void 0===r?void 0:r.id)?H():y.a.onNoteCreate(n,{content:L.current.value()})}),[null===r||void 0===r?void 0:r.id,n]),H=c.a.useCallback((function(){y.a.onNoteUpdate(n,{content:L.current.value()})}),[n]),A=c.a.useCallback((function(e){var t=T===e();S!==t&&R(t)}),[S,T]);return Object(O.jsxs)("section",{className:"RunDetailNotesTab",children:[Object(O.jsx)(x,{when:!S}),Object(O.jsxs)("div",{className:s()("RunDetailNotesTab__Editor",{isLoading:l}),children:[Object(O.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel",children:[Object(O.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info",children:[(null===r||void 0===r?void 0:r.created_at)&&Object(O.jsx)(b.a,{title:"Created at",children:Object(O.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info-field",children:[Object(O.jsx)(f.f,{name:"calendar"}),Object(O.jsx)(f.l,{tint:70,children:"".concat(j.a.utc(null===r||void 0===r?void 0:r.created_at).local().format("YYYY-MM-DD HH:mm A"))})]})}),(null===r||void 0===r?void 0:r.updated_at)&&Object(O.jsx)(b.a,{title:"Updated at",children:Object(O.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info-field",children:[Object(O.jsx)(f.f,{name:"time"}),Object(O.jsx)(f.l,{tint:70,children:"".concat(j.a.utc(null===r||void 0===r?void 0:r.updated_at).local().format("YYYY-MM-DD HH:mm A"))})]})})]}),Object(O.jsx)(b.a,{title:"Save Note",children:Object(O.jsx)("div",{children:Object(O.jsx)(f.c,{disabled:S||l,variant:"contained",size:"small",onClick:z,children:"Save"})})})]}),Object(O.jsx)(d.a,{ref:L,className:"RunDetailNotesTab__Editor__container",value:T,placeholder:"Leave your Note",theme:Y||(null===(t=L.current)||void 0===t?void 0:t.theme()),disableExtensions:["table","image","container_notice"],tooltip:function(e){var t=e.children;return Object(O.jsx)(D,{children:t})},onChange:A}),l&&Object(O.jsx)(v.a,{})]}),u.length>0&&Object(O.jsx)(m.a,{handleClose:y.a.onNoteNotificationDelete,data:u})]})}T.displayName="RunDetailNotesTab";var w=c.a.memo(T);t.default=w},499:function(e,t,n){"use strict";var a=n(0),i=n.n(a),o=n(448),c=n(4),l=n(9),s=(n(503),n(1));function r(e){return Object(s.jsx)(l.a,{children:Object(s.jsxs)(o.a,{open:e.open,onClose:e.onCancel,"aria-labelledby":"dialog-title","aria-describedby":"dialog-description",PaperProps:{elevation:10},className:"ConfirmModal ConfirmModal__".concat(e.statusType),children:[Object(s.jsxs)("div",{className:"ConfirmModal__Body",children:[Object(s.jsx)(c.c,{size:"small",className:"ConfirmModal__Close__Icon",color:"secondary",withOnlyIcon:!0,onClick:e.onCancel,children:Object(s.jsx)(c.f,{name:"close"})}),Object(s.jsxs)("div",{className:"ConfirmModal__Title__Container",children:[Object(s.jsx)("div",{className:"ConfirmModal__Icon",children:e.icon}),e.title&&Object(s.jsx)(c.l,{size:16,tint:100,component:"h4",weight:600,children:e.title})]}),Object(s.jsxs)("div",{children:[e.description&&Object(s.jsx)(c.l,{className:"ConfirmModal__description",weight:400,component:"p",id:"dialog-description",children:e.description}),Object(s.jsxs)("div",{children:[e.text&&Object(s.jsx)(c.l,{className:"ConfirmModal__text",weight:400,component:"p",size:14,id:"dialog-description",children:e.text||""}),e.children&&e.children]})]})]}),Object(s.jsxs)("div",{className:"ConfirmModal__Footer",children:[Object(s.jsx)(c.c,{onClick:e.onCancel,className:"ConfirmModal__CancelButton",children:e.cancelBtnText}),Object(s.jsx)(c.c,{onClick:e.onSubmit,color:"primary",variant:"contained",className:"ConfirmModal__ConfirmButton",autoFocus:!0,children:e.confirmBtnText})]})]})})}r.defaultProps={confirmBtnText:"Confirm",cancelBtnText:"Cancel",statusType:"info"},r.displayName="ConfirmModal",t.a=i.a.memo(r)},503:function(e,t,n){}}]);
//# sourceMappingURL=RunDetailNotesTab.js.map?version=790ca44f4ce7413e7108