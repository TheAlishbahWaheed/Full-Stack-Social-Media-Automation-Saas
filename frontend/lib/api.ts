const BASE=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";
export async function api<T>(path:string,options:RequestInit={}):Promise<T>{
 const token=typeof window!=="undefined"?localStorage.getItem("token"):null;
 const r=await fetch(BASE+path,{...options,headers:{"Content-Type":"application/json",...(token?{Authorization:`Bearer ${token}`}:{})}});
 const data=await r.json().catch(()=>({})); if(!r.ok) throw new Error(data.detail||"Request failed"); return data;
}
export const save=(t:string)=>localStorage.setItem("token",t); export const logout=()=>localStorage.removeItem("token");
