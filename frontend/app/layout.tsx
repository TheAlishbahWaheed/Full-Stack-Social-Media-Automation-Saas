import "./globals.css";
export const metadata = { title: "SocialFlow — Social Media Command Center", description: "Plan, schedule and manage social content." };
export default function Layout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
