import type { Metadata } from "next";
import { GoogleAnalytics } from "@next/third-parties/google";
import "./globals.css";

// GA4 Measurement ID situs Parameter (parameter.cloud). Publik — aman di-commit.
// Bisa di-override lewat env NEXT_PUBLIC_GA_ID kalau perlu.
const GA_ID = process.env.NEXT_PUBLIC_GA_ID ?? "G-S6S2CZCE6F";
// Cuma nyalain GA di production, biar dev/localhost nggak ngotorin data.
const gaEnabled = process.env.NODE_ENV === "production" && Boolean(GA_ID);

export const metadata: Metadata = {
  metadataBase: new URL("https://parameter.cloud"),
  title: "Parameter — Studio Produk Digital Indonesia",
  description:
    "Parameter membangun produk digital yang beneran dipakai. Kami bikin SaaS sendiri (Platform Belajar Pro, Ritme) & bantu UMKM punya aplikasi, sistem, website, dan landing page yang naikin produktivitas.",
  openGraph: {
    title: "Parameter — Studio Produk Digital Indonesia",
    description:
      "Builder produk digital, bukan sekadar vendor. Atur parameter pertumbuhan bisnismu.",
    type: "website",
    locale: "id_ID",
    images: ["/parameter-square.jpg"],
  },
  // Bukti kepemilikan parameter.cloud untuk Meta Business Manager. Nilainya
  // publik — ini penanda kepemilikan, bukan rahasia, jadi aman di-commit.
  //
  // Ditaruh lewat metadata API dan bukan sebagai tag mentah di <head> karena
  // Meta menolak tag yang disisipkan JavaScript di browser; Next merender ini
  // di server, sehingga sudah ada di HTML saat crawler Meta membacanya.
  other: {
    "facebook-domain-verification": "tvlmlm2380mqpqv9tu9ia690doehs1",
  },
  icons: {
    icon: [
      { url: "/parameter-favicon-white-20260617.png", type: "image/png", sizes: "512x512" },
    ],
    shortcut: [{ url: "/parameter-favicon-white-20260617.png", type: "image/png" }],
    apple: [
      { url: "/parameter-apple-icon-white-20260617.png", type: "image/png", sizes: "180x180" },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" crossOrigin="" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&f[]=satoshi@400,500,700&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-dvh">{children}</body>
      {gaEnabled ? <GoogleAnalytics gaId={GA_ID} /> : null}
    </html>
  );
}
