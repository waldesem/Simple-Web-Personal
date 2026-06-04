import { useStorage } from "@vueuse/core";
import { Session } from "@/types";

export const access = useStorage("access", "", localStorage);

export const refresh = useStorage("refresh", "", localStorage);

export const session = useStorage("session", {} as Session, sessionStorage);
