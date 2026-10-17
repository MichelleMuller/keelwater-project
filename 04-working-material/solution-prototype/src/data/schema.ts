export type Pile = "Simple" | "Needs a closer look" | "Suspicious";
export const PILES: Pile[] = ["Simple", "Needs a closer look", "Suspicious"];

export type InsurerId = "harbour" | "northgate" | "fleetwise";

export type Insurer = {
  id: InsurerId;
  name: string;
  market: "UK" | "US";
  currency: "£" | "$";
  segment: string;
  fraudVendor: string;
  simpleMaxAmount: number;
  seniorReviewAmount: number;
};

export type IncidentType = "collision" | "windscreen" | "theft" | "vandalism" | "weather" | "other";

export type ClaimStatus = "new" | "waiting on claimant" | "sorted" | "senior review before payment";

export type HistoryEntry = { at: string; actor: string; action: string; detail?: string };

export type Claim = {
  id: string;
  insurer: InsurerId;
  receivedAt: string;
  channel: "web form" | "phone" | "broker";
  policy: { number: string; startDate: string; cover: "comprehensive" | "third party, fire & theft" | "third party"; excess: number };
  claimant: { name: string; email: string; phone: string; priorClaims5y: number };
  vehicle: { reg: string; make: string; model: string; year: number; value: number };
  incident: {
    date: string;
    type: IncidentType;
    location: string;
    description: string;
    policeReport: boolean;
    policeRef?: string;
  };
  parties: {
    thirdPartyInvolved: boolean;
    thirdParty?: { name: string; insurer?: string; reg?: string };
    injuries: boolean;
    injuryDetails?: string;
    witnesses: number;
  };
  damage: { estimatedAmount: number; drivable: boolean; photos: number; repairEstimate: boolean };
  missingInfo: string[];
  fraud: { score: number; vendor: string; reasons: string[] };
  suggestion?: { pile: Pile; reasons: string[]; confidence: number; rule: string; workflowVersion: string };
  pile?: Pile;
  status: ClaimStatus;
  history: HistoryEntry[];
};

export function requiredItems(c: Pick<Claim, "incident" | "parties" | "damage">): string[] {
  const missing: string[] = [];
  if (c.damage.photos === 0 && c.incident.type !== "theft") missing.push("photos of the damage");
  const needsPolice = c.incident.type === "theft" || c.parties.injuries || c.parties.thirdPartyInvolved;
  if (needsPolice && !c.incident.policeReport) missing.push("police report");
  if (c.parties.thirdPartyInvolved && !c.parties.thirdParty?.reg) missing.push("third party's vehicle registration");
  if (c.damage.estimatedAmount > 2000 && !c.damage.repairEstimate) missing.push("repair estimate");
  return missing;
}
