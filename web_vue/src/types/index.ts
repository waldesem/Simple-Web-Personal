import type { Component } from "vue";
import type { InputProps } from "@nuxt/ui/runtime/components/Input.vue.js";
import type { SelectProps } from "@nuxt/ui/runtime/components/Select.vue.js";
import type { TextareaProps } from "@nuxt/ui/runtime/components/Textarea.vue.js";

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

export type TableColumns<T> = {
  name: keyof T;
  header: string;
  cell?: (row: T) => string;
};

export type ItemFields<T> = {
  key: keyof T;
  label: string;
  slot?: boolean;
  div?: (row: T) => string;
  component?: (row: T) => Component;
};

type FormElementAttrs = {
  input: InputProps;
  select: SelectProps;
  textarea: TextareaProps;
};

export type FormFields<T> = {
  [K in keyof FormElementAttrs]: {
    element: K;
    key: keyof T;
    label: string;
    props: Omit<FormElementAttrs[K], "modelValue" | "defaultValue">;
    items?: K extends "select" ? string[] : never;
  };
}[keyof FormElementAttrs];

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
  editable: boolean;
  created: string;
  user_id: string;
}

export interface Previous {
  id: string;
  surname?: string;
  firstname?: string;
  patronymic?: string;
  changed?: string;
  reason?: string;
}
export interface Education {
  id: string;
  view?: string;
  institution: string;
  finished?: string;
  specialty: string;
}

export interface Staff {
  id: string;
  position: string;
  department?: string;
}

export interface Passport {
  id: string;
  view: string;
  series?: string;
  digits: string;
  agency?: string;
  issue: string;
}

export interface Address {
  id: string;
  view: string;
  address: string;
}

export interface Contact {
  id: string;
  view: string;
  contact: string;
}

export interface Work {
  id: string;
  starts: string;
  finished: string;
  workplace: string;
  address?: string;
  reason?: string;
  position: string;
}

export interface Affilation {
  id: string;
  view: string;
  organization: string;
  inn?: string;
  activity?: string;
}

export interface Verification {
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

export interface Pfo {
  id: string;
  theme: string;
  results: string;
  conclusion: Decisions;
  created: string;
}

export interface Inquisition {
  id: string;
  theme: string;
  info: string;
  created: string;
}

export interface Needs {
  id: string;
  info: string;
  initiator: string;
  origins?: string;
  created: string;
}

export type Items = {
  addresses: Address;
  affilations: Affilation;
  checks: Verification;
  contacts: Contact;
  documents: Passport;
  educations: Education;
  inquiries: Needs;
  investigations: Inquisition;
  person: Person;
  poligrafs: Pfo;
  previous: Previous;
  staffs: Staff;
  workplaces: Work;
};
