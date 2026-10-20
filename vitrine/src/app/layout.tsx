import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { CheckCircle2, ShieldCheck } from "lucide-react";

export const metadata: Metadata = {
  title: "Clever Finds US | Field-Tested Amazon Essentials & Daily Problem Solvers",
  description:
    "Independent testing and curated essentials from Amazon US. Verified Prime listings with video demonstrations and honest product breakdowns.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-slate-900 selection:text-white">
        {/* Subtle Editorial Top Notice */}
        <div className="bg-slate-100 border-b border-slate-200/80 text-slate-600 text-[11px] sm:text-xs py-2 px-4 text-center font-medium tracking-tight">
          <span>🇺🇸 Independent, field-tested recommendations • Direct links to verified Amazon Prime listings</span>
        </div>

        {/* Editorial Header */}
        <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
          <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center text-white font-serif font-black text-base shadow-sm group-hover:bg-slate-800 transition-colors">
                C
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg tracking-tight text-slate-900 leading-none">
                  Clever Finds <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200 ml-1">US</span>
                </span>
                <span className="text-[10px] uppercase tracking-widest text-slate-500 font-medium mt-0.5">
                  Consumer Reviews & Curated Essentials
                </span>
              </div>
            </Link>

            <div className="flex items-center gap-2 sm:gap-4">
              <div className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Amazon Prime Verified</span>
              </div>
              <div className="inline-flex items-center gap-1.5 text-xs text-slate-500">
                <ShieldCheck className="w-4 h-4 text-slate-400" />
                <span className="hidden md:inline">100% Free Service</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Body */}
        <main className="flex-1">{children}</main>

        {/* Trust & FTC Compliance Footer */}
        <footer className="border-t border-slate-200 bg-white mt-20 py-12 px-4 text-slate-500 text-xs">
          <div className="max-w-4xl mx-auto space-y-4 text-center sm:text-left sm:flex sm:items-start sm:justify-between sm:space-y-0 gap-8">
            <div className="max-w-xl space-y-2">
              <p className="font-semibold text-slate-900 text-sm">
                About Clever Finds US & FTC Disclosure
              </p>
              <p className="leading-relaxed text-slate-500">
                <strong>As an Amazon Associate, we earn from qualifying purchases.</strong> Clever Finds US participates in the Amazon Services LLC Associates Program, an affiliate advertising initiative that enables publications to earn advertising fees by linking directly to official listings on Amazon.com.
              </p>
              <p className="leading-relaxed text-slate-400">
                Prices, ratings, and Prime availability are confirmed on the date of publication and may vary. We never hold inventory or charge customers directly.
              </p>
            </div>
            <div className="space-y-1 text-slate-400 text-[11px] sm:text-right shrink-0">
              <p className="font-medium text-slate-600">Editorial Independence Guarantee</p>
              <p>Independent Product Testing</p>
              <p>Official 30-Day Amazon Return Policy Applies</p>
              <p className="pt-3 text-slate-400">© {new Date().getFullYear()} Clever Finds US. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
