import{r as f,R as me,v as Ne,w as Ce,l as L,u as P,x as De,y as Ae,z as fe,A as ke,B as Me,i as M,D as I,F as Fe,G as z,d as Q,j as n,g as C,H as B,I as U,b as T,J as Te,S as Ie,K as $e,P as ve,Q as Le}from"./index-3144ef62.js";import{I as ze}from"./Input-81dfa79c.js";import{M as O,C as Oe}from"./ModalConfirmation-42b6be93.js";import{E as A}from"./context-677a5bfa.js";import{F as Qe,P as he}from"./PlanChangePreview-3b6d61a6.js";import{S as xe,D as J,y as X,o as R,c as Be,u as Ee,d as H,X as Y,I as te,C as Ue,l as _,h as Ke,T as _e,a as w,r as Ge,b as ee,_ as Ve,M as pe,e as je,f as He}from"./keyboard-896332ff.js";import{L as Je,p as we,n as Xe,t as Pe}from"./transition-b76f66ee.js";import{s as Ye}from"./use-resolve-button-type-acdcfc49.js";import{L as ge}from"./popover-6da25bfe.js";import"./dialog-3d301c95.js";import"./context-a28ba8eb.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./ModelLineage-6e57704c.js";import"./Graph-4c19d482.js";import"./PlusIcon-75d92586.js";import"./disclosure-bc43cb4e.js";function qe({title:e,titleId:r,...a},t){return f.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:t,"aria-labelledby":r},a),e?f.createElement("title",{id:r},e):null,f.createElement("path",{fillRule:"evenodd",d:"M12.53 16.28a.75.75 0 01-1.06 0l-7.5-7.5a.75.75 0 011.06-1.06L12 14.69l6.97-6.97a.75.75 0 111.06 1.06l-7.5 7.5z",clipRule:"evenodd"}))}const We=f.forwardRef(qe),Ze=We;function et(e){throw new Error("Unexpected object: "+e)}var S=(e=>(e[e.First=0]="First",e[e.Previous=1]="Previous",e[e.Next=2]="Next",e[e.Last=3]="Last",e[e.Specific=4]="Specific",e[e.Nothing=5]="Nothing",e))(S||{});function tt(e,r){let a=r.resolveItems();if(a.length<=0)return null;let t=r.resolveActiveIndex(),i=t??-1,v=(()=>{switch(e.focus){case 0:return a.findIndex(o=>!r.resolveDisabled(o));case 1:{let o=a.slice().reverse().findIndex((s,m,l)=>i!==-1&&l.length-m-1>=i?!1:!r.resolveDisabled(s));return o===-1?o:a.length-1-o}case 2:return a.findIndex((o,s)=>s<=i?!1:!r.resolveDisabled(o));case 3:{let o=a.slice().reverse().findIndex(s=>!r.resolveDisabled(s));return o===-1?o:a.length-1-o}case 4:return a.findIndex(o=>r.resolveId(o)===e.id);case 5:return null;default:et(e)}})();return v===-1?t:v}function ye(e){return[e.screenX,e.screenY]}function nt(){let e=f.useRef([-1,-1]);return{wasMoved(r){let a=ye(r);return e.current[0]===a[0]&&e.current[1]===a[1]?!1:(e.current=a,!0)},update(r){e.current=ye(r)}}}var st=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(st||{}),rt=(e=>(e[e.Pointer=0]="Pointer",e[e.Other=1]="Other",e))(rt||{}),at=(e=>(e[e.OpenMenu=0]="OpenMenu",e[e.CloseMenu=1]="CloseMenu",e[e.GoToItem=2]="GoToItem",e[e.Search=3]="Search",e[e.ClearSearch=4]="ClearSearch",e[e.RegisterItem=5]="RegisterItem",e[e.UnregisterItem=6]="UnregisterItem",e))(at||{});function Z(e,r=a=>a){let a=e.activeItemIndex!==null?e.items[e.activeItemIndex]:null,t=He(r(e.items.slice()),v=>v.dataRef.current.domRef.current),i=a?t.indexOf(a):null;return i===-1&&(i=null),{items:t,activeItemIndex:i}}let it={[1](e){return e.menuState===1?e:{...e,activeItemIndex:null,menuState:1}},[0](e){return e.menuState===0?e:{...e,menuState:0}},[2]:(e,r)=>{var a;let t=Z(e),i=tt(r,{resolveItems:()=>t.items,resolveActiveIndex:()=>t.activeItemIndex,resolveId:v=>v.id,resolveDisabled:v=>v.dataRef.current.disabled});return{...e,...t,searchQuery:"",activeItemIndex:i,activationTrigger:(a=r.trigger)!=null?a:1}},[3]:(e,r)=>{let a=e.searchQuery!==""?0:1,t=e.searchQuery+r.value.toLowerCase(),i=(e.activeItemIndex!==null?e.items.slice(e.activeItemIndex+a).concat(e.items.slice(0,e.activeItemIndex+a)):e.items).find(o=>{var s;return((s=o.dataRef.current.textValue)==null?void 0:s.startsWith(t))&&!o.dataRef.current.disabled}),v=i?e.items.indexOf(i):-1;return v===-1||v===e.activeItemIndex?{...e,searchQuery:t}:{...e,searchQuery:t,activeItemIndex:v,activationTrigger:1}},[4](e){return e.searchQuery===""?e:{...e,searchQuery:"",searchActiveItemIndex:null}},[5]:(e,r)=>{let a=Z(e,t=>[...t,{id:r.id,dataRef:r.dataRef}]);return{...e,...a}},[6]:(e,r)=>{let a=Z(e,t=>{let i=t.findIndex(v=>v.id===r.id);return i!==-1&&t.splice(i,1),t});return{...e,...a,activationTrigger:1}}},ne=f.createContext(null);ne.displayName="MenuContext";function q(e){let r=f.useContext(ne);if(r===null){let a=new Error(`<${e} /> is missing a parent <Menu /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(a,q),a}return r}function ot(e,r){return Ee(r.type,it,e,r)}let lt=f.Fragment;function ct(e,r){let a=f.useReducer(ot,{menuState:1,buttonRef:f.createRef(),itemsRef:f.createRef(),items:[],searchQuery:"",activeItemIndex:null,activationTrigger:1}),[{menuState:t,itemsRef:i,buttonRef:v},o]=a,s=X(r);Je([v,i],(p,E)=>{var b;o({type:1}),Ke(E,_e.Loose)||(p.preventDefault(),(b=v.current)==null||b.focus())},t===0);let m=R(()=>{o({type:1})}),l=f.useMemo(()=>({open:t===0,close:m}),[t,m]),y=e,d={ref:s};return me.createElement(ne.Provider,{value:a},me.createElement(Be,{value:Ee(t,{[0]:H.Open,[1]:H.Closed})},Y({ourProps:d,theirProps:y,slot:l,defaultTag:lt,name:"Menu"})))}let ut="button";function dt(e,r){var a;let t=te(),{id:i=`headlessui-menu-button-${t}`,...v}=e,[o,s]=q("Menu.Button"),m=X(o.buttonRef,r),l=we(),y=R(g=>{switch(g.key){case w.Space:case w.Enter:case w.ArrowDown:g.preventDefault(),g.stopPropagation(),s({type:0}),l.nextFrame(()=>s({type:2,focus:S.First}));break;case w.ArrowUp:g.preventDefault(),g.stopPropagation(),s({type:0}),l.nextFrame(()=>s({type:2,focus:S.Last}));break}}),d=R(g=>{switch(g.key){case w.Space:g.preventDefault();break}}),p=R(g=>{if(Ge(g.currentTarget))return g.preventDefault();e.disabled||(o.menuState===0?(s({type:1}),l.nextFrame(()=>{var N;return(N=o.buttonRef.current)==null?void 0:N.focus({preventScroll:!0})})):(g.preventDefault(),s({type:0})))}),E=f.useMemo(()=>({open:o.menuState===0}),[o]),b={ref:m,id:i,type:Ye(e,o.buttonRef),"aria-haspopup":"menu","aria-controls":(a=o.itemsRef.current)==null?void 0:a.id,"aria-expanded":e.disabled?void 0:o.menuState===0,onKeyDown:y,onKeyUp:d,onClick:p};return Y({ourProps:b,theirProps:v,slot:E,defaultTag:ut,name:"Menu.Button"})}let mt="div",ft=xe.RenderStrategy|xe.Static;function vt(e,r){var a,t;let i=te(),{id:v=`headlessui-menu-items-${i}`,...o}=e,[s,m]=q("Menu.Items"),l=X(s.itemsRef,r),y=Xe(s.itemsRef),d=we(),p=Ue(),E=(()=>p!==null?(p&H.Open)===H.Open:s.menuState===0)();f.useEffect(()=>{let u=s.itemsRef.current;u&&s.menuState===0&&u!==(y==null?void 0:y.activeElement)&&u.focus({preventScroll:!0})},[s.menuState,s.itemsRef,y]),Qe({container:s.itemsRef.current,enabled:s.menuState===0,accept(u){return u.getAttribute("role")==="menuitem"?NodeFilter.FILTER_REJECT:u.hasAttribute("role")?NodeFilter.FILTER_SKIP:NodeFilter.FILTER_ACCEPT},walk(u){u.setAttribute("role","none")}});let b=R(u=>{var k,c;switch(d.dispose(),u.key){case w.Space:if(s.searchQuery!=="")return u.preventDefault(),u.stopPropagation(),m({type:3,value:u.key});case w.Enter:if(u.preventDefault(),u.stopPropagation(),m({type:1}),s.activeItemIndex!==null){let{dataRef:j}=s.items[s.activeItemIndex];(c=(k=j.current)==null?void 0:k.domRef.current)==null||c.click()}je(s.buttonRef.current);break;case w.ArrowDown:return u.preventDefault(),u.stopPropagation(),m({type:2,focus:S.Next});case w.ArrowUp:return u.preventDefault(),u.stopPropagation(),m({type:2,focus:S.Previous});case w.Home:case w.PageUp:return u.preventDefault(),u.stopPropagation(),m({type:2,focus:S.First});case w.End:case w.PageDown:return u.preventDefault(),u.stopPropagation(),m({type:2,focus:S.Last});case w.Escape:u.preventDefault(),u.stopPropagation(),m({type:1}),ee().nextFrame(()=>{var j;return(j=s.buttonRef.current)==null?void 0:j.focus({preventScroll:!0})});break;case w.Tab:u.preventDefault(),u.stopPropagation(),m({type:1}),ee().nextFrame(()=>{Ve(s.buttonRef.current,u.shiftKey?pe.Previous:pe.Next)});break;default:u.key.length===1&&(m({type:3,value:u.key}),d.setTimeout(()=>m({type:4}),350));break}}),g=R(u=>{switch(u.key){case w.Space:u.preventDefault();break}}),N=f.useMemo(()=>({open:s.menuState===0}),[s]),D={"aria-activedescendant":s.activeItemIndex===null||(a=s.items[s.activeItemIndex])==null?void 0:a.id,"aria-labelledby":(t=s.buttonRef.current)==null?void 0:t.id,id:v,onKeyDown:b,onKeyUp:g,role:"menu",tabIndex:0,ref:l};return Y({ourProps:D,theirProps:o,slot:N,defaultTag:mt,features:ft,visible:E,name:"Menu.Items"})}let ht=f.Fragment;function xt(e,r){let a=te(),{id:t=`headlessui-menu-item-${a}`,disabled:i=!1,...v}=e,[o,s]=q("Menu.Item"),m=o.activeItemIndex!==null?o.items[o.activeItemIndex].id===t:!1,l=f.useRef(null),y=X(r,l);_(()=>{if(o.menuState!==0||!m||o.activationTrigger===0)return;let c=ee();return c.requestAnimationFrame(()=>{var j,F;(F=(j=l.current)==null?void 0:j.scrollIntoView)==null||F.call(j,{block:"nearest"})}),c.dispose},[l,m,o.menuState,o.activationTrigger,o.activeItemIndex]);let d=f.useRef({disabled:i,domRef:l});_(()=>{d.current.disabled=i},[d,i]),_(()=>{var c,j;d.current.textValue=(j=(c=l.current)==null?void 0:c.textContent)==null?void 0:j.toLowerCase()},[d,l]),_(()=>(s({type:5,id:t,dataRef:d}),()=>s({type:6,id:t})),[d,t]);let p=R(()=>{s({type:1})}),E=R(c=>{if(i)return c.preventDefault();s({type:1}),je(o.buttonRef.current)}),b=R(()=>{if(i)return s({type:2,focus:S.Nothing});s({type:2,focus:S.Specific,id:t})}),g=nt(),N=R(c=>g.update(c)),D=R(c=>{g.wasMoved(c)&&(i||m||s({type:2,focus:S.Specific,id:t,trigger:0}))}),u=R(c=>{g.wasMoved(c)&&(i||m&&s({type:2,focus:S.Nothing}))}),k=f.useMemo(()=>({active:m,disabled:i,close:p}),[m,i,p]);return Y({ourProps:{id:t,ref:y,role:"menuitem",tabIndex:i===!0?void 0:-1,"aria-disabled":i===!0?!0:void 0,disabled:void 0,onClick:E,onFocus:b,onPointerEnter:N,onMouseEnter:N,onPointerMove:D,onMouseMove:D,onPointerLeave:u,onMouseLeave:u},theirProps:v,slot:k,defaultTag:ht,name:"Menu.Item"})}let pt=J(ct),gt=J(dt),yt=J(vt),bt=J(xt),G=Object.assign(pt,{Button:gt,Items:yt,Item:bt});function zt(){var re,ae,ie,oe,le,ce,ue,de;const e=Ne(),{errors:r,setIsPlanOpen:a}=Ce(),t=L(h=>h.state),i=L(h=>h.action),v=L(h=>h.setState),o=L(h=>h.setAction),s=L(h=>h.setActivePlan),m=P(h=>h.models),l=P(h=>h.environment),y=P(h=>h.environments),d=P(h=>h.setInitialDates),p=P(h=>h.addSyncronizedEnvironments),E=P(h=>h.hasSyncronizedEnvironments),[b,g]=f.useState(!1),[N,D]=f.useState(!1),{refetch:u}=De(),{refetch:k,data:c,isFetching:j}=Ae(l.name,{planOptions:{skip_tests:!0}}),F=f.useCallback(fe(u,1e3,!0),[u]),K=f.useCallback(fe(k,1e3,!0),[k]),x=f.useMemo(()=>l.isDefault?{headline:"Running Plan Directly On Prod Environment!",description:"Are you sure you want to run your changes directly on prod? Safer choice will be to select or add new environment first.",yesText:`Yes, Run ${l.name}`,noText:"No, Cancel",action(){W()}}:void 0,[l]);f.useEffect(()=>()=>{F.cancel(),K.cancel(),ke(e),Me(e)},[]),f.useEffect(()=>{M(l.isSyncronized)||K().finally(()=>{N&&(W(),D(!1))})},[l,N]),f.useEffect(()=>{t===I.Finished&&(K(),F())},[t]),f.useEffect(()=>{d(c==null?void 0:c.start,c==null?void 0:c.end)},[c]),f.useEffect(()=>{m.size>0&&M(E())&&F().then(({data:h})=>{h==null||Fe(h)||p(Object.values(h))}),E()&&K()},[m,y]);function W(){s(void 0),v(I.Init),o(z.Run),a(!0)}const Se=[(re=c==null?void 0:c.changes)==null?void 0:re.added,(ae=c==null?void 0:c.changes)==null?void 0:ae.removed,(oe=(ie=c==null?void 0:c.changes)==null?void 0:ie.modified)==null?void 0:oe.direct,(ce=(le=c==null?void 0:c.changes)==null?void 0:le.modified)==null?void 0:ce.indirect,(de=(ue=c==null?void 0:c.changes)==null?void 0:ue.modified)==null?void 0:de.metadata].some(Q),se=r.size>0;return n.jsxs("div",{className:C("flex items-center",l==null&&"opacity-50 pointer-events-none cursor-not-allowed"),children:[n.jsxs("div",{className:"flex items-center relative",children:[n.jsxs(B,{className:C("mx-0",M(l.isInitial&&l.isDefault)&&"rounded-none rounded-l-lg border-r"),disabled:se||j||i!==z.None||t===I.Applying||t===I.Running||t===I.Cancelling,variant:U.Alternative,size:T.sm,onClick:h=>{h.stopPropagation(),l.isDefault&&M(l.isInitial)?g(!0):W()},children:[Te([I.Applying,I.Running,I.Cancelling],t)&&n.jsx(Ie,{className:"w-3 h-3 mr-1"}),n.jsx("span",{className:"inline-block",children:t===I.Running?"Running Plan...":t===I.Applying?"Applying Plan...":t===I.Cancelling?"Cancelling Plan...":i!==z.None?"Setting Plan...":"Run Plan"})]}),(M(l.isInitial)||M(l.isDefault))&&n.jsx(be,{className:"rounded-none rounded-r-lg border-l mx-0",environment:l,disabled:se||j||i!==z.None||t===I.Applying||t===I.Running||t===I.Cancelling})]}),t!==I.Applying&&n.jsx(It,{environment:l,plan:c,isLoading:j,hasChanges:Se}),n.jsxs(O,{show:b,onClose:()=>{},children:[n.jsxs(O.Main,{children:[(x==null?void 0:x.headline)!=null&&n.jsx(O.Headline,{children:x==null?void 0:x.headline}),(x==null?void 0:x.description)!=null&&n.jsx(O.Description,{children:x==null?void 0:x.description}),n.jsxs("div",{className:"mt-5 pt-4",children:[n.jsx("h4",{className:"mb-2",children:`${y.size>1?"Select or ":""}Add Environment`}),n.jsxs("div",{className:"flex items-center relative",children:[y.size>1&&n.jsx(be,{className:"mr-2",side:"left",environment:l,showAddEnvironemnt:!1,onSelect:()=>{D(!0),g(!1)},size:T.md,disabled:j||i!==z.None||t===I.Applying||t===I.Cancelling}),n.jsx(Re,{className:"w-full",size:T.md,onAdd:()=>{D(!0),g(!1)}})]})]})]}),n.jsxs(O.Actions,{children:[n.jsx(B,{className:"font-bold",size:"md",variant:U.Primary,onClick:h=>{var $;h.stopPropagation(),($=x==null?void 0:x.action)==null||$.call(x),g(!1)},children:(x==null?void 0:x.yesText)??"Confirm"}),n.jsx(B,{size:"md",variant:U.Neutral,onClick:h=>{var $;h.stopPropagation(),($=x==null?void 0:x.cancel)==null||$.call(x),g(!1)},children:(x==null?void 0:x.noText)??"Cancel"})]})]})]})}function It({isLoading:e,hasChanges:r,environment:a,plan:t}){var i,v,o,s,m,l,y,d,p,E;return n.jsx("span",{className:"flex align-center pr-2 h-full w-full",children:n.jsxs(n.Fragment,{children:[a.isInitial&&a.isSyncronized&&n.jsx("span",{title:"New",className:"block ml-1 px-2 first-child:ml-0 rounded-full bg-success-10 text-success-500 text-xs text-center font-bold",children:"New"}),e&&n.jsxs("span",{className:"flex items-center ml-2",children:[n.jsx(Ie,{className:"w-3 h-3 mr-1"}),n.jsx("span",{className:"inline-block text-xs text-neutral-500",children:"Checking..."})]}),[r,e,a.isLocal].every(M)&&n.jsx("span",{title:"Latest",className:"block ml-1 px-2 first-child:ml-0 rounded-full bg-neutral-10 text-xs text-center",children:n.jsx("span",{children:"Latest"})}),((i=t==null?void 0:t.changes)==null?void 0:i.added)!=null&&Q((v=t==null?void 0:t.changes)==null?void 0:v.added)&&n.jsx(V,{headline:"Added Models",type:A.Add,changes:t.changes.added}),((s=(o=t==null?void 0:t.changes)==null?void 0:o.modified)==null?void 0:s.direct)!=null&&Q((m=t==null?void 0:t.changes)==null?void 0:m.modified.direct)&&n.jsx(V,{headline:"Direct Changes",type:A.Direct,changes:t.changes.modified.direct.map(({model_name:b})=>b)}),((y=(l=t==null?void 0:t.changes)==null?void 0:l.modified)==null?void 0:y.indirect)!=null&&Q((d=t==null?void 0:t.changes)==null?void 0:d.modified.indirect)&&n.jsx(V,{headline:"Indirectly Modified",type:A.Indirect,changes:t.changes.modified.indirect.map(b=>b.model_name)}),((p=t==null?void 0:t.changes)==null?void 0:p.removed)!=null&&Q((E=t==null?void 0:t.changes)==null?void 0:E.removed)&&n.jsx(V,{headline:"Removed Models",type:A.Remove,changes:t.changes.removed})]})})}function be({onSelect:e,environment:r,disabled:a,side:t="right",className:i,showAddEnvironemnt:v=!0,size:o=T.sm}){const s=P(d=>d.environments),m=P(d=>d.setEnvironment),l=P(d=>d.removeLocalEnvironment),y=$e(G.Button);return n.jsx(G,{children:({close:d})=>n.jsxs(n.Fragment,{children:[n.jsxs(y,{variant:U.Alternative,size:o,disabled:a,className:C(i),children:[n.jsx("span",{className:"block overflow-hidden truncate",children:r.name}),n.jsx("span",{className:"pointer-events-none inset-y-0 right-0 flex items-center pl-2",children:n.jsx(Ze,{className:"h-4 w-4","aria-hidden":"true"})})]}),n.jsx(Pe,{as:f.Fragment,leave:"transition ease-in duration-100",leaveFrom:"opacity-100",leaveTo:"opacity-0",children:n.jsxs("div",{className:C("absolute top-9 overflow-hidden shadow-xl bg-theme border-2 border-primary-20 rounded-md flex flex-col z-10",t==="left"&&"left-0",t==="right"&&"right-0"),children:[n.jsxs(G.Items,{className:"overflow-auto max-h-80 py-2 scrollbar scrollbar--vertical",children:[Array.from(s).map(p=>n.jsx(G.Item,{children:({active:E})=>n.jsxs("div",{onClick:b=>{b.stopPropagation(),m(p),e==null||e()},className:C("flex justify-between items-center px-4 py-1 cursor-pointer overflow-auto",E&&"bg-primary-10",p===r&&"pointer-events-none cursor-default bg-secondary-10"),children:[n.jsxs("div",{className:"flex items-start",children:[n.jsx(Oe,{className:C("w-4 h-4 text-primary-500 mt-1",E&&"opacity-10",p!==r&&"opacity-0")}),n.jsxs("span",{className:"block",children:[n.jsxs("span",{className:"flex items-center",children:[n.jsx("span",{className:C("block truncate ml-2",p.isSyncronized&&"text-primary-500"),children:p.name}),n.jsxs("small",{className:"block ml-2",children:["(",p.type,")"]})]}),p.isDefault&&n.jsx("span",{className:"flex ml-2",children:n.jsx("small",{className:"text-xs text-neutral-500",children:"Default Environment"})})]})]}),p.isLocal&&p!==r&&n.jsx(B,{className:"my-0 mx-0",size:T.xs,variant:U.Neutral,onClick:b=>{b.stopPropagation(),l(p)},children:"-"})]})},p.name)),v&&n.jsxs(n.Fragment,{children:[n.jsx(ve,{}),n.jsx(Re,{onAdd:d,className:"mt-2 px-2"})]})]}),n.jsx(ve,{})]})})]})})}function Re({onAdd:e,className:r,label:a="Add",size:t=T.sm}){const i=P(d=>d.getNextEnvironment),v=P(d=>d.isExistingEnvironment),o=P(d=>d.addLocalEnvironment),[s,m]=f.useState(""),[l,y]=f.useState(i().name);return n.jsxs("div",{className:C("flex w-full items-center",r),children:[n.jsx(ze,{className:"my-0 mx-0 mr-4 min-w-[10rem] w-full",size:t,placeholder:"Environment",value:s,onInput:d=>{d.stopPropagation(),m(d.target.value)}}),n.jsx(B,{className:"my-0 mx-0 font-bold",size:t,disabled:Le(s)||v(s),onClick:d=>{d.stopPropagation(),o(s,l),m(""),y(i().name),e==null||e()},children:a})]})}function V({headline:e,type:r,changes:a}){const[t,i]=f.useState(!1);return n.jsx(ge,{onMouseEnter:()=>{i(!0)},onMouseLeave:()=>{i(!1)},className:"relative flex",children:()=>n.jsxs(n.Fragment,{children:[n.jsx("span",{className:C("inline-block ml-1 px-2 rounded-full text-xs font-bold text-neutral-100 cursor-default border border-inherit",r===A.Add&&"bg-success-500 border-success-500",r===A.Remove&&"bg-danger-500 border-danger-500",r===A.Direct&&"bg-secondary-500 border-secondary-500",r===A.Indirect&&"bg-warning-500 border-warning-500",r==="metadata"&&"bg-neutral-500 border-neutral-500"),children:a.length}),n.jsx(Pe,{show:t,as:f.Fragment,enter:"transition ease-out duration-200",enterFrom:"opacity-0 translate-y-1",enterTo:"opacity-100 translate-y-0",leave:"transition ease-in duration-150",leaveFrom:"opacity-100 translate-y-0",leaveTo:"opacity-0 translate-y-1",children:n.jsx(ge.Panel,{className:"absolute right-1 z-10 mt-8 transform flex p-2 bg-theme-lighter shadow-xl focus:ring-2 ring-opacity-5 rounded-lg ",children:n.jsx(he,{headline:e,type:r,className:"w-full h-full max-h-[40vh] overflow-hidden overflow-y-auto ",children:n.jsx(he.Default,{type:r,changes:a})})})})]})})}export{zt as default};
