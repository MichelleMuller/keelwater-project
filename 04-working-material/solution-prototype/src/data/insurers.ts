import type { Insurer, InsurerId } from "./schema";

// [INVENTED] One insurer per customer segment in internal-data.md §1.
export const INSURERS: Record<InsurerId, Insurer> = {
  harbour: {
    id: "harbour",
    name: "Harbour Mutual",
    market: "UK",
    currency: "£",
    segment: "Simple-heavy: large direct personal motor",
    fraudVendor: "Shift Claims",
    simpleMaxAmount: 3000,
    seniorReviewAmount: 2500,
  },
  northgate: {
    id: "northgate",
    name: "Northgate Direct",
    market: "UK",
    currency: "£",
    segment: "Mixed: regional personal motor",
    fraudVendor: "FRISS",
    simpleMaxAmount: 2500,
    seniorReviewAmount: 2000,
  },
  fleetwise: {
    id: "fleetwise",
    name: "Fleetwise Commercial",
    market: "US",
    currency: "$",
    segment: "Complex-heavy: fleet and commercial",
    fraudVendor: "Verisk Claim Scoring",
    simpleMaxAmount: 4000,
    seniorReviewAmount: 3000,
  },
};

export const INSURER_LIST = Object.values(INSURERS);

export function money(insurerId: InsurerId, amount: number) {
  return `${INSURERS[insurerId].currency}${Math.round(amount).toLocaleString("en-GB")}`;
}
