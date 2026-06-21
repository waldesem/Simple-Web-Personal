import type { Component } from "vue";
import type {
  AccordionItem,
  InputProps,
  SelectProps,
  TextareaProps,
} from "@nuxt/ui";

export enum Actions {
  delete = "delete",
  block = "block",
  reset = "reset",
}

export enum Roles {
  admin = "admin",
  api = "api",
  user = "user",
  guest = "guest",
}

export enum Conclusions {
  agreed = "СОГЛАСОВАНО",
  comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ",
  cancel = "СНЯТ С ПРОВЕРКИ",
  denied = "ОТКАЗАНО В СОГЛАСОВАНИИ",
}

export enum Decisions {
  agreed = "БЕЗ ЗАМЕЧАНИЙ",
  comments = "С КОММЕНТАРИЯМИ",
  cancel = "ОТКАЗ ОТ ПРОВЕРКИ",
  denied = "НЕГАТИВ",
}

export type ItemFields<T> = {
  key: keyof T;
  label: string;
  slot?: boolean;
  foo?: (row: T) => string;
  component?: (row: T) => Component;
};

export type FormElemAttrs = {
  input: InputProps;
  select: SelectProps;
  textarea: TextareaProps;
};

export type FormFields<T> = {
  [K in keyof FormElemAttrs]: {
    element?: K;
    key: keyof T;
    label: string;
    props: Omit<FormElemAttrs[K], "modelValue" | "defaultValue">;
  };
}[keyof FormElemAttrs];

export interface Navigations extends AccordionItem {
  label: string;
  slot: keyof Items;
}

export interface Auth {
  message: string;
  access_token: string;
  refresh_token: string;
}

export interface Login {
  username: string;
  password: string;
  new_pswd: string;
  conf_pswd: string;
}

export interface Session {
  id: string;
  fullname: string;
  username: string;
  email: string;
  role: Roles;
}

export interface User extends Session {
  pswd_create: string;
  change_pswd: boolean;
  blocked: boolean;
  deleted: boolean;
  created: string;
  attempt: string;
}

export interface Person {
  id: string;
  surname: string;
  firstname: string;
  patronymic?: string;
  birthday: string;
  birthplace?: string;
  citizenship?: string;
  dual?: string;
  snils?: string;
  inn?: string;
  marital?: string;
  addition?: string;
  destination?: string;
  created: string;
}

interface Previous {
  id: string;
  surname: string;
  firstname?: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}
interface Education {
  id: string;
  view?: string;
  institution: string;
  finished?: string;
  specialty: string;
}

interface Staff {
  id: string;
  position: string;
  department?: string;
}

interface Passport {
  id: string;
  view: string;
  series?: string;
  digits: string;
  agency?: string;
  issue: string;
}

interface Address {
  id: string;
  view: string;
  address: string;
}

interface Contact {
  id: string;
  view: string;
  contact: string;
}

interface Work {
  id: string;
  starts: string;
  finished: string;
  workplace: string;
  address?: string;
  reason?: string;
  position: string;
}

interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn?: string;
  activity?: string;
}

interface Verification {
  id: string;
  workplace?: string;
  document?: string;
  debt?: string;
  bankruptcy?: string;
  bki?: string;
  courts?: string;
  affilation?: string;
  terrorist?: string;
  internet?: string;
  cronos?: string;
  addition?: string;
  conclusion: Conclusions;
  comment?: string;
  created: string;
}

interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: Decisions;
  created: string;
}

interface Inquisition {
  id: string;
  theme: string;
  info: string;
  created: string;
}

interface Needs {
  id: string;
  info: string;
  initiator: string;
  created: string;
}

export interface Items {
  addresses: Address;
  affilations: Affilation;
  checks: Verification;
  contacts: Contact;
  documents: Passport;
  educations: Education;
  inquiries: Needs;
  investigations: Inquisition;
  poligrafs: Pfo;
  previous: Previous;
  staffs: Staff;
  workplaces: Work;
}
