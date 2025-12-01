import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Pricing - Reframe | Affordable AI Text Reframing Plans",
  description: "Transform AI text with 6 authentic voices adapted for any age group. Choose from Monthly/Yearly subscriptions. All prices in INR with live currency conversions.",
  keywords: ["AI text reframing", "content transformation", "pricing", "subscription plans", "AI text rewriting", "affordable AI"],
  openGraph: {
    title: "Pricing - Reframe | Affordable AI Text Reframing",
    description: "Transform AI text with 6 authentic voices adapted for any age group. Monthly/Yearly subscriptions available.",
    type: "website",
    siteName: "Reframe",
  },
  twitter: {
    card: "summary_large_image",
    title: "Pricing - Reframe | Affordable AI Text Reframing",
    description: "Transform AI text with 6 authentic voices. Plans from $2.99/week.",
  },
  alternates: {
    canonical: "/pricing",
  },
};

export default function PricingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {/* JSON-LD Structured Data for Pricing */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Reframe Text Reframing Service",
            "description": "Transform AI-generated text into authentic human voices with 6 distinct tones",
            "brand": {
              "@type": "Brand",
              "name": "Reframe"
            },
            "offers": [
              {
                "@type": "Offer",
                "name": "Free Tier",
                "price": "0",
                "priceCurrency": "USD",
                "description": "3 requests per day, 3 essential tones"
              },
              {
                "@type": "Offer",
                "name": "Monthly Pro",
                "price": "9.99",
                "priceCurrency": "USD",
                "priceSpecification": {
                  "@type": "UnitPriceSpecification",
                  "price": "9.99",
                  "priceCurrency": "USD",
                  "billingDuration": "P1M"
                },
                "description": "Unlimited requests, all 6 tones unlocked"
              },
              {
                "@type": "Offer",
                "name": "Yearly Pro",
                "price": "99",
                "priceCurrency": "USD",
                "priceSpecification": {
                  "@type": "UnitPriceSpecification",
                  "price": "99",
                  "priceCurrency": "USD",
                  "billingDuration": "P1Y"
                },
                "description": "Unlimited requests, 17% savings, all features"
              }
            ]
          }),
        }}
      />
      {children}
    </>
  );
}

