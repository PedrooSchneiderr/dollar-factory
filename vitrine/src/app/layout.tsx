import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "CleverUS Finds | Viral Amazon Must-Haves & Daily Gadget Deals",
  description:
    "Curated problem-solving gadgets and top-rated Amazon US finds seen on TikTok, Reels & Shorts. Search by video code (#01, #02...) for instant links.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-[#0b0f19] text-slate-100 antialiased selection:bg-amber-500 selection:text-slate-950">
        {/* Top Announcement Bar */}
        <div className="bg-gradient-to-r from-amber-500 via-orange-500 to-amber-500 text-slate-950 text-xs sm:text-sm font-bold py-2 px-4 text-center tracking-wide">
          🇺🇸 AS SEEN ON TIKTOK & REELS • TYPE YOUR VIDEO CODE (E.G. #01) BELOW FOR INSTANT AMAZON PRIME LINKS
        </div>

        {/* Header */}
        <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-[#0b0f19]/90 backdrop-blur-md">
          <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-400 to-orange-600 flex items-center justify-center text-slate-950 font-black text-lg shadow-lg shadow-amber-500/20">
                ⚡
              </div>
              <div>
                <span className="font-extrabold text-lg tracking-tight text-white">
                  Clever<span className="text-amber-400">US</span>Finds
                </span>
                <span className="block text-[10px] uppercase tracking-widest text-slate-400 -mt-1">
                  Verified Viral Gadgets
                </span>
              </div>
            </Link>

            <div className="flex items-center gap-3">
              <span className="hidden sm:inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                US Prime Fast Shipping
              </span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1">{children}</main>

        {/* Mandatory FTC & Amazon Associates Footer */}
        <footer className="border-t border-slate-800/80 bg-slate-950/80 mt-20 py-10 px-4 text-center text-xs text-slate-400">
          <div className="max-w-3xl mx-auto space-y-3">
            <p className="font-semibold text-slate-300">
              FTC & Amazon Associate Disclosure
            </p>
            <p className="leading-relaxed">
              <strong>As an Amazon Associate I earn from qualifying purchases.</strong>{" "}
              CleverUSFinds participates in the Amazon Services LLC Associates Program,
              an affiliate advertising program designed to provide a means for sites to
              earn advertising fees by advertising and linking to Amazon.com. Product
              prices and availability are accurate as of the date/time indicated and are
              subject to change.
            </p>
            <p className="text-slate-500 pt-2">
              © {new Date().getFullYear()} CleverUSFinds. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
