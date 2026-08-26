const BASE=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";

export async function api<T>(path:string, options:RequestInit={}):Promise<T>{
 const token=typeof window!=="undefined"?localStorage.getItem("token"):null;
 const headers=new Headers(options.headers);
 if(!headers.has("Content-Type")) headers.set("Content-Type","application/json");
 if(token) headers.set("Authorization",`Bearer ${token}`);
 const response=await fetch(BASE+path,{...options,headers});
 const data=await response.json().catch(()=>({}));
 if(!response.ok){
   if(response.status===401 && typeof window!=="undefined") localStorage.removeItem("token");
   const detail=Array.isArray(data.detail)?data.detail.map((x:{msg?:string})=>x.msg||"Invalid value").join(", "):data.detail;
   throw new Error(detail||`Request failed (${response.status})`);
 }
 return data as T;
}
export const save=(t:string)=>localStorage.setItem("token",t);
export const logout=()=>localStorage.removeItem("token");
