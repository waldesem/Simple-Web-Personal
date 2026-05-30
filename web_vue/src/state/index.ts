import { useStorage } from "@vueuse/core";
import { Session } from "@/types";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const refreshToken = useStorage("refreshToken", "", localStorage, {
  mergeDefaults: true,
});

export const session = useStorage("session", {} as Session, sessionStorage);
