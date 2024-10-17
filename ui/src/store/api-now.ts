import {create} from "zustand";

import dayjs, {Dayjs} from "dayjs";

interface NowStore {
  loading: boolean
  now?: Dayjs
  fetchNow: () => void
  getNow: () => void
  setNow: (now: string) => void
}

export const nowStore = create<NowStore>((set, get) => ({
  loading: false,
  getNow: async () => {
    return get().now
  },
  setNow: (now: string) => {
    set({now: dayjs(now)})
  },
  fetchNow: async () => {
    try {
      set({loading: true})
      const response = await fetch(`${process.env.NEXT_PUBLIC_API}/hello`, {
        method: "GET",
        signal: AbortSignal.timeout(20000), // 20s timeout
      })
      if (!response.ok) {
        return Promise.reject(new Error('Network response was not ok'));
      }
      const setNow = get().setNow
      const data = await response.json()
      setNow(data.now)
      return
    } catch (error: unknown) {
      if (error instanceof Error) {
        console.error(error.message);
      } else {
        console.error('An unknown error occurred');
      }
    } finally {
      set({loading: false})
    }
  },
}))
