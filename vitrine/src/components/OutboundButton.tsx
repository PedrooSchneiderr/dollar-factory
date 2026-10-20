"use client";

import React from "react";
import { ExternalLink, ShieldCheck } from "lucide-react";

interface OutboundButtonProps {
  productId: string;
  code: string;
  title: string;
  amazonUrl: string;
  price: number;
  label?: string;
  className?: string;
}

export default function OutboundButton({
  productId,
  code,
  title,
  amazonUrl,
  price,
  label = "Check Price on Amazon",
  className = "",
}: OutboundButtonProps) {
  const handleOutboundClick = () => {
    try {
      // Dispara evento local de analytics + compatível com Meta Pixel (fbq) e TikTok Pixel (ttq)
      fetch("/api/click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          productId,
          code,
          title,
          price,
          timestamp: new Date().toISOString(),
        }),
        keepalive: true,
      }).catch(() => {});

      const win = window as unknown as {
        fbq?: (...args: unknown[]) => void;
        ttq?: { track?: (...args: unknown[]) => void };
      };
      if (typeof win.fbq === "function") {
        win.fbq("trackCustom", "click_outbound_amazon", {
          content_ids: [productId],
          content_name: title,
          value: price,
          currency: "USD",
        });
      }
      if (win.ttq && typeof win.ttq.track === "function") {
        win.ttq.track("ClickButton", {
          content_id: productId,
          content_name: title,
          value: price,
          currency: "USD",
        });
      }
    } catch {
      // ignore tracking errors so redirect never fails
    }
  };

  return (
    <a
      href={amazonUrl}
      target="_blank"
      rel="noopener noreferrer sponsored"
      onClick={handleOutboundClick}
      className={
        className ||
        "w-full inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 text-slate-950 font-extrabold py-3.5 px-5 text-sm shadow-lg shadow-amber-500/20 transition-all active:scale-[0.99]"
      }
    >
      <span>{label}</span>
      <ExternalLink className="w-4 h-4 stroke-[2.5]" />
    </a>
  );
}
