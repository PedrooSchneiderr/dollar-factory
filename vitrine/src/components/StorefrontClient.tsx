"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { Search, Star, Play, CheckCircle2, ArrowRight, ShieldCheck, Sparkles } from "lucide-react";

export interface Product {
  id: string;
  code: string;
  slug: string;
  title: string;
  short_title: string;
  niche: string;
  price: number;
  old_price: number;
  rating: number;
  reviews_count: number;
  amazon_asin: string;
  amazon_url: string;
  pain_point: string;
  visual_hook: string;
  solution_summary: string;
  benefits: string[];
  image_url: string;
  gallery_urls: string[];
  video_url: string | null;
  badge: string;
}

export default function StorefrontClient({ products }: { products: Product[] }) {
  const [query, setQuery] = useState("");
  const [selectedNiche, setSelectedNiche] = useState("All");

  const niches = useMemo(() => {
    const set = new Set(products.map((p) => p.niche));
    return ["All", ...Array.from(set)];
  }, [products]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase().replace(/^#/, "");
    return products.filter((p) => {
      const matchesNiche = selectedNiche === "All" || p.niche === selectedNiche;
      if (!q) return matchesNiche;
      const codeClean = p.code.toLowerCase().replace(/^#/, "");
      return (
        matchesNiche &&
        (codeClean.includes(q) ||
          p.id.toLowerCase().includes(q) ||
          p.short_title.toLowerCase().includes(q) ||
          p.title.toLowerCase().includes(q) ||
          p.niche.toLowerCase().includes(q))
      );
    });
  }, [products, query, selectedNiche]);

  return (
    <div className="max-w-6xl mx-auto px-4 pt-10 pb-16">
      {/* Editorial Hero */}
      <div className="text-center max-w-2xl mx-auto mb-10">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold uppercase tracking-wider mb-4">
          <Sparkles className="w-3.5 h-3.5 text-slate-600" />
          Field-Tested Curations • Amazon Prime
        </div>
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900 mb-4 font-serif">
          Practical Everyday Finds, <br className="hidden sm:inline" />
          Independently Tested.
        </h1>
        <p className="text-slate-600 text-sm sm:text-base leading-relaxed mb-8">
          Looking for a tool featured in our video reviews? Enter the video code (e.g.{" "}
          <span className="font-bold text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">#01</span> or{" "}
          <span className="font-bold text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">#02</span>) below for direct, verified Amazon links.
        </p>

        {/* Clean Search Input */}
        <div className="relative max-w-xl mx-auto">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by code (#01, #02...) or keyword..."
            className="w-full pl-12 pr-20 py-3.5 rounded-xl bg-white border border-slate-300 focus:border-slate-900 focus:ring-1 focus:ring-slate-900 focus:outline-none text-slate-900 placeholder-slate-400 text-sm sm:text-base shadow-sm transition-all"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-600"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex items-center justify-center gap-2 overflow-x-auto pb-4 mb-10 no-scrollbar">
        {niches.map((niche) => {
          const active = selectedNiche === niche;
          return (
            <button
              key={niche}
              onClick={() => setSelectedNiche(niche)}
              className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold whitespace-nowrap transition-all cursor-pointer ${
                active
                  ? "bg-slate-900 text-white shadow-sm"
                  : "bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200"
              }`}
            >
              {niche === "All" ? "All Recommendations" : niche}
            </button>
          );
        })}
      </div>

      {/* Product Grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8 max-w-md mx-auto">
          <p className="text-base font-bold text-slate-800 mb-1">
            No recommendation found for &ldquo;{query}&rdquo;
          </p>
          <p className="text-xs text-slate-500 mb-5">
            Please search for a code between #01 and #10, or browse categories.
          </p>
          <button
            onClick={() => {
              setQuery("");
              setSelectedNiche("All");
            }}
            className="px-4 py-2 rounded-lg bg-slate-900 text-white font-semibold text-xs"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((item) => {
            const hasRealDiscount = item.old_price > item.price;
            const discountPct = hasRealDiscount
              ? Math.round(((item.old_price - item.price) / item.old_price) * 100)
              : 0;

            return (
              <div
                key={item.id}
                className="group rounded-2xl bg-white border border-slate-200 hover:border-slate-400 overflow-hidden flex flex-col transition-all duration-200 shadow-sm hover:shadow-md"
              >
                {/* Image Section */}
                <Link
                  href={`/p/${item.id}`}
                  className="relative aspect-square bg-white p-6 overflow-hidden flex items-center justify-center border-b border-slate-100"
                >
                  <img
                    src={item.image_url}
                    alt={item.short_title}
                    className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300"
                  />

                  {/* Code Tag Top-Left */}
                  <div className="absolute top-3 left-3 flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-md bg-slate-900 text-white font-mono font-bold text-xs tracking-wider">
                      {item.code}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 text-slate-600 border border-slate-200">
                      {item.niche}
                    </span>
                  </div>

                  {/* Verified Discount Badge (Only if real discount exists) */}
                  {hasRealDiscount && discountPct > 0 && (
                    <span className="absolute top-3 right-3 px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
                      Save {discountPct}%
                    </span>
                  )}

                  {/* Video demo pill */}
                  {item.video_url && (
                    <div className="absolute bottom-3 right-3 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900/80 backdrop-blur-sm text-white text-[11px] font-medium">
                      <Play className="w-3 h-3 fill-white" />
                      Video Demo
                    </div>
                  )}
                </Link>

                {/* Card Body */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div>
                    {/* Ratings */}
                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-2">
                      <div className="flex items-center text-amber-500 font-bold">
                        <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400 mr-1" />
                        <span>{item.rating.toFixed(1)}</span>
                      </div>
                      <span>•</span>
                      <span>{item.reviews_count.toLocaleString()}+ reviews</span>
                    </div>

                    {/* Title */}
                    <Link href={`/p/${item.id}`}>
                      <h2 className="font-bold text-slate-900 text-base leading-snug group-hover:text-slate-600 transition-colors line-clamp-2">
                        {item.title}
                      </h2>
                    </Link>

                    {/* Problem Solved Summary */}
                    <p className="text-xs text-slate-500 mt-2 line-clamp-2 leading-relaxed">
                      {item.solution_summary}
                    </p>
                  </div>

                  {/* Pricing and Action */}
                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                    <div>
                      <div className="flex items-baseline gap-2">
                        <span className="text-xl font-bold text-slate-900">
                          ${item.price.toFixed(2)}
                        </span>
                        {/* Only strikethrough if old_price > price */}
                        {hasRealDiscount && (
                          <span className="text-xs text-slate-400 line-through">
                            ${item.old_price.toFixed(2)}
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-emerald-600 font-semibold flex items-center gap-1 mt-0.5">
                        <CheckCircle2 className="w-3 h-3" /> Prime Eligible
                      </span>
                    </div>

                    <Link
                      href={`/p/${item.id}`}
                      className="inline-flex items-center gap-1 text-xs font-semibold px-3.5 py-2 rounded-lg bg-slate-900 text-white hover:bg-slate-800 transition-colors"
                    >
                      <span>Review</span>
                      <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Trust Badges Banner at Bottom */}
      <div className="mt-16 p-6 rounded-2xl bg-white border border-slate-200 grid grid-cols-1 sm:grid-cols-3 gap-6 text-center sm:text-left">
        <div className="flex items-start gap-3 justify-center sm:justify-start">
          <CheckCircle2 className="w-5 h-5 text-slate-700 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Independent Testing</h4>
            <p className="text-xs text-slate-500 mt-0.5">All products are selected based on real utility and verified customer ratings.</p>
          </div>
        </div>
        <div className="flex items-start gap-3 justify-center sm:justify-start">
          <ShieldCheck className="w-5 h-5 text-slate-700 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Secure Amazon Checkout</h4>
            <p className="text-xs text-slate-500 mt-0.5">Orders and payments are processed directly by Amazon with standard return policies.</p>
          </div>
        </div>
        <div className="flex items-start gap-3 justify-center sm:justify-start">
          <Sparkles className="w-5 h-5 text-slate-700 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Updated Daily</h4>
            <p className="text-xs text-slate-500 mt-0.5">Pricing and Prime delivery status are refreshed continuously.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
