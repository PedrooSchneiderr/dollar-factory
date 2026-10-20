"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { Search, Star, Play, Flame, Sparkles, CheckCircle2 } from "lucide-react";
import OutboundButton from "./OutboundButton";

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
      const matchesQuery =
        codeClean.includes(q) ||
        p.id.toLowerCase().includes(q) ||
        p.short_title.toLowerCase().includes(q) ||
        p.title.toLowerCase().includes(q) ||
        p.niche.toLowerCase().includes(q);
      return matchesNiche && matchesQuery;
    });
  }, [products, query, selectedNiche]);

  return (
    <div className="max-w-6xl mx-auto px-4 pt-8 pb-12">
      {/* Hero + Code Search */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-wider mb-4">
          <Sparkles className="w-3.5 h-3.5" />
          Curated Problem-Solving Finds
        </div>
        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white mb-4">
          Viral Amazon US Finds{" "}
          <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
            That Actually Work
          </span>
        </h1>
        <p className="text-slate-400 text-sm sm:text-base mb-6">
          Saw a gadget in our TikTok, Reels, or Shorts? Type the{" "}
          <span className="text-amber-400 font-bold">#Code</span> (like{" "}
          <code className="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">#01</code> or{" "}
          <code className="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">#02</code>) or
          search by name below.
        </p>

        {/* Instant Search Input */}
        <div className="relative max-w-xl mx-auto">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by video code (e.g. #01, 02) or product name..."
            className="w-full pl-12 pr-24 py-4 rounded-2xl bg-slate-900/90 border-2 border-slate-800 focus:border-amber-400 focus:outline-none text-white placeholder-slate-500 text-sm sm:text-base shadow-xl"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex items-center justify-center gap-2 overflow-x-auto pb-4 mb-8 no-scrollbar">
        {niches.map((niche) => {
          const active = selectedNiche === niche;
          return (
            <button
              key={niche}
              onClick={() => setSelectedNiche(niche)}
              className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all cursor-pointer ${
                active
                  ? "bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/20"
                  : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800"
              }`}
            >
              {niche === "All" ? "🔥 All Viral Finds" : niche}
            </button>
          );
        })}
      </div>

      {/* Product Grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-16 bg-slate-900/40 rounded-3xl border border-slate-800">
          <p className="text-lg font-bold text-slate-300 mb-2">
            No gadget found for &ldquo;{query}&rdquo;
          </p>
          <p className="text-sm text-slate-500 mb-4">
            Try searching a code from #01 to #10 or clearing your filters.
          </p>
          <button
            onClick={() => {
              setQuery("");
              setSelectedNiche("All");
            }}
            className="px-4 py-2 rounded-xl bg-amber-400 text-slate-950 font-bold text-sm"
          >
            Show All Finds
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((item) => {
            const discountPct = Math.round(
              ((item.old_price - item.price) / item.old_price) * 100
            );
            return (
              <div
                key={item.id}
                className="group rounded-3xl bg-slate-900/70 border border-slate-800/90 hover:border-amber-500/50 overflow-hidden flex flex-col transition-all duration-200 hover:shadow-2xl hover:shadow-amber-500/5"
              >
                {/* Image / Video Preview Header */}
                <Link href={`/p/${item.id}`} className="relative aspect-[4/3] bg-slate-950 overflow-hidden block">
                  <img
                    src={item.image_url}
                    alt={item.short_title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent" />

                  {/* Code Badge */}
                  <div className="absolute top-3 left-3 flex items-center gap-2">
                    <span className="px-3 py-1 rounded-xl bg-amber-400 text-slate-950 font-black text-sm shadow-md">
                      {item.code}
                    </span>
                    <span className="px-2.5 py-1 rounded-lg bg-slate-950/80 backdrop-blur-md text-white text-xs font-bold border border-slate-700">
                      {item.badge}
                    </span>
                  </div>

                  {/* Discount Badge */}
                  {discountPct > 0 && (
                    <span className="absolute top-3 right-3 px-2.5 py-1 rounded-lg bg-rose-500 text-white font-extrabold text-xs">
                      -{discountPct}% OFF
                    </span>
                  )}

                  {/* Watch Demo Pill if video exists */}
                  {item.video_url && (
                    <div className="absolute bottom-3 right-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-950/85 text-amber-400 text-xs font-bold border border-amber-400/30">
                      <Play className="w-3.5 h-3.5 fill-amber-400" />
                      Watch Video Demo
                    </div>
                  )}

                  {/* Price on Image Bottom-Left */}
                  <div className="absolute bottom-3 left-3 flex items-baseline gap-2">
                    <span className="text-2xl font-black text-white">
                      ${item.price.toFixed(2)}
                    </span>
                    <span className="text-xs text-slate-400 line-through">
                      ${item.old_price.toFixed(2)}
                    </span>
                  </div>
                </Link>

                {/* Card Body */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                      <span className="font-semibold text-amber-400/90">{item.niche}</span>
                      <span className="inline-flex items-center gap-1 text-amber-300 font-bold">
                        <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                        {item.rating} ({item.reviews_count.toLocaleString()})
                      </span>
                    </div>

                    <Link href={`/p/${item.id}`}>
                      <h2 className="text-lg font-extrabold text-white group-hover:text-amber-400 transition-colors line-clamp-2 mb-2">
                        {item.short_title} — {item.title}
                      </h2>
                    </Link>

                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                      {item.solution_summary}
                    </p>
                  </div>

                  <div className="space-y-2.5 pt-2">
                    <OutboundButton
                      productId={item.id}
                      code={item.code}
                      title={item.short_title}
                      amazonUrl={item.amazon_url}
                      price={item.price}
                      label={`View ${item.code} on Amazon ($${item.price})`}
                    />
                    <Link
                      href={`/p/${item.id}`}
                      className="w-full inline-flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 font-semibold text-xs transition-colors"
                    >
                      <Flame className="w-3.5 h-3.5 text-amber-400" />
                      See Full Review & Video Demo
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
