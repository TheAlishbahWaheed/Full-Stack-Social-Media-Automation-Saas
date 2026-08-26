"use client";
import { FormEvent,useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Field from "../../components/Field";
import { api,save } from "../../lib/api";

export default function Login(){
 const r=useRouter(); const[e,setE]=useState(""); const[p,setP]=useState(""); const[err,setErr]=useState(""); const[busy,setBusy]=useState(false);
 async function submit(x:FormEvent){x.preventDefault();setErr("");setBusy(true);try{const d=await api<{access_token:string}>("/auth/login",{method:"POST",body:JSON.stringify({email:e,password:p})});save(d.access_token);r.push("/dashboard")}catch(x){setErr(x instanceof Error?x.message:"Login failed")}finally{setBusy(false)}}
 return <main className="min-h-screen grid lg:grid-cols-2 bg-white">
  <div className="hidden lg:flex bg-[#0b1020] text-white p-14 flex-col justify-between"><div className="text-2xl font-black">Social<span className="text-[#8c84ff]">Flow</span></div><div><p className="text-5xl font-black leading-tight max-w-xl">Your social media, finally under control.</p><p className="mt-5 text-slate-300 max-w-lg text-lg">Plan content, schedule campaigns and see your publishing pipeline from one command center.</p></div><p className="text-slate-500 text-sm">SocialFlow v2.0</p></div>
  <div className="flex items-center justify-center p-6"><form onSubmit={submit} className="w-full max-w-md space-y-5"><div className="lg:hidden text-2xl font-black mb-10">Social<span className="text-[#635bff]">Flow</span></div><div><h1 className="text-3xl font-black">Welcome back</h1><p className="mt-2 muted">Sign in to your workspace.</p></div>{err&&<p className="rounded-xl bg-red-50 border border-red-100 p-3 text-sm text-red-700">{err}</p>}<Field label="Email" type="email" value={e} onChange={x=>setE(x.target.value)} required/><Field label="Password" type="password" value={p} onChange={x=>setP(x.target.value)} required/><button disabled={busy} className="btn btn-primary w-full py-3 disabled:opacity-60">{busy?"Signing in…":"Sign in"}</button><p className="text-center text-sm muted">New to SocialFlow? <Link className="text-[#635bff] font-semibold" href="/register">Create an account</Link></p></form></div>
 </main>
}
