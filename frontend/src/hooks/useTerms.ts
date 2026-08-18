import { useEffect, useState } from "react";
import { school, type Term } from "../api";

/** Loads academic terms and preselects the current one. */
export function useTerms() {
  const [terms, setTerms] = useState<Term[]>([]);
  const [termId, setTermId] = useState<number | undefined>(undefined);

  useEffect(() => {
    school
      .getTerms()
      .then((loaded) => {
        setTerms(loaded);
        setTermId(
          (previous) =>
            previous ?? loaded.find((term) => term.is_current)?.id ?? loaded[0]?.id,
        );
      })
      .catch(() => setTerms([]));
  }, []);

  return { terms, termId, setTermId };
}
