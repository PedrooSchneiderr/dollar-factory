import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CheckCircle2, Star, ShieldCheck, Truck, ExternalLink, Info } from "lucide-react";
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

  const hasRealDiscount = product.old_price > product.price;
  const discountPct = hasRealDiscount
    ? Math.round(((product.old_price - product.price) / product.old_price) * 100)
    : 0;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Back Link */}
      <Link
        href="/"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 mb-8 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to All Recommendations
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        {/* Left Column: Vertical Video Demo (9:16) */}
        <div className="lg:col-span-5 flex flex-col items-center">
          <div className="w-full max-w-sm rounded-3xl overflow-hidden bg-slate-950 border border-slate-300 shadow-xl relative aspect-[9/16]">
            {product.video_url ? (
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
            ) : (
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-full object-contain p-8 bg-white"
              />
            )}
          </div>
          <p className="text-[11px] text-slate-400 mt-2.5 text-center flex items-center gap-1">
            <Info className="w-3.5 h-3.5" />
            Field test demonstration video for {product.code}
          </p>
        </div>

        {/* Right Column: Editorial Review Breakdown */}
        <div className="lg:col-span-7 space-y-6">
          {/* Metadata badges */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-md bg-slate-900 text-white font-mono font-bold text-xs">
              CODE {product.code}
            </span>
            <span className="px-3 py-1 rounded-md bg-slate-100 text-slate-700 font-semibold text-xs border border-slate-200">
              {product.niche}
            </span>
            <span className="px-3 py-1 rounded-md bg-emerald-50 text-emerald-700 font-semibold text-xs border border-emerald-200 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> In Stock on Amazon Prime
            </span>
          </div>

          {/* Title */}
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-snug font-serif">
            {product.title}
          </h1>

          {/* Rating */}
          <div className="flex items-center gap-3 text-sm">
            <div className="flex items-center gap-1 text-slate-900 font-bold">
              <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
              <span>{product.rating.toFixed(1)} / 5.0</span>
            </div>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500 font-medium">
              {product.reviews_count.toLocaleString()}+ verified Amazon customer ratings
            </span>
          </div>

          {/* Editorial Tested Price Card */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold block">
                Verified Amazon Price
              </span>
              <div className="flex items-baseline gap-3 mt-1">
                <span className="text-3xl sm:text-4xl font-extrabold text-slate-900">
                  ${product.price.toFixed(2)}
                </span>
                {hasRealDiscount && (
                  <>
                    <span className="text-base text-slate-400 line-through">
                      ${product.old_price.toFixed(2)}
                    </span>
                    <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
                      Save {discountPct}%
                    </span>
                  </>
                )}
              </div>
            </div>

            <div className="sm:text-right border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-100">
              <span className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-800">
                <Truck className="w-4 h-4 text-slate-600" />
                FREE Prime Delivery Available
              </span>
              <span className="block text-[11px] text-slate-400 mt-0.5">
                Shipped & fulfilled directly by Amazon.com
              </span>
            </div>
          </div>

          {/* Direct Outbound Button */}
          <div className="space-y-3 pt-2">
            <OutboundButton
              productId={product.id}
              code={product.code}
              title={product.short_title}
              amazonUrl={product.amazon_url}
              price={product.price}
              label={`View Listing on Amazon.com — $${product.price.toFixed(2)}`}
              className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold py-4 px-6 text-base shadow-sm transition-all cursor-pointer"
            />
            <p className="text-center text-xs text-slate-500 flex items-center justify-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              Secure redirect to Amazon.com • Standard 30-Day Amazon Return Guarantee
            </p>
          </div>

          {/* The Problem It Solves */}
          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              The Everyday Problem It Solves:
            </h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              {product.solution_summary}
            </p>
          </div>

          {/* Key Specifications & Benefits */}
          <div className="pt-4 border-t border-slate-200 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Key Tested Features:
            </h2>
            <ul className="space-y-2.5">
              {product.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-sm text-slate-700">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
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
