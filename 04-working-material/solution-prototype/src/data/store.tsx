import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { Claim, InsurerId } from "./schema";
import { seedClaims } from "./seed";

export type View = "consumer" | "handler";
export type HandlerPage = "inbox" | "bulk" | "workflow" | "agent";

type Store = {
  claims: Claim[];
  addClaim: (c: Claim) => void;
  updateClaim: (id: string, update: (c: Claim) => Claim) => void;
  view: View;
  setView: (v: View) => void;
  page: HandlerPage;
  setPage: (p: HandlerPage) => void;
  insurer: InsurerId;
  setInsurer: (i: InsurerId) => void;
};

const StoreContext = createContext<Store | null>(null);

const PAGES: HandlerPage[] = ["inbox", "bulk", "workflow", "agent"];

function fromHash(): { view: View; page: HandlerPage } {
  const [view, page] = window.location.hash.replace("#", "").split("/");
  return {
    view: view === "handler" ? "handler" : "consumer",
    page: PAGES.includes(page as HandlerPage) ? (page as HandlerPage) : "inbox",
  };
}

export function StoreProvider({ children }: { children: ReactNode }) {
  const initial = fromHash();
  const [claims, setClaims] = useState<Claim[]>(seedClaims);
  const [view, setViewState] = useState<View>(initial.view);
  const [page, setPageState] = useState<HandlerPage>(initial.page);

  const setView = (v: View) => {
    setViewState(v);
    window.history.replaceState(null, "", v === "handler" ? `#handler/${page}` : "#consumer");
  };
  const setPage = (p: HandlerPage) => {
    setPageState(p);
    window.history.replaceState(null, "", `#handler/${p}`);
  };
  const [insurer, setInsurer] = useState<InsurerId>("harbour");

  const value = useMemo<Store>(
    () => ({
      claims,
      addClaim: (c) => setClaims((cs) => [c, ...cs]),
      updateClaim: (id, update) => setClaims((cs) => cs.map((c) => (c.id === id ? update(c) : c))),
      view,
      setView,
      page,
      setPage,
      insurer,
      setInsurer,
    }),
    [claims, view, page, insurer],
  );

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}

export function useStore() {
  const s = useContext(StoreContext);
  if (!s) throw new Error("useStore outside StoreProvider");
  return s;
}
