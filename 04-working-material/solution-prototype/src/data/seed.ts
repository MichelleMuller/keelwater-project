import { INSURERS } from "./insurers";
import { requiredItems, type Claim, type IncidentType, type InsurerId } from "./schema";

// [INVENTED] Deterministic synthetic claims. Amounts loosely follow the Kaggle claim
// distribution (median ~4k); mix per insurer follows the segments in internal-data.md §1.

function rng(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const r = rng(42);
const pick = <T,>(xs: T[]) => xs[Math.floor(r() * xs.length)];
const between = (lo: number, hi: number) => Math.round(lo + r() * (hi - lo));
const chance = (p: number) => r() < p;

const FIRST = ["Sarah", "James", "Priya", "Tom", "Aisha", "Daniel", "Chloe", "Marcus", "Emily", "Oliver", "Grace", "Liam", "Fatima", "Noah", "Hannah", "Ethan", "Zara", "Ryan", "Megan", "Samuel"];
const LAST = ["Patel", "Hughes", "Okafor", "Bennett", "Khan", "Murphy", "Clarke", "Evans", "Nowak", "Reid", "Ahmed", "Walsh", "Turner", "Shah", "Price", "Doyle", "Ward", "Kowalski"];
const CARS: [string, string, number][] = [
  ["Ford", "Fiesta", 9000], ["Vauxhall", "Corsa", 8000], ["VW", "Golf", 15000], ["Toyota", "Yaris", 12000],
  ["BMW", "3 Series", 24000], ["Nissan", "Qashqai", 17000], ["Kia", "Sportage", 19000], ["Tesla", "Model 3", 32000],
  ["Ford", "Transit", 22000], ["Mercedes", "Sprinter", 30000],
];
const UK_PLACES = ["A40, Oxford", "Tesco car park, Leeds", "M6 J10, Walsall", "High St, Bristol", "Ring road, Norwich", "Outside home, Cardiff"];
const US_PLACES = ["I-95, Baltimore", "Depot lot, Newark", "Route 1, Trenton", "Warehouse yard, Camden", "I-76, Philadelphia"];

const DESCRIPTIONS: Record<IncidentType, string[]> = {
  collision: [
    "Car in front braked suddenly and I couldn't stop in time.",
    "Other driver pulled out of a side road and hit my front wing.",
    "Reversed into a bollard in a car park.",
    "Hit from behind while queuing at traffic lights.",
  ],
  windscreen: ["Stone chip on the motorway cracked the windscreen.", "Crack spread across the windscreen overnight."],
  theft: ["Car taken from outside my house overnight. Keys still with me.", "Catalytic converter stolen from the driveway."],
  vandalism: ["Keyed down the passenger side while parked.", "Wing mirror smashed while parked on the street."],
  weather: ["Tree branch fell on the roof during the storm.", "Flood water came into the footwells."],
  other: ["Pothole damaged the front tyre and alloy.", "Garage door came down on the bonnet."],
};

const MIX: Record<InsurerId, [IncidentType, number][]> = {
  harbour: [["windscreen", 0.3], ["collision", 0.4], ["vandalism", 0.1], ["weather", 0.08], ["other", 0.08], ["theft", 0.04]],
  northgate: [["collision", 0.55], ["windscreen", 0.15], ["vandalism", 0.1], ["weather", 0.07], ["other", 0.07], ["theft", 0.06]],
  fleetwise: [["collision", 0.7], ["theft", 0.1], ["vandalism", 0.08], ["windscreen", 0.07], ["other", 0.05]],
};

function weighted(mix: [IncidentType, number][]): IncidentType {
  let x = r();
  for (const [t, p] of mix) {
    if ((x -= p) <= 0) return t;
  }
  return mix[0][0];
}

const NOW = new Date("2026-10-17T09:30:00Z").getTime();
const iso = (msAgo: number) => new Date(NOW - msAgo).toISOString();
const day = 86_400_000;

function makeClaim(n: number, insurer: InsurerId): Claim {
  const ins = INSURERS[insurer];
  const type = weighted(MIX[insurer]);
  const [make, model, baseValue] = insurer === "fleetwise" ? pick(CARS.slice(7)) : pick(CARS.slice(0, 8));
  const year = between(2012, 2025);
  const value = Math.round(baseValue * (1 - (2026 - year) * 0.06) * (0.8 + r() * 0.4));
  const thirdParty = type === "collision" && chance(insurer === "harbour" ? 0.3 : insurer === "northgate" ? 0.5 : 0.65);
  const injuries = thirdParty && chance(insurer === "fleetwise" ? 0.35 : 0.2);
  const amount =
    type === "windscreen" ? between(180, 1100)
    : type === "theft" ? Math.round(value * (0.5 + r() * 0.6))
    : type === "collision" ? between(600, thirdParty ? 14000 : 6000)
    : between(250, 4500);
  const received = between(5, 60 * 30) * 60_000;
  const policyAgeDays = chance(0.08) ? between(3, 40) : between(60, 2500);
  const priorClaims = chance(0.12) ? between(2, 5) : chance(0.3) ? 1 : 0;
  const first = pick(FIRST);
  const last = pick(LAST);

  const fraudReasons: string[] = [];
  let score = 0.05 + r() * 0.25;
  if (policyAgeDays < 30) { score += 0.35; fraudReasons.push(`Claim ${policyAgeDays} days after policy start`); }
  if (priorClaims >= 3) { score += 0.25; fraudReasons.push(`${priorClaims} prior claims in 5 years`); }
  if (type === "theft") { score += 0.15; fraudReasons.push("Theft claim"); }
  if (amount > value * 1.1 && type !== "theft") { score += 0.2; fraudReasons.push("Claimed amount above vehicle value"); }

  const claim: Claim = {
    id: `CLM-${1000 + n}`,
    insurer,
    receivedAt: iso(received),
    channel: pick(["web form", "web form", "web form", "phone", "broker"]),
    policy: {
      number: `${insurer.slice(0, 2).toUpperCase()}-${between(100000, 999999)}`,
      startDate: iso(policyAgeDays * day).slice(0, 10),
      cover: chance(0.8) ? "comprehensive" : chance(0.5) ? "third party, fire & theft" : "third party",
      excess: pick([100, 250, 250, 350, 500]),
    },
    claimant: {
      name: `${first} ${last}`,
      email: `${first.toLowerCase()}.${last.toLowerCase()}@example.com`,
      phone: ins.market === "UK" ? `07${between(100, 999)} ${between(100000, 999999)}` : `(${between(200, 989)}) 555-${between(1000, 9999)}`,
      priorClaims5y: priorClaims,
    },
    vehicle: {
      reg: ins.market === "UK" ? `${pick(["AB", "KX", "LM", "RT", "YP"])}${between(10, 73)} ${pick(["FHD", "KLM", "XRT", "PZA", "GDN"])}` : `${between(100, 999)}-${pick(["KTR", "PLA", "NWD"])}`,
      make, model, year, value,
    },
    incident: {
      date: iso(received + between(0, 3) * day).slice(0, 10),
      type,
      location: ins.market === "UK" ? pick(UK_PLACES) : pick(US_PLACES),
      description: pick(DESCRIPTIONS[type]),
      policeReport: type === "theft" || injuries ? chance(0.7) : thirdParty ? chance(0.5) : chance(0.1),
    },
    parties: {
      thirdPartyInvolved: thirdParty,
      thirdParty: thirdParty ? { name: `${pick(FIRST)} ${pick(LAST)}`, insurer: pick(["Aviva", "Admiral", "Direct Line", "Progressive", "Geico"]), reg: chance(0.8) ? "WX19 PLK" : undefined } : undefined,
      injuries,
      injuryDetails: injuries ? pick(["Whiplash, saw GP", "Bruised shoulder", "Passenger taken to A&E as a precaution"]) : undefined,
      witnesses: thirdParty ? between(0, 2) : 0,
    },
    damage: {
      estimatedAmount: amount,
      drivable: type !== "theft" && chance(0.75),
      photos: type === "theft" ? 0 : chance(0.85) ? between(1, 6) : 0,
      repairEstimate: chance(0.5),
    },
    missingInfo: [],
    fraud: { score: Math.min(0.97, Math.round(score * 100) / 100), vendor: ins.fraudVendor, reasons: fraudReasons },
    status: "new",
    history: [{ at: iso(received), actor: "system", action: "Claim received", detail: "via first notice of loss form" }],
  };
  if (claim.incident.policeReport) claim.incident.policeRef = `REF-${between(10000, 99999)}`;
  claim.missingInfo = requiredItems(claim);
  return claim;
}

export function seedClaims(): Claim[] {
  const counts: [InsurerId, number][] = [["harbour", 28], ["northgate", 20], ["fleetwise", 12]];
  const claims: Claim[] = [];
  let n = 1;
  for (const [insurer, count] of counts) {
    for (let i = 0; i < count; i++) claims.push(makeClaim(n++, insurer));
  }
  return claims.sort((a, b) => b.receivedAt.localeCompare(a.receivedAt));
}
