import { useStorage } from "@vueuse/core";
import { Session } from "@/types";

export const access = useStorage("access", "", localStorage, {
  mergeDefaults: true,
});

export const refresh = useStorage("refresh", "", localStorage, {
  mergeDefaults: true,
});

export const session = useStorage("session", {} as Session, sessionStorage);
