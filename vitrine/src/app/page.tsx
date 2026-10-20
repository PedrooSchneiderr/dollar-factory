import React from "react";
import StorefrontClient, { Product } from "@/components/StorefrontClient";
import productsData from "@/data/produtos.json";

export default function HomePage() {
  const products = productsData as Product[];
  return <StorefrontClient products={products} />;
}
