import{r as d,i as L,j as e,b,c as w,d as h,e as E,f as S,M as f,g as N,N as P,h as A,k as C,u as v,l as y,C as T,m as z,O as D}from"./index-3144ef62.js";import{S as F}from"./SplitPane-e3e6ef3d.js";import{I as M}from"./Input-81dfa79c.js";import{T as g}from"./TasksOverview-158a5095.js";import"./pluralize-ca1790d5.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./context-677a5bfa.js";function I({models:i,search:l,setSearch:t}){const r=d.useMemo(()=>i.map(n=>[n,n.index]),[i]),s=l!==""&&l.length>1,a=L(s)?[]:H(r,l);return e.jsxs("div",{className:"p-2 relative",children:[e.jsx(M,{className:"w-full !m-0",size:b.md,value:l,placeholder:"Search",onInput:n=>{t(n.target.value.trim())},autoFocus:!0}),s&&e.jsxs("ul",{className:"p-4 bg-theme dark:bg-theme-lighter absolute z-10 w-full top-16 left-0 right-0 rounded-lg max-h-[25vh] overflow-auto scrollbar scrollbar--vertical scrollbar--horizontal shadow-2xl",children:[w(a)&&e.jsx("li",{className:"p-2",onClick:()=>{t("")},children:"No Results Found"},"not-found"),h(a)&&a.map(([n,c])=>e.jsx(E,{to:`${S.IdeDocsModels}/${f.encodeName(n.name)}`,className:"text-md font-normal mb-1 w-full",children:e.jsxs("li",{className:"p-2 cursor-pointer hover:bg-secondary-10",children:[e.jsx("span",{className:"font-bold",children:n.name}),e.jsx("small",{className:"block text-neutral-600 p-2 italic",children:_(c,l)})]})},n.name))]})]})}function _(i,l){return e.jsx(e.Fragment,{children:i.split(l).reduce((t,r,s,a)=>(t.push(e.jsx(e.Fragment,{children:r})),s>0||s%2!==0||s===a.length||t.push(e.jsx("span",{className:"inline-block text-brand-500 bg-brand-10",children:l})),t),[])})}function H(i=[],l){return i.reduce((r,[s,a])=>{const n=a.indexOf(l.toLocaleLowerCase());if(n>-1){const c=Math.max(0,n-40),m=Math.min(a.length-1,n+l.length+40);r.push([s,(c>0?"... ":"")+a.slice(c,m)+(m<a.length?" ...":"")])}return r},[])}function R({models:i,filter:l,setFilter:t}){const r=Array.from(new Set(i.values())).filter(s=>l===""?!0:s.name.includes(l));return e.jsxs("div",{className:"flex flex-col w-full h-full",children:[e.jsxs("div",{className:"px-2 w-full flex justify-between",children:[e.jsx(M,{className:"w-full !m-0",size:b.sm,value:l,placeholder:"Filter models",onInput:s=>{t(s.target.value)}}),e.jsx("div",{className:"ml-3 px-3 bg-primary-10 text-primary-500 rounded-full text-xs flex items-center",children:r.length})]}),e.jsxs("ul",{className:"p-2 overflow-auto scrollbar scrollbar--horizontal scrollbar--vertical",children:[w(r)&&e.jsx("li",{className:"p-2",onClick:()=>{t("")},children:"No Results Found"},"not-found"),h(r)&&r.map(s=>e.jsx("li",{className:N("text-sm font-normal"),children:e.jsxs(P,{to:`${S.IdeDocsModels}/${f.encodeName(s.name)}`,className:({isActive:a})=>N("block px-2 overflow-hidden whitespace-nowrap overflow-ellipsis py-1 rounded-md w-full hover:bg-primary-10",a?"text-primary-500 bg-primary-10":"text-neutral-500 dark:text-neutral-100"),children:[s.name,e.jsxs("span",{title:s.type==="python"?"Column lineage disabled for Python models":"SQL Model",className:"inline-block ml-2 bg-primary-10 px-2 rounded-md text-[0.65rem]",children:[s.type==="python"&&"Python",s.type==="sql"&&"SQL",s.type==="seed"&&"Seed"]})]})},s.name))]})]})}function q(){const i=A(),{modelName:l}=C(),t=v(o=>o.models),r=v(o=>o.environment),s=y(o=>o.activePlan),a=y(o=>o.state),[n,c]=d.useState(""),[m,x]=d.useState(""),j=Array.from(t.entries()).reduce((o,[p,u])=>(u.name===p||(l==null||u.name!==f.decodeName(l))&&o.push(u),o),[]);return d.useEffect(()=>{x(""),c("")},[i.pathname]),e.jsx(T.Page,{children:e.jsxs("div",{className:"p-4 flex flex-col w-full h-full overflow-hidden",children:[h(j)&&e.jsx(I,{models:j,search:n,setSearch:c}),s!=null&&e.jsx("div",{className:"w-full p-4",children:e.jsx(g,{tasks:s.tasks,children:({total:o,completed:p,totalBatches:u,completedBatches:k})=>e.jsx(e.Fragment,{children:e.jsx(g.Summary,{environment:r.name,planState:a,headline:"Most Recent Plan",completed:p,total:o,totalBatches:u,completedBatches:k,updateType:s.type===z.Virtual?"Virtual":"Backfill",updatedAt:s.updated_at})})})}),e.jsxs(F,{className:"flex w-full h-full overflow-hidden mt-8",sizes:[25,75],minSize:0,snapOffset:0,children:[e.jsx("div",{className:"py-4 w-full",children:t.size>0&&e.jsx(R,{models:t,filter:m,setFilter:x})}),e.jsx("div",{className:"w-full",children:e.jsx(D,{})})]})]})})}export{q as default};
