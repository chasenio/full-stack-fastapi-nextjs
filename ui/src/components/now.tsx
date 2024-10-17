'use client'

import {nowStore} from "@/store/api-now";
import {useEffect} from "react";

export const ServerNow = () => {
  const fetchNow = nowStore((state) => state.fetchNow);
  const serverNow = nowStore((state) => state.now);
  const loading = nowStore((state) => state.loading);

  useEffect(() => {
    fetchNow();
  }, [fetchNow]);

  if (loading) {
    return <>Loading...</>
  }

  return (
      <>
        Server now:
        <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">
          {serverNow?.format()}
        </code>
      </>
  )
}
