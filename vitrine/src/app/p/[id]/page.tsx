import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CheckCircle2, Star, ShieldCheck, Truck, Sparkles } from "lucide-react";
import productsData from "@/data/produtos.json";
import { Product } from "@/components/StorefrontClient";
import OutboundButton from "@/components/OutboundButton";

export function generateStaticParams() {
  const products = productsData as Product[];
  return products.map((p) => ({ id: p.id }));
}

export default async function ProductDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const products = productsData as Product[];
  const product = products.find(
    (p) => p.id === id || p.slug === id || p.code.replace("#", "") === id
  );

  if (!product) {
    notFound();
  }

  const discountPct = Math.round(
    ((product.old_price - product.price) / product.old_price) * 100
  );

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-xs sm:text-sm font-bold text-slate-400 hover:text-amber-400 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to All Viral Finds
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Vertical Video Player (9:16) or Product Image */}
        <div className="lg:col-span-5">
          <div className="rounded-3xl overflow-hidden bg-slate-900 border border-slate-800 shadow-2xl">
            {product.video_url ? (
              <div className="relative aspect-[9/16] bg-black">
                <video
                  src={product.video_url}
                  controls
                  autoPlay
                  muted
                  loop
                  playsInline
                  poster={product.image_url}
                  className="w-full h-full object-cover"
                />
              </div>
            ) : (
              <div className="relative aspect-square bg-slate-950">
                <img
                  src={product.image_url}
                  alt={product.title}
                  className="w-full h-full object-cover"
                />
              </div>
            )}
          </div>
        </div>

        {/* Right Column: High-Converting Copy & Amazon CTA */}
        <div className="lg:col-span-7 space-y-6">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3.5 py-1 rounded-xl bg-amber-400 text-slate-950 font-black text-sm">
              CODE {product.code}
            </span>
            <span className="px-3 py-1 rounded-xl bg-slate-800 text-amber-300 font-bold text-xs">
              {product.niche}
            </span>
            <span className="px-3 py-1 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold text-xs">
              ✓ In Stock on Amazon US
            </span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-black text-white leading-tight">
            {product.title}
          </h1>

          {/* Rating & Reviews */}
          <div className="flex items-center gap-3 text-sm">
            <div className="flex items-center gap-1 text-amber-400 font-extrabold">
              <Star className="w-4 h-4 fill-amber-400" />
              <span>{product.rating} / 5.0</span>
            </div>
            <span className="text-slate-500">•</span>
            <span className="text-slate-300 font-medium">
              {product.reviews_count.toLocaleString()}+ verified ratings on Amazon
            </span>
          </div>

          {/* Price Box */}
          <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
            <div>
              <span className="block text-xs uppercase tracking-wider text-slate-400 font-semibold">
                Amazon Prime Deal Price
              </span>
              <div className="flex items-baseline gap-3 mt-1">
                <span className="text-3xl sm:text-4xl font-black text-white">
                  ${product.price.toFixed(2)}
                </span>
                <span className="text-base text-slate-500 line-through">
                  ${product.old_price.toFixed(2)}
                </span>
                {discountPct > 0 && (
                  <span className="px-2.5 py-0.5 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 font-extrabold text-xs">
                    Save {discountPct}%
                  </span>
                )}
              </div>
            </div>
            <div className="text-right hidden sm:block">
              <span className="inline-flex items-center gap-1.5 text-xs font-bold text-sky-400">
                <Truck className="w-4 h-4" />
                FREE Prime Delivery
              </span>
              <span className="block text-[11px] text-slate-500 mt-0.5">
                Ships & handled by Amazon.com
              </span>
            </div>
          </div>

          {/* Hook Quote */}
          <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-200 text-sm italic">
            <Sparkles className="w-4 h-4 text-amber-400 inline mr-2 -mt-0.5" />
            &ldquo;{product.visual_hook}&rdquo;
          </div>

          {/* Primary CTA */}
          <div className="space-y-3">
            <OutboundButton
              productId={product.id}
              code={product.code}
              title={product.short_title}
              amazonUrl={product.amazon_url}
              price={product.price}
              label={`Buy on Amazon.com — $${product.price.toFixed(2)}`}
              className="w-full inline-flex items-center justify-center gap-2.5 rounded-2xl bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 text-slate-950 font-black py-4 px-6 text-base sm:text-lg shadow-xl shadow-amber-500/20 transition-all"
            />
            <p className="text-center text-xs text-slate-400 flex items-center justify-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Redirects securely to Amazon.com • 30-Day Amazon Return Guarantee
            </p>
          </div>

          {/* Why Americans Love It */}
          <div className="pt-4 border-t border-slate-800/80">
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-slate-300 mb-3">
              Why Everyone Is Buying This ({product.code}):
            </h2>
            <ul className="space-y-2.5">
              {product.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
